from analyze_question import AnalysisQuestion
from get_answer import Get_answer
import gradio as gr

if __name__ == "__main__":
    aq = AnalysisQuestion()
    ga = Get_answer()
    while True:
        question = input('请输入你想查询的信息：') 
        index, params = aq.analysis_question(question)
        answers = ga.get_data(index, params)
        print('答案:')
        for ans in answers:
            print(ans)
