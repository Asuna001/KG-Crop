import pandas as pd

disease_dict = []
title_dict = []
crop_dict = []
insect_dict = []

data = pd.read_csv("D:/数字治理实验室/玉米病虫害图谱的三元组.csv",names=['a','b','c','d','e'],encoding="gbk")

for index,item in data.iterrows():
    print(index,item)
    if item["b"] == "标题":
        title_dict.append(item["a"])
    elif item["b"] == "病害":
        disease_dict.append(item["a"])
    elif item["b"] == "作物":
        crop_dict.append(item["a"])
    elif item["b"] == "虫害":
        insect_dict.append(item["a"])

disease_dict = list(set(disease_dict))
title_dict = list(set(title_dict))
crop_dict = list(set(crop_dict))
insect_dict = list(set(insect_dict))

with open('数字治理实验室\chat-bot\word\disease.txt',mode='w+',encoding="utf-8") as f:
    for i in disease_dict:
        f.write(i+' disease'+'\n')
    f.close()
with open('数字治理实验室\chat-bot\word/title.txt',mode='w+',encoding="utf-8") as f:
    for i in title_dict:
        f.write(i+' title'+'\n')
    f.close()
with open('数字治理实验室\chat-bot\word\crop.txt',mode='w+',encoding="utf-8") as f:   
    for i in crop_dict:
        f.write(i+' crop'+'\n')
    f.close()
with open('数字治理实验室\chat-bot\word\insect.txt',mode='w+',encoding="utf-8") as f:   
    for i in insect_dict:
        f.write(i+' insect'+'\n')
    f.close()
