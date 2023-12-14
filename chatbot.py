from analyze_question_stronger import AnalysisQuestion
from get_answer_stronger import Get_answer

def run(question):
    aq = AnalysisQuestion()
    ga = Get_answer()
    index, params , temp = aq.analysis_question(question)
    answers = ga.get_ans(index, params)
    return answers

if __name__ == "__main__":
    while True:
        question = input('请输入你想查询的信息：') 
        answers = run(question)
        print('答案:')
        for ans in answers:
            print(ans)
