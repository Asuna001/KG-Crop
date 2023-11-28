import os
import re
import json
import jieba
import joblib
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier



class GenerQuestionClassification():
    def __init__(self):
        self.question_classification_path = "D:/vscode_python\数字治理实验室\chat-bot\model\question_classification.json"
        if not os.path.isfile(self.question_classification_path):
            self.save_vocab()

    def save_vocab(self):
        '''这部分 dict 需要和训练数据顺序对应'''
        dic = {
                '0': 'crop 病害',
                '1': 'crop 虫害',
                '2': 'pest 别称',
                '3': 'pest 危害作物',
                '4': 'pest 学名',
                '5': 'pest 研究文献 ',
                '6': 'title 作者',
                '7': 'title 关键字',
                '8': 'pest 发生规律',
                '9': 'pest 图例',
                '10': 'title 摘要',
                '11': 'title 期刊',
                '12': 'title 网址',
                '13': 'pest 简介',
                '14': 'crop 病虫害',
                '15': 'pest 生活习性',
                '16': 'pest 症状',
                '17': 'pest 形态特征',
                '18': 'pest 防治方法'
               }
        with open(self.question_classification_path, 'w',encoding="utf8") as f:
            json.dump(dic, f, ensure_ascii=False)  # 会在目录下生成一个*.json的文件，文件内容是dict数据转成的json数据  ensure_ascii=False
        print("save question classification success...")


class GenerVocab():
    '''生成所有训练数据的vocab文件, 使用模型的时候需要. 变更数据的时候需要重新生成.'''
    def __init__(self):
        self.data_path = "D:/vscode_python\数字治理实验室\chat-bot\data_train"
        self.save_vocab_path = "D:/vscode_python\数字治理实验室\chat-bot\model/vocabulary.json"
        if not os.path.isfile(self.save_vocab_path):
            self.save_vocab()

    def cut_word(self, file_path):
        result_list = []
        with open(file_path, "r",encoding="utf-8") as temp_f:
            for sentence in temp_f.readlines():
                sentence = sentence.strip()
                temp = jieba.lcut(sentence)
                result_list += temp
        return result_list

    def get_all_word(self):
        all_word_list = []
        for path in os.listdir(self.data_path):
            file_path = os.path.join(self.data_path, path)
            result_word_list = self.cut_word(file_path)
            all_word_list += result_word_list
        all_word_set = set(all_word_list)
        result_dict = {}
        for index, cont in enumerate(all_word_set):
            result_dict[cont] = index
        return result_dict

    def save_vocab(self):
        dic = self.get_all_word()
        with open(self.save_vocab_path, 'w',encoding="utf-8") as f:
            json.dump(dic, f, ensure_ascii=False)  # 会在目录下生成一个*.json的文件，文件内容是dict数据转成的json数据  ensure_ascii=False
        print("save vocab success...")


class Trainer(GenerVocab):
    def __init__(self):
        super().__init__()
        self.vocab = self.load_vocab()

    def load_vocab(self):
        with open(self.save_vocab_path, "r",encoding="utf-8") as f:
            vocab = json.loads(f.read())
        return vocab

    def load_data(self):
        X = []
        Y = []
        list_file = os.listdir(self.data_path)
        for file_name in list_file:
            file_path = os.path.join(self.data_path, file_name)
            result = re.match('【[0-9]*】', file_name).span()
            start = result[0]
            end = result[1]
            with open(file_path, 'r', encoding='utf-8')as fread:
                for line in fread:
                    tmp = np.zeros(len(self.vocab))
                    Y.append(file_name[start + 1:end - 1])  # label
                    list_sentence = jieba.lcut(line.rstrip())
                    for word in list_sentence:
                        if word in self.vocab:
                            tmp[int(self.vocab[word])] = 1
                    X.append(tmp)
        return X, Y

    def train(self):
        X, Y = self.load_data()
        clf = RandomForestClassifier(n_estimators=100).fit(X,Y)
        # clf = GaussianNB().fit(X, Y)
        joblib.dump(clf, 'D:/vscode_python\数字治理实验室\chat-bot\model\clf.model')
        # 在模型训练之后添加以下代码
        y_pred = clf.predict(X)  # 使用训练好的模型预测训练数据
        accuracy = accuracy_score(Y, y_pred)  # 计算预测准确率
        print("Accuracy: {:.2f}%".format(accuracy * 100))

if __name__ == "__main__":
    gqc = GenerQuestionClassification()
    t = Trainer()
    t.train()
