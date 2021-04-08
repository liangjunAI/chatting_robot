# -*- coding:utf-8 -*-
from fuzzywuzzy import fuzz
import sys
import jieba
import csv
import pickle
print(sys.getdefaultencoding())
def load_corpus_data(filename,load = False):
    try:
        with open('stop_words.txt', 'r', encoding="utf-8") as f:
            stop_words = f.read().splitlines()
    except:
        print("加载失败")
    # 加载用户词
    jieba.load_userdict('UserDefined_words.txt')

    corpus = []
    label = []
    question = []
    answer = []
    with open(filename, 'r', encoding="utf-8") as f:
        data_corpus = csv.reader(f)
        header = next(data_corpus)
        for words in data_corpus:
            word = jieba.cut(words[1])
            tmp = ''
            for x in word:
                if x not in stop_words:
                    tmp += x
            corpus.append(tmp)
            question.append(words[1])
            label.append(words[0])
            answer.append(words[2])
    if load == True:
        with open('corpus_1233.oj','wb') as f:
            pickle.dump(corpus,f)
        with open('label_1233.oj','wb') as f:
            pickle.dump(label,f)
        with open('question_1233.oj', 'wb') as f:
            pickle.dump(question, f)
        with open('answer_1233.oj', 'wb') as f:
            pickle.dump(answer, f)
        with open('stop_words.oj', 'wb') as f:
            pickle.dump(stop_words, f)
    return corpus,label,question,answer

def Query(input_words):
    try:
        with open('stop_words.oj','rb') as f:
            stop_words = pickle.load(f)
    except:
        print ("----------stop_words加载失败---------")
    input_questions = ''
    input_words = jieba.cut(input_words)
    for x in input_words:
        if x not in stop_words:
            input_questions += x
    return input_questions

class Similarity:
    def similarity(input_questions):
        try:
            with open('corpus_1233.oj','rb') as f:
                corpus = pickle.load(f)
        except:
            print("----------corpus加载失败---------")

        try:
            with open('question_1233.oj', 'rb') as f:
                 question = pickle.load(f)
        except:
            print("----------question加载失败---------")

        try:
            with open('answer_1233.oj','rb') as f:
                answer = pickle.load(f)
        except:
            print("----------answer加载失败---------")

        text = {}
        train = []
        for key, value in enumerate(corpus):
            similarity = fuzz.ratio(input_questions, value)
            if similarity > 40:
                text[key] = similarity
        if len(text) >= 3:
            train = sorted(text.items(), key=lambda d: d[1], reverse=True)
            print("与您提的疑问相似的问题有\n")
            for i in range(3):
                print ("%d、"%(i+1),  \
                    " 问题：%s\n" % question[train[i][0]], \
                    " 答案：%s" % answer[train[i][0]])
        elif len(text) == 2:
            train = sorted(text.items(), key=lambda d: d[1], reverse=True)
            print ("与您提的疑问相似的问题有\n")
            for i in range(2):
                print ("%d、"%(i+1),  \
                    " 问题：%s\n" % question[train[i][0]], \
                    " 答案：%s" % answer[train[i][0]])
        elif len(text) == 1:
            print ("与您提的疑问相似的问题有：\n", \
                " 问题：%s" % question[text.keys()[0]], \
                " 答案：%s" % answer[text.keys()[0]])
        else:
            print ("您所提的问答无其他相似问题！")