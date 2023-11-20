import json
import joblib
import numpy as np
import jieba.posseg as pseg
import jieba
import sys
sys.path.append('数字治理实验室\谣言知识图谱论文模型\模型\CRF')
from CRF_NER import predict

# sentences = input("请输入句子")
sentences = '我们不可忽视散播谣言的危害'
labels = predict(sentences)
labels.append("O")
for i in range(0,len(labels)):
    if labels[i] == "B-UnlawfulAct":
        b = i
    elif labels[i] == "I-UnlawfulAct" and labels[i+1] != "I-UnlawfulAct":
        sentences = sentences[:b] + "crop" + sentences[i+1:]     
    i = i + 1
print(sentences)
sentences = pseg.lcut(sentences)
print(sentences)