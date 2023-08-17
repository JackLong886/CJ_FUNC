from nicegui import ui
import tkinter as tk
from tkinter import filedialog
from functools import partial
from datetime import datetime

root = tk.Tk()
root.withdraw()


class Para:
    def __init__(self):
        self.img_list = None

    def print_members(self):
        for member_name, member_value in vars(self).items():
            print(f"{member_name}: {member_value}")

    def check(self):
        ui.notify(f'check')
        self.print_members()


def run_tk_filedialog(para_class):
    root.wm_attributes("-topmost", 1)
    file_paths = filedialog.askopenfilenames()
    root.wm_attributes("-topmost", 0)
    para_class.img_list = []
    message = 'you have selected files:\n'
    for file_path in file_paths:
        para_class.img_list.append(file_path)
        message += file_path
        message += '\n'
    ui.chat_message(message, name='Fast Img Robot', stamp=f'{datetime.now():%X}', avatar='https://robohash.org/ui')


para = Para()
my_btn = ui.button("pick", on_click=partial(run_tk_filedialog, para))
my_btn2 = ui.button("check", on_click=para.check)
ui.run()
