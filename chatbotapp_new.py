import gradio as gr
from analyze_question import AnalysisQuestion
from get_answer import Get_answer

user_question = ""
b=False

data_path = [
    "数字治理实验室\chat-bot\data_train\【0】病害.txt",
    "数字治理实验室\chat-bot\data_train\【1】虫害.txt",
    "数字治理实验室\chat-bot\data_train\【2】别称.txt",
    "数字治理实验室\chat-bot\data_train\【3】危害作物.txt",
    "数字治理实验室\chat-bot\data_train\【4】学名.txt",
    "数字治理实验室\chat-bot\data_train\【5】研究文献.txt",
    "数字治理实验室\chat-bot\data_train\【6】作者.txt",
    "数字治理实验室\chat-bot\data_train\【7】关键字.txt",
    "数字治理实验室\chat-bot\data_train\【8】发生规律.txt",
    "数字治理实验室\chat-bot\data_train\【9】图例.txt",
    "数字治理实验室\chat-bot\data_train\【10】摘要.txt",
    "数字治理实验室\chat-bot\data_train\【11】期刊.txt",
    "数字治理实验室\chat-bot\data_train\【12】网址.txt",
    "数字治理实验室\chat-bot\data_train\【13】简介.txt"
]

index = 0

def get_answer(question):
    global user_question,index
    aq = AnalysisQuestion()
    ga = Get_answer()
    index, params,abstr = aq.analysis_question(question)
    print(abstr.replace(" ", ""))
    user_question = abstr.replace(" ", "")
    answers = ga.get_data(index, params)
    if answers[0] == 'img':
        return "图片如下",gr.Image(value=answers[1])
    else:
        return gr.Textbox(value=answers),None

def hide():
    global b 
    b = True
    return gr.Radio(choices=["满意","不满意"],visible=b),gr.Button(value="确认提交",visible=b)

def feedback(e):
    print(e)
    return 

def load_evaluate(e):
    global user_question,b
    b = not b
    if e == "满意":
        global index,data_path
        print(user_question,index)
        try:
            with open(data_path[index], 'r', encoding='utf-8') as file:
                lines = file.readlines()
                lines = [line.strip() for line in lines]
                print(lines)
                if user_question in lines:
                    print("问题已经存在")
                else:
                    with open(data_path[index], 'a', encoding='utf-8') as file:
                        file.write("\n" + user_question)
        except FileNotFoundError:
            print("文件不存在")
        
    else:
        print("用户不满意")
    return gr.Radio(choices=["满意","不满意"],visible=b,value="不满意"), gr.Button(value="确认提交",visible=b)

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            user_input = gr.Text(label="请输入您的问题")
            match_answer = gr.Button(value="获取答案")
        with gr.Column():
            result = gr.Text(label="匹配到的答案如下：")
            result_img = gr.Image(label="图片如下")
            user_evaluate = gr.Radio(choices=["满意","不满意"],visible=b,value="不满意")
            upload_evaluate = gr.Button(value="确认提交",visible=b)
    match_answer.click(fn=get_answer,inputs=[user_input],outputs=[result,result_img]).then(fn=hide,outputs=[user_evaluate,upload_evaluate])
    # user_evaluate.change(fn=feedback,inputs=[user_evaluate])
    upload_evaluate.click(fn=load_evaluate,inputs=[user_evaluate],outputs=[user_evaluate,upload_evaluate])

demo.launch()