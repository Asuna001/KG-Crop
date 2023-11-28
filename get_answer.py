from neo4j import GraphDatabase
import mysql.connector
import openai

class Get_answer:
    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "031118xyt"))

    def close(self):
        self.driver.close()

    dic = [
            '作物@的病害',
            '作物@的虫害',
            '病虫害@的别称',
            '病虫害@的危害作物',
            '病虫害@的学名',
            '病虫害@的研究文献 ',
            '文章@的作者',
            '文章@的关键字',
            '病虫害@的发生规律',
            '病虫害@的图例',
            '文章@的摘要',
            '文章@的期刊',
            '文章@的网址',
            '病虫害@的简介',
            '作物@的病虫害',
            '病虫害@的生活习性',
            '病虫害@的症状',
            '病虫害@的形态特征',
            '病虫害@的防治方法'
        ]

    def get_data(self, index, params):
        query = ''
        if index == 0:
            query = "MATCH (n:`作物`)-[:`病害`]->(m:`病害`) WHERE n.name=$name RETURN m.name"
        elif index == 1:
            query = "MATCH (n:`作物`)-[:`虫害`]->(m:`虫害`) WHERE n.name=$name RETURN m.name"
        elif index == 2:
            query = "MATCH (n:`病害`)-[:`别称`]->(m:`别称`) WHERE n.name=$name RETURN m.name UNION \
                    MATCH (n:`虫害`)-[:`别称`]->(m:`别称`) WHERE n.name=$name RETURN m.name"
        elif index == 3:
            query = "MATCH (n:`病害`)-[:`危害作物`]->(m:`作物`) WHERE n.name=$name RETURN m.name UNION \
                    MATCH (n:`虫害`)-[:`危害作物`]->(m:`作物`) WHERE n.name=$name RETURN m.name"
        elif index == 4:
            query = "MATCH (n:`病害`)-[:`学名`]->(m:`学名`) WHERE n.name=$name RETURN m.name UNION \
                    MATCH (n:`虫害`)-[:`学名`]->(m:`学名`) WHERE n.name=$name RETURN m.name"
        elif index == 5:
            query = "MATCH (n:`病害`)-[:`研究文献`]->(m:`标题`) WHERE n.name=$name RETURN m.name UNION \
                    MATCH (n:`虫害`)-[:`研究文献`]->(m:`标题`) WHERE n.name=$name RETURN m.name"
        elif index == 6:
            query = "MATCH (n:`标题`)-[:`作者`]->(m:`作者`) WHERE n.name=$name RETURN m.name"
        elif index == 7:
            query = "MATCH (n:`标题`)-[:`关键字`]->(m:`关键字`) WHERE n.name=$name RETURN m.name"
        elif index == 8:
            query = "MATCH (n:`病害`)-[:`发生规律`]->(m:`发生规律`) WHERE n.name=$name RETURN m.name UNION \
                    MATCH (n:`虫害`)-[:`发生规律`]->(m:`发生规律`) WHERE n.name=$name RETURN m.name" 
        elif index == 9:
            query = "MATCH (n:`病害`)-[:`图例`]->(m:`图例`) WHERE n.name=$name RETURN m.name UNION \
                    MATCH (n:`虫害`)-[:`图例`]->(m:`图例`) WHERE n.name=$name RETURN m.name"
        elif index == 10:
            query = "MATCH (n:`标题`)-[:`摘要`]->(m:`摘要`) WHERE n.name=$name RETURN m.name"
        elif index == 11:
            query = "MATCH (n:`标题`)-[:`期刊`]->(m:`期刊`) WHERE n.name=$name RETURN m.name"
        elif index == 12:
            query = "MATCH (n:`标题`)-[:`网址`]->(m:`网址`) WHERE n.name=$name RETURN m.name"
        elif index == 13:
            query = "MATCH (n:`标题`)-[:`简介`]->(m:`简介`) WHERE n.name=$name RETURN m.name"
        elif index == 14:
            query = "MATCH (n:`作物`)-[:`病害`]->(m:`病害`) WHERE n.name=$name RETURN m.name UNION \
                    MATCH (n:`作物`)-[:`虫害`]->(m:`虫害`) WHERE n.name=$name RETURN m.name"
        elif index == 15:
            query = "MATCH (n:`虫害`)-[:`生活习性`]->(m:`生活习性`) WHERE n.name=$name RETURN m.name UNION \
                    MATCH (n:`病害`)-[:`生活习性`]->(m:`生活习性`) WHERE n.name=$name RETURN m.name"
        elif index == 16:
            query = "MATCH (n:`虫害`)-[:`症状`]->(m:`症状`) WHERE n.name=$name RETURN m.name UNION \
                    MATCH (n:`病害`)-[:`症状`]->(m:`症状`) WHERE n.name=$name RETURN m.name"
        elif index == 17:
            query = "MATCH (n:`虫害`)-[:`形态特征`]->(m:`形态特征`) WHERE n.name=$name RETURN m.name UNION \
                    MATCH (n:`病害`)-[:`形态特征`]->(m:`形态特征`) WHERE n.name=$name RETURN m.name"
        elif index == 18:
            query = "MATCH (n:`虫害`)-[:`防治方法`]->(m:`防治方法`) WHERE n.name=$name RETURN m.name UNION \
                    MATCH (n:`病害`)-[:`防治方法`]->(m:`防治方法`) WHERE n.name=$name RETURN m.name"

        with self.driver.session() as session:
            result = session.run(query, {"name": params[0]})
            result_list = []
            for recode in result:
                result_list.append(recode['m.name'])

            if index == 9: # 图片特殊处理
                db_image = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            passwd="123456",
                            database = "image"
                            ) 
                image = db_image.cursor()
                cloudpath_value = result_list[0]  
                query = "SELECT localpath FROM imgpath WHERE cloudpath = %s"  
                image.execute(query, (cloudpath_value,))  
                result1 = image.fetchone()
                result_list[0] = "img"
                result_list.append(result1[0])
            return result_list
        
    def get_Question(self,index,params):
        question = self.dic[index].replace("@",str(params))
        return question

async def Get_newanswer(index,params):
    ga = Get_answer()
    answers = ga.get_data(index,params)
    question = ga.get_Question(index,params)
    messages = '问题是：' + question + '\n答案是：' + str(answers)
    print(messages)

    openai.api_base = "http://192.168.0.112:8000/v1"
    openai.api_key = "none"
    final_ans = ""
    for chunk in openai.ChatCompletion.create(
        model="chatglm3-6b",
        messages=[
            {"role": "system", "content": "你是一个语言润色大师，你会接受一个问题和问题的答案，然后你会重新组织语言条理清晰地用中文输出这些答案"},
            {"role": "user", "content": messages}
            ],
        stream=True
        ):
        if hasattr(chunk.choices[0].delta, "content"):
            # print(chunk.choices[0].delta.content, end="", flush=True)
            final_ans += chunk.choices[0].delta.content
        # for answer in answers:
        #     print(answer)
        yield final_ans

if __name__ == "__main__":
    print(Get_newanswer(8,['玉米大斑病']))