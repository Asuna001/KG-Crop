from analyze_question import AnalysisQuestion
from get_answer import Get_answer
import gradio as gr

def run(question):
    aq = AnalysisQuestion()
    ga = Get_answer()
    index, params , temp = aq.analysis_question(question)
    answers = ga.get_data(index, params)
    return answers

if __name__ == "__main__":
    while True:
        question = input('请输入你想查询的信息：') 
        answers = run(question)
        print('答案:')
        for ans in answers:
            print(ans)
