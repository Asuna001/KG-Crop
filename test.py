import gradio as gr
from analyze_question import AnalysisQuestion
from get_answer import Get_answer


def greet(name):
    aq = AnalysisQuestion()
    ga = Get_answer()
    while True:
        question = name 
        index, params = aq.analysis_question(question)
        answers = ga.get_data(index, params)
        if answers[0] == 'img':
            return "图片如下",gr.Image(value=answers[1])
        else:
            return gr.Textbox(value=answers),None
         
iface = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(placeholder="请输入你想查询的信息："),
    outputs=["text","image"] )

iface.launch()

