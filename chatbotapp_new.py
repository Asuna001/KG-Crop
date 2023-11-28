import gradio as gr
from analyze_question import AnalysisQuestion
from get_answer import Get_answer
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
    answers = ga.get_data(index, params)
    question = ga.get_Question(index, params)
    messages = '问题是：' + question + '\n答案是：' + str(answers)
    print(messages)
    openai.api_base = "http://192.168.0.112:8000/v1"
    openai.api_key = "none"
    final_ans = ""
    message = "问题是：作物['玉米']的病害\n \
            答案是：['玉米平脐蠕孢茎基腐病', '玉米镰刀菌苗枯病', '玉米矮花叶病', '玉米假黑粉病', '玉米炭疽病', '玉米纹枯病', '玉米弯孢霉叶斑病', '玉米轮纹斑病', '玉米全蚀病', '玉米灰斑病', '玉米茎腐病', '玉米丝黑穗病', '玉米斑枯病', '玉米赤霉病', '玉米细菌性茎腐病', '玉米小斑病', '玉米链格孢菌叶枯病', '玉米秃尖', '玉米细菌性条纹病', '玉米锈病', '玉米眼斑病', '玉米褐斑病', '玉米条纹矮缩病', '玉米种子霉烂', '玉米疯顶病', '玉米黑粉病', '玉米圆斑病', '玉米叶鞘紫斑病', '玉米立枯丝核菌根腐病', '玉米细菌萎蔫病', '玉米大斑病', '玉米粗缩病', '玉米干腐病', '玉米花期不协调', '玉米霜霉病']"
    answer = " 以下是关于作物玉米常见病害：\n \
        1. 玉米平脐蠕孢茎基腐病\n  \
        2. 玉米镰刀菌苗枯病\n  \
        3. 玉米矮花叶病\n  \
        4. 玉米假黑粉病\n  \
        5. 玉米炭疽病\n  \
        6. 玉米纹枯病\n  \
        7. 玉米弯孢霉叶斑病\n  \
        8. 玉米轮纹斑病\n  \
        9. 玉米全蚀病\n  \
        10. 玉米灰斑病\n  \
        11. 玉米茎腐病\n  \
        12. 玉米丝黑穗病\n  \
        13. 玉米斑枯病\n  \
        14. 玉米赤霉病\n  \
        15. 玉米细菌性茎腐病\n  \
        16. 玉米小斑病\n  \
        17. 玉米链格孢菌叶枯病\n  \
        18. 玉米秃尖\n  \
        19. 玉米细菌性条纹病\n  \
        20. 玉米锈病\n  \
        21. 玉米眼斑病\n  \
        22. 玉米褐斑病\n  \
        23. 玉米条纹矮缩病\n  \
        24. 玉米种子霉烂\n  \
        25. 玉米疯顶病\n  \
        26. 玉米黑粉病\n  \
        27. 玉米圆斑病\n  \
        28. 玉米叶鞘紫斑病\n  \
        29. 玉米立枯丝核菌根腐病\n  \
        30. 玉米细菌萎荏病\n  \
        31. 玉米大斑病\n  \
        32. 玉米粗缩病\n  \
        33. 玉米干腐病\n  \
        34. 玉米花期不协调 \
        35. 玉米霜霉病  "
    for chunk in openai.ChatCompletion.create(
        model="chatglm3-6b",
        messages=[
            {"role": "system", "content": "你是一个语言润色大师，你会接受一个问题和问题的答案，然后你会重新组织语言条理清晰地用中文输出这些答案"},
            {"role": "user", "content": message},
            {"role": "assistant", "content": answer},
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
                    print("问题存储成功")
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
            # result_img = gr.Image(label="图片如下")
            user_evaluate = gr.Radio(choices=["满意","不满意"],visible=b,value="不满意")
            upload_evaluate = gr.Button(value="确认提交",visible=b)
    match_answer.click(fn=get_answer,inputs=[user_input],outputs=[result]).then(fn=hide,outputs=[user_evaluate,upload_evaluate])
    # user_evaluate.change(fn=feedback,inputs=[user_evaluate])
    upload_evaluate.click(fn=load_evaluate,inputs=[user_evaluate],outputs=[user_evaluate,upload_evaluate])

demo.queue().launch()