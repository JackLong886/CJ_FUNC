import tkinter as tk
from tkinter import Label, Entry, Button, messagebox

def submit():
    try:
        res_value = int(res_entry.get())
        output_path_value = output_path_entry.get()
        # 在这里你可以使用res_value和output_path_value进行你的操作
        # 例如，打印参数值
        print("res:", res_value)
        print("output_path:", output_path_value)
        # 这里可以添加更多你想要的操作
    except ValueError:
        messagebox.showerror("Error", "Invalid input for 'res'. Please enter a valid integer.")

# 创建主窗口
root = tk.Tk()
root.title("Parameter Input")

# 添加标签和输入框
res_label = Label(root, text="res:")
res_label.pack()

res_entry = Entry(root)
res_entry.pack()

output_path_label = Label(root, text="output_path:")
output_path_label.pack()

output_path_entry = Entry(root)
output_path_entry.pack()

# 添加提交按钮
submit_button = Button(root, text="Submit", command=submit)
submit_button.pack()

# 运行主循环
root.mainloop()
