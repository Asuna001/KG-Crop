from neo4j import GraphDatabase
import mysql.connector

class Get_answer:
    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "031118xyt"))

    def close(self):
        self.driver.close()

    def get_data(self, index, params):
        query = ''
        if index == 0:
            query = "MATCH (n:`作物`)-[:`病害`]->(m:`病害`) WHERE n.name=$name RETURN m.name"
        elif index == 1:
            query = "MATCH (n:`作物`)-[:`虫害`]->(m:`虫害`) WHERE n.name=$name RETURN m.name"
        elif index == 2:
            query = "MATCH (n:`病害`)-[:`别称`]->(m:`别称`) WHERE n.name='玉米异跗萤叶甲' RETURN m.name UNION \
                    MATCH (n:`虫害`)-[:`别称`]->(m:`别称`) WHERE n.name='玉米异跗萤叶甲' RETURN m.name"
        elif index == 3:
            query = "MATCH (n:`病害`)-[:`危害作物`]->(m:`作物`) WHERE n.name=$name RETURN m.name"
        elif index == 4:
            query = "MATCH (n:`病害`)-[:`学名`]->(m:`学名`) WHERE n.name=$name RETURN m.name UNION \
                    MATCH (n:`虫害`)-[:`学名`]->(m:`学名`) WHERE n.name=$name RETURN m.name"
        elif index == 5:
            query = "MATCH (n:`病害`)-[:`研究文献`]->(m:`标题`) WHERE n.name=$name RETURN m.name"
        elif index == 6:
            query = "MATCH (n:`标题`)-[:`作者`]->(m:`作者`) WHERE n.name=$name RETURN m.name"
        elif index == 7:
            query = "MATCH (n:`标题`)-[:`关键字`]->(m:`关键字`) WHERE n.name=$name RETURN m.name"
        elif index == 8:
            query = "MATCH (n:`病害`)-[:`发生规律`]->(m:`发生规律`) WHERE n.name=$name RETURN m.name"
        elif index == 9:
            query = "MATCH (n:`病害`)-[:`图例`]->(m:`图例`) WHERE n.name=$name RETURN m.name"
        elif index == 10:
            query = "MATCH (n:`标题`)-[:`摘要`]->(m:`摘要`) WHERE n.name=$name RETURN m.name"
        elif index == 11:
            query = "MATCH (n:`标题`)-[:`期刊`]->(m:`期刊`) WHERE n.name=$name RETURN m.name"
        elif index == 12:
            query = "MATCH (n:`标题`)-[:`网址`]->(m:`网址`) WHERE n.name=$name RETURN m.name"
        elif index == 13:
            query = "MATCH (n:`标题`)-[:`简介`]->(m:`简介`) WHERE n.name=$name RETURN m.name"

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

if __name__ == "__main__":
    ga = Get_answer()
    answers = ga.get_data(2, ['玉米大斑病'])
    for answer in answers:
        print(answer)
    ga.close()
