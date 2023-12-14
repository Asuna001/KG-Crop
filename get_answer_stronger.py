from neo4j import GraphDatabase
import mysql.connector

class Get_answer:

    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "031118xyt"))
        self.index_dict = {
            0 : '病害',
            1 : '虫害',
            2 : '别称',
            3 : '学名',
            4 : '危害作物',
            5 : '研究文献',
            6 : '作者',
            7 : '关键字',
            8 : '发生规律',
            9 : '图例',
            10 : '摘要',
            11 : '期刊',
            12 : '网址',
            13 : '简介',
            14 : '病虫害',
            15 : '生活习性',
            16 : '症状',
            17 : '形态特征',
            18 : '防治方法'
        }

    def close(self):
        self.driver.close()

    def get_data(self, index, params):
        query = ''
        print(type(index))
        if type(index) == type(1):
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
                print('关键词是：' + params[0])
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
                    if len(result_list) >= 1:
                        cloudpath_value = result_list[0]  
                        query = "SELECT localpath FROM imgpath WHERE cloudpath = %s"  
                        image.execute(query, (cloudpath_value,))  
                        result1 = image.fetchone()
                        result_list[0] = '图片的本地链接是'
                        result_list.append(result1[0])
                return result_list
            
        elif type(index) == type([]):
            result_dict = []
            params_list = [params]
            # i = 0
            # print(i,index[i],params_list[i])
            # temp_result = self.get_data(index[i],params_list[i])
            # print(temp_result)

            for i in range(len(index)):
                params_list.append([])
                result_dict.append({}) 
                # for result in result_list[i]:
                print('层数是：'+ str(i) + ' 索引和关键词是：' + str(index[i]),params_list[i])
                for params in params_list[i]:
                    temp_result = self.get_data(index[i],[params])
                    for temp in  temp_result:
                        params_list[i+1].append(temp)
                    result_dict[i][params] = temp_result


            return result_dict

    def pr(self,list,index,temp,replacement):
                if index > 0:
                    # print(list[index])
                    for key,value in list[index].items():
                        # print(key,value)
                        if temp in value or temp == value:
                            ouput = self.pr(list,index-1,key,replacement)
                            # print(index,ouput)
                            if index == len(list)-1:
                                ouput += str(key) + "的" + replacement[index] + "是" + str(value).replace("[","").replace("]","")
                            else:
                                ouput += str(key) + "的" + replacement[index] + " "
                            return ouput
                elif index == 0:
                    for key,value in list[index].items():
                        # print(key,value)
                        ouput = str(key) + "的" + replacement[index] + " "
                        # print(index,ouput)
                        return ouput
                    
    def get_ans(self,index,params):
        result_dict = self.get_data(index,params)
        final_ans = []
        if len(index) > 1:
            relation_list = []
            for key in index:
                relation_list.append(self.index_dict[key]) 
            for key,value in result_dict[len(result_dict)-1].items():
                if value != []:
                    final_ans.append(self.pr(result_dict,len(result_dict)-1,value,relation_list))
        elif len(index) == 1:
            for key,value in result_dict[0].items():
                final_ans.append(str(key) + "的" + self.index_dict[index[0]]+ '是' + str(value).replace("[","").replace("]",""))
        return final_ans
    
    def get_Question(self,index,params):
        question = str(params)
        for i in index:
            question += '的' + self.index_dict[i]
        return question

if __name__ == "__main__":
    ga = Get_answer()
    index = [0]
    params = ['玉米']
    print(ga.get_ans(index,params))