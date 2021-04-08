#coding:utf-8
import logging
logging.getLogger("requests").setLevel(logging.WARNING)
import csv
import jieba
import pickle
from fuzzywuzzy import fuzz
import math
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import lil_matrix
from sklearn.naive_bayes import MultinomialNB
from znwd_1233 import load_corpus_data
import warnings
warnings.filterwarnings("ignore")

'''
    @brief: 用于序列化分类模型及模糊匹配相关数据文件
'''


def load_label_url():
    with open('znwd_label_url.csv','r',encoding='utf-8') as f:
        name_id = {}
        label_url = csv.reader(f)
        header = next(label_url)
        for power_name_id in label_url:
            name_id[power_name_id[0]] = power_name_id[1]
    return name_id


def load_cut_save(filename,load = False):
    jieba.load_userdict('UserDefined_words.txt')
    corpus = []
    label = []
    with open(filename,'rt',encoding='utf-8') as f:
        data_corpus = csv.reader(f)
        header = next(data_corpus)
        for words in data_corpus:
            word = jieba.cut(words[1])
            doc = []
            for x in word:
                 if x not in stop_words and not x.isdigit():
                     doc.append(x)
            corpus.append(' '.join(doc))
            label.append(words[0])
    if load == True:
        with open('corpus.oj','wb') as f:
            pickle.dump(corpus,f)
        with open('label.oj','wb') as f:
            pickle.dump(label,f)
    return corpus,label

def train_model():

    with open('corpus.oj','rb') as f_corpus:
        corpus = pickle.load(f_corpus)

    with open('label.oj','rb') as f_label:
        label = pickle.load(f_label,encoding='bytes')


    vectorizer = CountVectorizer(min_df=1)
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    words_frequency = vectorizer.fit_transform(corpus)
    word = vectorizer.get_feature_names()
    saved = input_tfidf(vectorizer.vocabulary_,sparse.csc_matrix(words_frequency),len(corpus))
    model = MultinomialNB()
    model.fit(tfidf,label)


    with open('model.oj','wb') as f_model:
        pickle.dump(model,f_model)

    with open('idf.oj','wb') as f_idf:
        pickle.dump(saved,f_idf)

    return model,tfidf,label

class input_tfidf(object):
    def __init__(self,feature_index,frequency,docs):
        self.feature_index = feature_index
        self.frequency = frequency
        self.docs = docs
        self.len = len(feature_index)

    def key_count(self,input_words):
        keys = jieba.cut(input_words)
        count = {}
        for key in keys:
            num = count.get(key, 0)
            count[key] = num + 1
        return count

    def getTdidf(self,input_words):
        count = self.key_count(input_words)
        result = lil_matrix((1, self.len))
        frequency = sparse.csc_matrix(self.frequency)
        for x in count:
            word = self.feature_index.get(x)
            if word != None and word>=0:
                word_frequency = frequency.getcol(word)
                feature_docs = word_frequency.sum()
                tfidf = count.get(x) * (math.log((self.docs+1) / (feature_docs+1))+1)
                result[0, word] = tfidf
        return result

def model_predict(input_str):
    f = open('idf.oj','rb')
    idf = pickle.load(f)
    f.close()
    f = open('model.oj','rb')
    model = pickle.load(f)
    f.close()
    tfidf = idf.getTdidf(input_str)
    classifiction = (model.predict(tfidf))
    # print(model.predict_proba(tfidf))
    prob = model.predict_proba(tfidf).max()
    name_id = load_label_url()
    if prob >= 0.5:
        answer1 = str(classifiction[0],'utf-8')
    else:
        answer1 = None
    return answer1

