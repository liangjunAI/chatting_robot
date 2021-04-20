# Intelligent Answer System
本方案根据自己制作的语料库，基于sklearn训练分类模型和模糊匹配方法实现一个简易的智能问答机器人
具体方案思路可参考博客https://blog.csdn.net/qq_26535271/article/details/100748210

环境：
python==3.6.5

pandas

scipy

jieba

fuzzywuzzy

scikit_learn

数据介绍：
#stop_words.txt 停用词表

#UserDefined_words.txt 新增分词

#greeting.csv 娱乐聊天语料库

#znwd_corpus.csv 用于分类训练语料库

#znwd_label_url.csv 类别映射标签

#znwd_1233.csv 模糊匹配语料库

步骤
1.下载工程：

git clone https://github.com/liangjunAI/chatting_robot.git

2.由于工程环境版本不同需重新序列化数据及模型训练后文件得到相关.oj结尾的文件

python znwd_new.py

3.运行demo开始智能问答聊天

python run_main.py


4.创建属于自己的语料库，可以从上述数据介绍中进行修改/新增自己的语料库

效果：

![20190911203850153](https://user-images.githubusercontent.com/33650087/114993959-e22d4000-9ece-11eb-90e5-845026126c70.png)


