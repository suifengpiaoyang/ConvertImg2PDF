import os
import json
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mBox
from img_changer import ImgChanger
from tkinter import scrolledtext

DEFAULT_PATH = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(DEFAULT_PATH, 'guiconfig.json')
WIDGETS_WIDTH = 25

class JsonLoader:

    def __init__(self):
        self.json = {}

    def load(self,path):
        try:
            with open(path,encoding = 'utf-8') as fl:
                self.json = json.load(fl)
        except Exception as e:
            pass

    def save(self,path):
        with open(path,'w',encoding = 'utf-8')as fl:
            json.dump(self.json, fl,ensure_ascii = False,sort_keys = True,indent = 4)

class GUI:

    def __init__(self):
        self.data = JsonLoader()
        self.image_changer = ImgChanger()
        self.data.load(CONFIG_FILE)
        self.win = tk.Tk()
        self.win.withdraw()
        self.win.title('图片合并小助手')
        self.create_widgets()
        self.center_window(self.win)
        self.win.deiconify()
        self.win.mainloop()

    def create_thread(self, func, **kwargs):
        thread = threading.Thread(target=func, daemon=True, **kwargs)
        thread.start()

    def choose_target_dictory(self):
        td = fd.askdirectory(parent=self.labelframe,initialdir=os.path.dirname(__file__))
        self.frame1_entry_var1.set(os.path.basename(td))
        # self.frame1_entry_var1.set(td)
        self.data.json['target_path'] = td

    def choose_img_dictory(self):
        id = fd.askdirectory(parent=self.labelframe, initialdir=os.path.dirname(__file__))
        self.img_path_var.set(id)
        self.data.json['img_path'] = id
        self.data.save(CONFIG_FILE)

    def save_configure(self):
        self.data.save(CONFIG_FILE)
        mBox.showinfo('提示','保存成功。')

    def create_widgets(self):

        self.labelframe = ttk.LabelFrame(self.win,text = '图片转 PDF')
        self.labelframe.grid(row = 0,column = 0,padx = 10,pady = 10)

        self.frame_left = ttk.Frame(self.labelframe)
        self.frame_right = ttk.Frame(self.labelframe)
        self.frame1 = ttk.Frame(self.frame_left)
        self.frame2 = ttk.Frame(self.frame_left)
        self.frame3 = ttk.Frame(self.frame_left)
        self.frame_left.grid(row = 0,column = 0,padx = 10,pady = 5)
        self.frame_right.grid(row = 0,column = 1,pady = 5)
        self.frame1.grid(row = 0,column = 0)
        self.frame2.grid(row = 1,column = 0)
        self.frame3.grid(row = 2,column = 0)

        # frame1 widgets

        # values 
        self.frame1_entry_var1 = tk.StringVar()
        self.frame1_entry_var2 = tk.StringVar()

        button1_frame1 = ttk.Button(self.frame1,text = '存储文件夹',command = self.choose_target_dictory)
        button2_frame1 = ttk.Button(self.frame1,text = '图片文件夹')
        label_frame1 = ttk.Label(self.frame1,text = '使用模式')
        entry1_frame1 = ttk.Entry(self.frame1,width = WIDGETS_WIDTH,textvariable = self.frame1_entry_var1,state = tk.DISABLED)
        entry2_frame1 = ttk.Entry(self.frame1,width = WIDGETS_WIDTH,textvariable = self.frame1_entry_var2,state = tk.DISABLED)
        combobox_frame1 = ttk.Combobox(self.frame1,width = WIDGETS_WIDTH - 2)

        button1_frame1.grid(row = 0,column = 0)
        button2_frame1.grid(row = 1,column = 0)
        label_frame1.grid(row = 2,column = 0)
        entry1_frame1.grid(row = 0,column = 1,sticky = 'W')
        entry2_frame1.grid(row = 1,column = 1,sticky = 'W')
        combobox_frame1.grid(row = 2,column = 1,sticky = 'W')

        # frame2 widgets
        label1_frame2 = ttk.Label(self.frame2,text = '格式')
        combobox_frame2 = ttk.Combobox(self.frame2,width = 6)
        combobox_frame2['values'] = ['jpg','bmp','png']
        combobox_frame2.current(0)
        check_button_frame2 = ttk.Checkbutton(self.frame2,text = '排序')

        label1_frame2.grid(row = 0,column = 0,padx = 13)
        combobox_frame2.grid(row = 0,column = 1,padx = 35)
        check_button_frame2.grid(row = 0,column = 2,padx = 10)

        # frame3 widgets
        button1_frame3 = ttk.Button(self.frame3,text = '保存配置',width = 9,command = self.save_configure)
        button2_frame3 = ttk.Button(self.frame3,text = '开始转化',width = 9)

        button1_frame3.grid(row = 0,column = 0)
        button2_frame3.grid(row = 0,column = 1)

        # frame_right widgets
        scr = scrolledtext.ScrolledText(self.frame_right,width = 23,height = 23)
        scr.grid(column = 0,row = 0)

        for child in self.labelframe.winfo_children():
            child.grid_configure(padx = 10,pady = 5)

        for child in self.frame1.winfo_children():
            child.grid_configure(padx = 10,pady = 5)

        for child in self.frame2.winfo_children():
            child.grid_configure(pady = 5)

        for child in self.frame3.winfo_children():
            child.grid_configure(padx = 23,pady = 10)

    def center_window(self, master, width_flag=0.382, height_flag=0.382):
        """
        窗口先隐藏到大小设置完成以后才恢复，主要原因是如果不这么做，会发生闪影现象。
        width_flag 和 height_flag 值在 (0,1) ，是定位目标左上角的坐标的权重值。
        都设置为 0.5 的话，则窗口居中。默认是窗口放在黄金比例上。
        withdraw() 函数是隐藏窗口，deiconify() 函数是显示窗口。
        update() 函数是将前面原件摆放以后的窗口更新，以便获得摆放后窗口的自适配大小。
        """
        master.withdraw()
        master.update()
        current_window_width = master.winfo_width()
        current_window_height = master.winfo_height()
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        suitable_location_x = int(
            (screen_width - current_window_width) * width_flag)
        suitable_location_y = int(
            (screen_height - current_window_height) * height_flag)
        master.geometry(
            '+{}+{}'.format(suitable_location_x, suitable_location_y))
        master.deiconify()

if __name__ == '__main__':
    GUI()
