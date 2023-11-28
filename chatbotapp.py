import gradio as gr
from analyze_question import AnalysisQuestion
from get_answer import Get_answer,Get_newanswer
import openai

async def greet(name):
    ga = Get_answer()
    answers = ga.get_data(8,['玉米大斑病'])
    question = ga.get_Question(8,['玉米大斑病'])
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
    # return 8,['玉米大斑病']


with gr.Blocks() as demo:
    index = 0
    param = []
    with gr.Row():
        with gr.Column():
            user_input = gr.Text(label="请输入您的问题")
            match_answer = gr.Button(value="获取答案")
        with gr.Column():
            result = gr.Text(label="匹配到的答案如下：")
    match_answer.click(fn=greet,inputs=[user_input],outputs=[result])
    # .then(fn=hide,outputs=[user_evaluate,upload_evaluate])
    # # user_evaluate.change(fn=feedback,inputs=[user_evaluate])
    # upload_evaluate.click(fn=load_evaluate,inputs=[user_evaluate],outputs=[user_evaluate,upload_evaluate])

# iface = gr.Interface(
#     fn=greet,
#     inputs=gr.Textbox(placeholder="请输入你想查询的信息："),
#     outputs=["text"] )

demo.queue().launch()