# KG-Crop
- [介绍](#介绍)
- [项目依赖](#项目依赖)
- [实现过程](#实现过程)
  - [模型训练](#模型训练)
  - [意图抽取](#意图抽取)
  - [获取答案](#获取答案)
  - [功能展示](#功能展示)
## 介绍
基于知识图谱的问答系统,适合搭载小图谱,搭载大图谱的表现未知
## 项目依赖
运行以下代码以安装项目依赖  
```
pip install requirements.txt
```
如果需要运行功能展示,额外需要  
```
pip install openai
```
## 实现过程
- [模型训练](#模型训练)
- [意图抽取](#意图抽取)
- [获取答案](#获取答案)
- [功能展示](#功能展示)
### 模型训练
[train.py](train.py)  
建立与训练数据对应的dic模板,并生成question_classification.json文件;加载train?_data中的训练数据文件,利用中文分词生成vocabulary词典文件;最后加载两份文件利用随机森林分类器生成clf模型文件
### 意图抽取
[analyze_question.py](analyze_question.py)  
输入问题,与预加载的clf模型进行匹配,返回问题的模板索引,关键词,模板内容
### 获取答案
[get_answer.py](get_answer.py)  
在通过意图抽取获取到意图模板和关键词后，连接图数据库，按模板将关键词输入match语句匹配答案，并返回匹配到的答案列表；如果模板为询问图片，则额外连接MySQL数据库用匹配到的链接索引本地图片链接，并返回固定格式列表，便于后续展示
### 功能展示
运行[chatbotapp_new.py](chatbotapp_new.py)后，进入本地服务器即可进行问答  
通过一个Text组件获取用户输入，调用[analyze_question.py](analyze_question.py)中的analyze_question()方法获取用户输入模板以及关键词，再将模板索引和关键词送入[get_answer.py](get_answer.py) 的get_answer()方法换取答案列表，最后连接openai调用openai.ChatCompletion.create()方法来使答案读起来更加通顺,最终以流式输出的方式把答案返回给一个异步的Text组件  
在获取答案的同时,也把analyze_question()方法获取到的模板的内容并存入全局变量中  
特别的,如果得到的模板索引是9(对应询问图例),则跳过调用openai环节,直接获取图片本地链接并返回给Image组件展示(在正常情况下处于未启用状态)  
在加载完答案后，修改反馈模块的visible属性,通过展示出来的Radio组件和Button组件,让用户可以选择对答案是否感到满意，感到满意则会将该次问题的模板内容录入训练库以增加准确率  

