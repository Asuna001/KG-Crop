import json
import joblib
import numpy as np
import jieba.posseg as pseg
import jieba



class AnalysisQuestion():
    def __init__(self):
        self.vocab_path = '数字治理实验室\chat-bot\model/vocabulary.json'
        self.model_path = '数字治理实验室\chat-bot\model\clf.model'
        self.question_classification_path = '数字治理实验室\chat-bot\model\question_classification.json'
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
        jieba.load_userdict("数字治理实验室\chat-bot\word\crop.txt")
        jieba.load_userdict("数字治理实验室\chat-bot\word/title.txt")
        jieba.load_userdict("数字治理实验室\chat-bot\word\insect.txt")
        jieba.load_userdict("数字治理实验室\chat-bot\word\disease.txt") # 加载属性
        self.abstractMap = {}
        list_word = pseg.lcut(question)  # 中文分词
        abstractQuery = ''
        for item in list_word:
            word = item.word
            pos = str(item)
            print('123,',pos)
            if 'disease' in pos:  # 病害
                abstractQuery += "disease "
                self.abstractMap['disease'] = word
            elif 'title' in pos:
                abstractQuery += 'title '
                self.abstractMap['title'] = word
            elif 'crop' in pos:
                abstractQuery += "crop "
                self.abstractMap['crop'] = word
            elif 'insect' in pos:  # 病害
                abstractQuery += "insect "
                self.abstractMap['insect'] = word
            else:
                abstractQuery += word + " "
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
            # if abs_key in temp:
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
    index, params,abstr = aq.analysis_question(question)
    print(index, params)