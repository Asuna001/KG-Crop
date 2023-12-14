import gradio as gr
from analyze_question_stronger import AnalysisQuestion
from get_answer_stronger import Get_answer
import openai

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
    "数字治理实验室\chat-bot\data_train\【13】简介.txt",
    '数字治理实验室\chat-bot\data_train\【14】病虫害.txt',
    '数字治理实验室\chat-bot\data_train\【15】生活习性.txt',
    '数字治理实验室\chat-bot\data_train\【16】症状.txt',
    '数字治理实验室\chat-bot\data_train\【17】形态特征.txt',
    '数字治理实验室\chat-bot\data_train\【18】防治方法.txt'
]

index = 0

async def get_answer(question):
    global user_question,index
    aq = AnalysisQuestion()
    ga = Get_answer()
    index, params,abstr = aq.analysis_question(question)
    print(abstr.replace(" ", ""))
    user_question = abstr.replace(" ", "")
    answers = ga.get_ans(index, params)
    question = ga.get_Question(index, params)
    messages = '问题是：' + question + '\n答案是：' + str(answers)
    print(messages)
    openai.api_base = "http://192.168.0.112:8000/v1"
    openai.api_key = "none"
    final_ans = ""
    message = "问题是：病虫害['玉米铁甲']的生活习性\n \
               答案是：['春天气温16℃以上时，成虫开始活动，一般4月上中旬成虫进入盛发期，卵产在嫩叶组织里，幼虫孵化后即在叶内咬食叶肉直至化蛹，幼虫期16～23天。']"
    answer = " 玉米铁甲是一种常见的病虫害，其生活习性如下：在春天气温达到16℃以上时，成虫会开始活动。一般来说，4月份上中旬是成虫的盛发期。此时，卵会在嫩叶组织里产出，随后，幼虫会孵化并立即在叶内咬食叶肉。在幼虫期，大约需要16～23天的时间。"
    if index == 9:
        yield "图片如下",gr.Image(value=answers[1],visible=True)
    else :
        for chunk in openai.ChatCompletion.create(
            model="chatglm3-6b",
            messages=[
                {"role": "system", "content": "你是一个语言润色大师，你会接受一个问题和问题的答案数据，然后你会利用答案中的数据重新组织语言用中文输出这些答案"},
                {"role": "user", "content": message},
                {"role": "assistant", "content": answer},
                {"role": "user", "content": messages}
                ],
            stream=True,
            temperature=0.5,
            ):
            if hasattr(chunk.choices[0].delta, "content"):
                # print(chunk.choices[0].delta.content, end="", flush=True)
                final_ans += chunk.choices[0].delta.content
            # for answer in answers:
            #     print(answer)
            yield final_ans , gr.Image(label="图片如下",visible=False)

def get_answer_list(question):
    global user_question,index,b
    aq = AnalysisQuestion()
    ga = Get_answer()
    index, params,abstr = aq.analysis_question(question)
    print(abstr.replace(" ", ""))
    user_question = abstr.replace(" ", "")
    answers = ga.get_ans(index, params)
    question = ga.get_Question(index, params)
    b = (len(index)==1)
    if index == 9:
        return "见下图",gr.Image(value=answers[1],visible=True)
    else:
        return answers , gr.Image(label="图片如下",visible=False)

def hide():
    global b 
    return gr.Radio(label="你对回答的准确度是否满意",choices=["满意","不满意"],visible=b),gr.Button(value="确认提交",visible=b)

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
            with open(data_path[index[0]], 'r', encoding='utf-8') as file:
                lines = file.readlines()
                lines = [line.strip() for line in lines]
                print(lines)
                if user_question in lines:
                    print("问题已经存在")
                else:
                    with open(data_path[index[0]], 'a', encoding='utf-8') as file:
                        file.write("\n" + user_question)
                    print("问题存储成功")
        except FileNotFoundError:
            print("文件不存在")
        
    else:
        print("用户不满意")
    return gr.Radio(label="你对回答的准确度是否满意",choices=["满意","不满意"],visible=b,value="不满意"), gr.Button(value="确认提交",visible=b)

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            user_input = gr.Text(label="请输入您的问题")
            match_answer = gr.Button(value="获取答案")
            match_answer_list = gr.Button(value="获取答案数据")
        with gr.Column():
            result = gr.Text(label="匹配到的答案如下：")
            result_img = gr.Image(label="图片如下",visible=False)
            user_evaluate = gr.Radio(label="你对回答的准确度是否满意",choices=["满意","不满意"],visible=b,value="不满意")
            upload_evaluate = gr.Button(value="确认提交",visible=b)
    match_answer.click(fn=get_answer,inputs=[user_input],outputs=[result,result_img]) \
    .then(fn=hide,outputs=[user_evaluate,upload_evaluate])
    match_answer_list.click(fn=get_answer_list,inputs=[user_input],outputs=[result,result_img]) \
    .then(fn=hide,outputs=[user_evaluate,upload_evaluate])
    # user_evaluate.change(fn=feedback,inputs=[user_evaluate])
    upload_evaluate.click(fn=load_evaluate,inputs=[user_evaluate],outputs=[user_evaluate,upload_evaluate])

demo.queue().launch()