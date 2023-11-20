import gradio as gr
from analyze_question import AnalysisQuestion
from get_answer import Get_answer

def get_response(question, feedback=None):
    aq = AnalysisQuestion()
    ga = Get_answer()
    index, params = aq.analysis_question(question)
    answers = ga.get_data(index, params)

    response_text = ""  # 默认为空字符串
    response_image = None  # 默认为None
    response_feedback = ""  # 默认为空字符串，用于反馈信息

    # 如果答案是一个图片链接数组
    if answers[0] == 'img':
        response_image = answers[1]  # 图片链接
        response_text = "答案如下图所示："  # 提示文本
    else:
        response_text = answers  # 纯文本答案

    # 检查反馈并设置反馈信息
    if feedback == "不满意":
        response_feedback = "我们会不断改进以提高准确度。"
    elif feedback == "满意":
        response_feedback = "感谢您的反馈！"

    # 返回所有响应
    print("问题已接收，内容为:", question)  # 添加调试 print 语句
    try:
        # ... 现有的代码逻辑 ...
        # 返回所有响应
        return response_text, response_image, response_feedback
    except Exception as e:
        print("发生错误:", e)  # 打印错误
        return "发生内部错误，请检查服务器日志。", None, ""  # 返回用户友好的错误消息

iface = gr.Interface(
    fn=get_response,
    inputs=[
        gr.inputs.Textbox(placeholder="请输入您的问题", label="问题"),
        gr.inputs.Radio(choices=["满意", "不满意"], label="满意度反馈", default=None, optional=True)
    ],
    outputs=[
        gr.outputs.Textbox(label="文本答案"),
        gr.outputs.Image(label="图片答案", type='filepath'),  # 指定 type 参数
        gr.outputs.Textbox(label="反馈结果")
    ]
)

# 启动 Gradio 接口
iface.launch(debug=True)  # 开启 debug 模式