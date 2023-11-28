import pandas as pd
import csv
import mysql.connector
import requests
from neo4j import GraphDatabase

# 读取三元组文件
h_r_t_name = [":start_id",":start_property","role", ":end_id",":end_property"]
h_r_t = pd.read_csv("D:\数字治理实验室\玉米病虫害图谱的三元组.csv", decimal="\t", names=h_r_t_name,encoding='gbk')

# # 读取属性为图例的对象并存入MySQL数据库中
# imagepath = []
# headers ={
#         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
#         }

# entity_h = h_r_t[[":start_id",":start_property"]]
# # print(entity_h)
# for index,row in entity_h.iterrows():
#     if row[":start_property"] == "图例":
#         r = requests.get(row[":start_id"],headers=headers)
#         f = open("D:\数字治理实验室\image\s"+str(index)+".jpg","wb")
#         f.write(r.content)
#         f.close()
#         imagepath.append((row[":start_id"],"D:\数字治理实验室\image\s"+str(index)+".jpg"))

# entity_t = h_r_t[[":end_id",":end_property"]]
# # print(entity_h)
# for index,row in entity_t.iterrows():
#     if row[":end_property"] == "图例":
#         r = requests.get(row[":end_id"],headers=headers)
#         f = open("D:\数字治理实验室\image\e"+str(index)+".jpg","wb")
#         f.write(r.content)
#         f.close()
#         imagepath.append((row[":end_id"],"D:\数字治理实验室\image\e"+str(index)+".jpg"))
# print(imagepath)


# db_image = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="123456",
#   database = "image"
# )  

# image = db_image.cursor()

# sql = """create table imgpath(
#         cloudpath varchar(100),
#         localpath varchar(100)
#         )"""
# # image.execute("drop table imgpath")
# add = "insert into imgpath (cloudpath,localpath) value (%s,%s)"
# # image.execute(sql)
# image.executemany(add,imagepath)

sql = """alter table imgpath   
        add index cloudpath_index (cloudpath)"""  # 添加索引  
# image.execute(sql)

# image.execute("select * from imgpath")
# results = image.fetchall() 
# for y in results:
#   print(y)

# 建立一个Neo4j会话
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', '031118xyt'))
with driver.session() as session:
    tx = session.begin_transaction()
    for index,item in h_r_t.iterrows():
        query = f"""
                MERGE (a:{item[":start_property"]} {{name: '{item[":start_id"]}'}})
                MERGE (b:{item[":end_property"]} {{name: '{item[":end_id"]}'}})
                MERGE (a)-[ab:{item["role"]}]->(b)
                """
        tx.run(query)
    tx.commit()  # 提交事务

print("已入库完成")
