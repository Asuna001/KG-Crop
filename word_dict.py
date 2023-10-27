import pandas as pd

pest_dict = []
title_dict = []
crop_dict = []

data = pd.read_csv("D:/vscode_python\数字治理实验室\chat-bot\data\data.csv")

for index,item in data.iterrows():
    print(index,item)
    if item["b"] == "标题":
        title_dict.append(item["a"])
    elif item["b"] == "病害":
        pest_dict.append(item["a"])
    elif item["b"] == "作物":
        crop_dict.append(item["a"])

pest_dict = list(set(pest_dict))
title_dict = list(set(title_dict))
crop_dict = list(set(crop_dict))

with open('数字治理实验室\chat-bot\word\pest.txt',mode='w+',encoding="utf-8") as f:
    for i in pest_dict:
        f.write(i+' pest'+'\n')
    f.close()
with open('数字治理实验室\chat-bot\word/title.txt',mode='w+',encoding="utf-8") as f:
    for i in title_dict:
        f.write(i+' title'+'\n')
    f.close()
with open('数字治理实验室\chat-bot\word\crop.txt',mode='w+',encoding="utf-8") as f:   
    for i in crop_dict:
        f.write(i+' crop'+'\n')
    f.close()