def similarity(input_questions):
    with open('corpus_1233.oj', 'rb') as f:
        corpus = pickle.load(f,encoding='bytes')

    with open('question_1233.oj', 'rb') as f:
        question = pickle.load(f,encoding='bytes')

    with open('answer_1233.oj', 'rb') as f:
        answer = pickle.load(f,encoding='bytes')


    text = {}
    train = []
    answer2 = []
    for key, value in enumerate(corpus):
        similarity = fuzz.ratio(input_questions, value)
        if similarity > 40:
            text[key] = similarity
    if len(text) >= 3:
        train = sorted(text.items(), key=lambda d: d[1], reverse=True)
        # print(u"与您提的疑问相似的问题有\n")
        for i in range(3):
            an = {"question":question[train[i][0]],"answer":answer[train[i][0]]}
            answer2.append(an)
            # print("%d、" % (i + 1), \
            #     " 问题：%s\n" % str(question[train[i][0]],'utf-8'), \
            #     " 答案：%s" % str(answer[train[i][0]],'utf-8'))
    elif len(text) == 2:
        train = sorted(text.items(), key=lambda d: d[1], reverse=True)
        # print("与您提的疑问相似的问题有\n")
        for i in range(2):
            an = {"question":question[train[i][0]],"answer":answer[train[i][0]]}
            answer2.append(an)
            # print("%d、" % (i + 1), \
            #     " 问题：%s\n" % str(question[train[i][0]],'utf-8'), \
            #     " 答案：%s" % str(answer[train[i][0]],'utf-8'))
    elif len(text) == 1:
        an = {"question": question[list(text.keys())[0]], "answer": answer[list(text.keys())[0]]}
        answer2.append(an)
        # print("与您提的疑问相似的问题有：\n", \
        #     " 问题：%s" % str(question[text.keys()[0]],'utf-8'), \
        #     " 答案：%s" % str(answer[text.keys()[0]],'utf-8'))
    else:
        # print("您所提的疑问无其他相似问题！")
        an = {"question":None,"answer":None}
        answer2.append(an)
    return answer2

def get_greeting(input_questions,question,answer):
    text = {}
    for key, value in enumerate(question):
        similarity = fuzz.ratio(input_questions, value)
        if similarity > 60:
            text[key] = similarity
    if len(text) > 0:
        train = sorted(text.items(), key=lambda d: d[1], reverse=True)
        answer3 = answer[train[0][0]]
    else:
        answer3 = None
    return  answer3


def sim(doc):
    input_questions = ''
    input_words = jieba.cut(doc)

    for x in input_words:
        if x not in stop_words:
            input_questions += x

    answer2 = similarity(input_questions)
    return answer2

def ans_show(returnSet):
    if returnSet[2] is not None:
        print("机器人Mike > %s"%returnSet[2])
    elif returnSet[0] is not None:
        print("机器人Mike > 您的问题属于<%s>专栏\n"%returnSet[0])
        if returnSet[1][0]['question'] is not None:
            print("机器人Mike > Mike还知道其他一些问题例如：\n")
            for i in range(len(returnSet[1])):
                print("%d、" % (i + 1), \
                    " 问题：%s\n" % str(returnSet[1][i]['question'],'utf-8'), \
                    " 答案：%s" % str(returnSet[1][i]['answer'],'utf-8'))
    elif returnSet[1][0]['question'] is not None:
        print("机器人Mike > Mike知道相似的问题如下：")
        for i in range(len(returnSet[1])):
            print("%d、" % (i + 1), \
                  " 问题：%s\n" % str(returnSet[1][i]['question'], 'utf-8'), \
                  " 答案：%s" % str(returnSet[1][i]['answer'], 'utf-8'))
    else:
        print("机器人Mike > 主人问的问题太过深奥，Mike才疏学浅暂时无法为您解答，待我读书破万卷后成为您的百科机器人")

if __name__ == "__main__":

    with open('stop_words.txt', 'rb') as f:
        stop_words = f.read().splitlines()

    #sklearn分类数据
    filename = 'znwd_corpus.csv'
    corpus, label = load_cut_save(filename,load=True)
    train_model()

    #模糊匹配数据
    filename_1233 = 'znwd_1233.csv'
    corpus, label, question, answer = load_corpus_data(filename_1233,load=True)

