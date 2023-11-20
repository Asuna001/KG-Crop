import tkinter as tk
from tkinter import simpledialog, messagebox, Label
from analyze_question_ner import AnalysisQuestion
from get_answer import Get_answer
from PIL import Image, ImageTk
import requests
from io import BytesIO

def submit_question():
    question = question_entry.get()
    index, params = aq.analysis_question(question)
    answers = ga.get_data(2, ['玉米大斑病'])
    
    # Clear the previous answer and satisfaction survey
    answer_label.config(text="")
    satisfaction_panel.pack_forget()

    if answers and answers[0] == 'img':
        # Display an image
        response = requests.get(answers[1])
        img = Image.open(BytesIO(response.content))
        img = img.resize((250, 250), Image.ANTIALIAS)  # Resize the image
        img = ImageTk.PhotoImage(img)
        answer_label.img = img  # Keep a reference, prevent GC
        answer_label.config(image=img)
    else:
        # Display text
        answer_label.config(text=answers)

    # Show the satisfaction survey
    satisfaction_panel.pack()
    
def submit_satisfaction():
    satisfaction = satisfaction_var.get()
    if satisfaction == "unsatisfied":
        messagebox.showinfo("Feedback", "我们会不断改进以提高准确度。")
    else:
        messagebox.showinfo("Feedback", "感谢您的反馈！")
    # Clear after submitting feedback
    satisfaction_var.set(None)  

# Initialize analysis and answer classes
aq = AnalysisQuestion()
ga = Get_answer()

root = tk.Tk()
root.title("Question Answer Interface")

# Question Entry
question_entry = tk.Entry(root, width=50)
question_entry.pack()

# Submit Question Button
submit_button = tk.Button(root, text="Submit Question", command=submit_question)
submit_button.pack()

# Answer Display
answer_label = Label(root)  # Used for both text and images
answer_label.pack()

# Satisfaction Survey
satisfaction_panel = tk.Frame(root)  
satisfaction_var = tk.StringVar(value=None)  # Holds satisfaction response
satisfied_rb = tk.Radiobutton(satisfaction_panel, text="满意", variable=satisfaction_var, value="satisfied")
unsatisfied_rb = tk.Radiobutton(satisfaction_panel, text="不满意", variable=satisfaction_var, value="unsatisfied")
submit_satisfaction_button = tk.Button(satisfaction_panel, text="Submit Feedback", command=submit_satisfaction)
satisfied_rb.pack(side=tk.LEFT)
unsatisfied_rb.pack(side=tk.LEFT)
submit_satisfaction_button.pack(side=tk.LEFT)

# Start the GUI
root.mainloop()