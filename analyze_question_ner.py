import json
import joblib
import numpy as np
import jieba.posseg as pseg
import jieba
import sys
sys.path.append('D:/vscode_python/数字治理实验室/uie-best-models')
from main import predict


class AnalysisQuestion():
    def __init__(self):
        self.vocab_path = 'D:/vscode_python/数字治理实验室/chat-bot/model/vocabulary.json'
        self.model_path = 'D:/vscode_python/数字治理实验室\chat-bot\model\clf.model'
        self.question_classification_path = 'D:/vscode_python/数字治理实验室/chat-bot/model/question_classification.json'
        self.vocab = self.load_vocab()
        self.question_class = self.load_question_classification()

    def load_vocab(self):
        with open(self.vocab_path, "r",encoding="utf-8") as f:
            vocab = json.loads(f.read())
        return vocab

    def load_question_classification(self):
        with open(self.question_classification_path, "r",encoding="utf-8") as f:
            question_classification = json.loads(f.read())
        return question_classification

    def abstract_question(self, question):
        """
        使用jieba进行分词，将关键词进行词性抽象
        :param question:
        :RETURN:
        """
        # jieba.load_userdict("数字治理实验室\chat-bot\word\crop.txt")
        # jieba.load_userdict("数字治理实验室\chat-bot\word/title.txt")
        # jieba.load_userdict("数字治理实验室\chat-bot\word\disease.txt") # 加载属性
        self.abstractMap = {}
        # labels = predict(question)
        # sentences = '我们不可忽视散播谣言的危害'
        schema = []
        ie = predict(question)
        maximum = 0
        for label in ie[0]:
            schema.append(label)
        for label in schema:
            for entity in ie[0][label]:
                temp = entity["probability"]
                if maximum < temp:
                    maximum = temp
                    mostentity = entity
                    mostlabel = label
        print(mostentity,mostlabel)
        if mostlabel == "作物":
            self.abstractMap['crop'] = mostentity['text']
            question = question[:mostentity["start"]] + 'crop' + question[mostentity["end"]+1:]
        elif mostlabel == '虫害':
            self.abstractMap['insect'] = mostentity['text']
            question = question[:mostentity["start"]] + "insect" + question[mostentity["end"]+1:]
        elif mostlabel == "病害":
            self.abstractMap['disease'] = mostentity['text']
            question = question[:mostentity["start"]] + "disease" + question[mostentity["end"]+1:]
        elif mostlabel == "标题":
            self.abstractMap['title'] = mostentity['text']
            question = question[:mostentity["start"]] + "title" + question[mostentity["end"]+1:]
        list_word = pseg.lcut(question)  # 中文分词
        abstractQuery = ''
        for item in list_word:
            word = item.word  
            abstractQuery += word + " "
        print(abstractQuery,self.abstractMap)
        return abstractQuery

    def query_classify(self, sentence):
        """
        获取模板索引
        :param sentence:
        :RETURN:
        """
        tmp = np.zeros(len(self.vocab))
        list_sentence = sentence.split(' ')
        for word in list_sentence:
            if word in self.vocab:
                tmp[int(self.vocab[word])] = 1
        clf = joblib.load(self.model_path)
        index = clf.predict(np.expand_dims(tmp, 0))[0]
        return int(index), self.question_class[index]

    def query_extention(self, temp):
        """
        模板中的实体值
        :param sentence:
        :RETURN:
        """
        params = []
        for abs_key in self.abstractMap:
            if abs_key in temp:
                params.append(self.abstractMap[abs_key])
        return params

    def analysis_question(self, question):
        print('原始句子：{}'.format(question))
        abstr = self.abstract_question(question)
        print('句子抽象化结果：{}'.format(abstr))
        index, strpatt = self.query_classify(abstr)
        print('句子对应的索引{}\t模板：{}'.format(index, strpatt))
        finalpatt = self.query_extention(strpatt)
        return index, finalpatt,abstr


if __name__ == "__main__":
    aq = AnalysisQuestion()
    question = input('请输入你想查询的信息：')
    # question = "玉米病虫害综合防治技术的摘要是玉米是我们常见农作物之一，随着种植结构调整、种植方式和气候条件的变化，玉米病虫草害的发生呈逐年加重趋势。发生的病害主要有：玉米粗缩病、苗枯病、玉米褐斑病、玉米大小斑病、玉米顶腐病、玉米茎基腐病和玉米青枯病等，玉米虫害主要有：玉米蓟马、玉米螟、棉铃虫、粘虫等虫害。"
    # labels = predict(question)  
    index, params,abstr = aq.analysis_question(question)
    print(index, params)
    # schema = []
    # ie = predict(question)
    # maximum = 0
    # for label in ie[0]:
    #     schema.append(label)
    # for label in schema:
    #     for entity in ie[0][label]:
    #         temp = entity["probability"]
    #         if maximum < temp:
    #             maximum = temp
    #             mostentity = entity
    #             mostlabel = label
    # print(mostentity,mostlabel)
    # print(predict(question))