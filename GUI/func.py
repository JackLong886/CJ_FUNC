from nicegui import ui
import os
import tkinter as tk
from tkinter import filedialog


class TK_selector:
    def __init__(self):
        self.file_paths = []

    def __call__(self, *args, **kwargs):
        self.root = tk.Tk()
        self.root.title("File Order Adjuster")
        self.root.geometry("400x400")  # 设置窗口大小
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill=tk.BOTH, expand=True)  # 使用fill和expand来填充窗口并扩展

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        move_up_button = tk.Button(self.root, text="Move Up", command=self.move_up)
        move_up_button.pack(side=tk.LEFT)

        move_down_button = tk.Button(self.root, text="Move Down", command=self.move_down)
        move_down_button.pack(side=tk.LEFT)

        remove_files_button = tk.Button(self.root, text="Delete Files", command=self.delete_file)
        remove_files_button.pack(side=tk.LEFT)

        select_files_button = tk.Button(self.root, text="Select Files", command=self.run_tk_filedialog)
        select_files_button.pack(side=tk.LEFT)

        print_files_button = tk.Button(self.root, text="Print Files", command=self.print_listbox)
        print_files_button.pack(side=tk.RIGHT)

        self.root.mainloop()
        return self.file_paths

    def delete_file(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.file_paths.remove(self.file_paths[index])
            self.update_listbox()

    def move_up(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if index > 0:
                self.file_paths.insert(index - 1, self.file_paths.pop(index))
                self.update_listbox()

    def move_down(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if index < len(self.file_paths) - 1:
                self.file_paths.insert(index + 1, self.file_paths.pop(index))
                self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for path in self.file_paths:
            self.listbox.insert(tk.END, path)

    def print_listbox(self):
        if len(self.file_paths) == 0:
            return []
        print('*' * 60)
        for path in self.file_paths:
            print(path)
        print('*' * 60)
        self.update_listbox()
        return self.file_paths

    def run_tk_filedialog(self):
        self.root.wm_attributes("-topmost", 1)
        selected_paths = filedialog.askopenfilenames()
        self.file_paths += list(selected_paths)
        self.root.wm_attributes("-topmost", 0)
        self.update_listbox()


class PansharpParam:
    def __init__(self):
        self.program_progress = 0.15
        self.input_list = []
        self.output_list = []
        self.pan_method = 'WG'
        self.if_build_overview = False
        self.ratio = 10
        self.winsize = 256
        self.output_dir = r'D:\龙超俊的文件夹'

        self.input_img_selector = None

    def set_if_build_overview(self):
        self.if_build_overview = True

    def print_members(self):
        for member_name, member_value in vars(self).items():
            print(f"{member_name}: {member_value}")

    def select_input_img(self):
        if not self.input_img_selector:
            self.input_img_selector = TK_selector()
        self.input_list = self.input_img_selector()

    def set_output_dir(self, x):
        self.output_dir = x.value
        self.set_output()

    def set_output(self):
        for i in self.input_list:
            self.output_list.append(os.path.join(self.output_dir, os.path.basename(i)))

    def parse_input(self, x):
        splitted_list = x.value.split('\n')
        for i in splitted_list:
            self.input_list.append(i)

    def run(self):
        if not self.output_list:
            self.set_output()
        ui.notify(f'run !!!')
        self.print_members()


class CloudRemovalParam:
    def __init__(self):
        self.program_progress = 'coming soon'
        self.img_list = []
        self.target_list = []
        self.source_list = []
        self.valid_list = []
        self.cloud_list = []
        self.rem_output_list = []
        self.color_trans = False
        self.target_num = 1
        self.if_build_overview = False
        self.ratio = 10
        self.win_size = 256
        self.output_dir = r'D:\龙超俊的文件夹'
        self.res = 2
        self.rem_union_path = []
        self.work_dir = 'workspace'
        self.rem_cost_time = 'rem_cost_time'
        self.rem_message = 'rem_message'

        self.target_img_selector = None
        self.source_img_selector = None
        self.valid_shp_selector = None
        self.cloud_shp_selector = None

    def set_if_build_overview(self):
        self.if_build_overview = True

    def set_color_trans(self):
        self.color_trans = True

    def print_members(self):
        for member_name, member_value in vars(self).items():
            print(f"{member_name}: {member_value}")

    def set_output(self):
        for i in self.img_list:
            self.rem_output_list.append(os.path.join(self.output_dir, os.path.basename(i)))

    def select_input_target_img(self):
        if not self.target_img_selector:
            self.target_img_selector = TK_selector()
        self.target_list = self.target_img_selector()

    def select_input_source_img(self):
        if not self.source_img_selector:
            self.source_img_selector = TK_selector()
        self.source_list = self.source_img_selector()

    def select_input_valid_shp(self):
        if not self.valid_shp_selector:
            self.valid_shp_selector = TK_selector()
        self.valid_list = self.valid_shp_selector()

    def select_input_cloud_shp(self):
        if not self.cloud_shp_selector:
            self.cloud_shp_selector = TK_selector()
        self.cloud_list = self.cloud_shp_selector()

    def parse_input_target_img(self, x):
        self.target_list = []
        splitted_list = x.value.split('\n')
        for i in splitted_list:
            self.target_list.append(i.replace('"', ''))

    def parse_input_source_img(self, x):
        self.source_list = []
        splitted_list = x.value.split('\n')
        for i in splitted_list:
            self.source_list.append(i.replace('"', ''))

    def parse_input_valid(self, x):
        self.valid_list = []
        splitted_list = x.value.split('\n')
        for i in splitted_list:
            self.valid_list.append(i.replace('"', ''))

    def parse_input_cloud(self, x):
        self.cloud_list = []
        splitted_list = x.value.split('\n')
        for i in splitted_list:
            self.cloud_list.append(i.replace('"', ''))

    def check(self):
        if not self.rem_output_list:
            self.set_output()
        self.img_list = self.target_list + self.source_list
        self.target_num = len(self.target_list)
        self.print_members()

    def run(self):
        ui.notify(f'run !!!')
        # rem_main(self)


class MosaicParam:
    def __init__(self):
        self.program_progress = 'coming soon'
        self.mos_input_list = []
        self.valid_list = []
        self.mos_output_path = None
        self.if_build_overview = False
        self.ratio = 10
        self.win_size = 256
        self.res = 2
        self.work_dir = 'workspace'
        self.mos_union_path = None
        self.output_region_shp = None
        self.mos_cost_time = 'mos_cost_time'
        self.mos_message = 'mos_message'
        self.program_progress = 'coming soon'

        # todo
        self.color_trans = False

    def set_if_build_overview(self):
        self.if_build_overview = True

    def set_color_trans(self):
        self.color_trans = True

    def print_members(self):
        for member_name, member_value in vars(self).items():
            print(f"{member_name}: {member_value}")

    def get_mos_input_list(self):
        tk_selector = TK_selector()
        self.mos_input_list = tk_selector()

    def parse_input_img(self, x):
        self.mos_input_list = []
        splitted_list = x.value.split('\n')
        for i in splitted_list:
            self.mos_input_list.append(i.replace('"', ''))

    def parse_input_valid(self, x):
        self.valid_list = []
        splitted_list = x.value.split('\n')
        for i in splitted_list:
            self.valid_list.append(i.replace('"', ''))

    def check(self):
        self.print_members()

    def run(self):
        ui.notify(f'run !!!')
        # mos_main(self)


class CloudDetectParam:
    def __init__(self):
        self.program_progress = 'coming soon'
        self.img_list = []
        self.valid_list = []
        self.cloud_list = []
        self.device = 'cuda:0'
        self.output_dir = r'D:\龙超俊的文件夹'
        self.work_dir = 'workspace'
        self.det_cost_time = 'cost_time'
        self.det_message = 'message'

        self.input_img_selector = None

    def select_input_img(self):
        if not self.input_img_selector:
            self.input_img_selector = TK_selector()
        self.img_list = self.input_img_selector()

    def print_members(self):
        for member_name, member_value in vars(self).items():
            print(f"{member_name}: {member_value}")

    def set_output(self):
        for i in self.img_list:
            self.valid_list.append(
                os.path.join(self.output_dir, os.path.splitext(os.path.basename(i))[0] + '_valid.shp'))
            self.cloud_list.append(
                os.path.join(self.output_dir, os.path.splitext(os.path.basename(i))[0] + '_cloud.shp'))

    def parse_input_img(self, x):
        self.img_list = []
        splitted_list = x.value.split('\n')
        for i in splitted_list:
            self.img_list.append(i.replace('"', ''))

    def check(self):
        if not self.valid_list:
            self.set_output()
        self.print_members()

    def run(self):
        ui.notify(f'run !!!')
        # det_main(self)
