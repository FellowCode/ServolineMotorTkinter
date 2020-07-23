import tkinter.ttk as ttk
from tkinter import *
import Image, ImageTk
from ui_modifications import *

style = None
font_small = ('Calibri', 10)
font_mean = ('Calibri', 12)

class Form:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)

    def show_element(self, elem):
        elem.lift(self.frame)

    def hide_element(self, elem):
        elem.lower(self.frame)

class UIPart:
    def __init__(self, master, **kwargs):
        self.frame_part = Frame(master)
        self.frame_part.place(**kwargs)

    def show_element(self, elem):
        elem.lift(self.frame_part)

    def hide_element(self, elem):
        elem.lower(self.frame_part)

class MainForm(Form):
    entry_com = None
    entry_es_com = None
    btn_connect = None
    switch_motor = None
    entry_speed = None
    entry_accel_time = None
    entry_deccel_time = None
    entry_work_time = None
    combobox_presets = None
    btn_add_preset = None
    btn_change_preset = None
    btn_del_preset = None
    image_speed_error = None

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.style_init()
        self.vars_init()
        self.ui_init()

    def style_init(self):
        style = ttk.Style()
        style.theme_use('vista')
        style.configure('TLabel', font=font_mean)
        style.configure('small.TLabel', font=font_small)
        style.configure('Param.TEntry', font=font_mean)
        style.configure('TButton', font=font_mean)
        style.configure('Mini.TButton', font=font_small)
        style.configure('SwitchOn.TButton', background='blue', foreground='blue')
        style.configure('TCombobox', font=font_mean)

    def vars_init(self):
        self.com = IntVar()
        self.escom = IntVar()
        self.speed = IntVar()
        self.accel_time = IntVar()
        self.deccel_time = IntVar()
        self.work_time = IntVar()
        self.preset_var = StringVar()
        self.preset_group_var = StringVar()

    def ui_init(self):
        self.label_com = ttk.Label(self.master, text='COM')
        self.label_com.place(x=10, y=10)

        self.entry_com = IntegerEntry(self.master, textvariable=self.com)
        self.entry_com.bind('<FocusOut>', (lambda _: self.save_params()))
        self.entry_com.place(x=50, y=10, width=30)

        self.btn_connect = CButton(self.master, text='Подключиться', style='Mini.TButton')
        self.btn_connect.place(x=90, y=8)

        self.label_motor = ttk.Label(self.master, text='Motor')
        self.label_motor.place(x=250, y=10)

        self.switch_motor = SwitchButton(self.master, state='disabled')
        self.switch_motor.place(x=300, y=7, width=60)

        self.label_speed = ttk.Label(self.master, text='Скорость')
        self.label_speed.place(x=155, y=50, anchor='ne')
        self.label_accel_time = ttk.Label(self.master, text='Время ускорения')
        self.label_accel_time.place(x=155, y=80, anchor='ne')
        self.label_deccel_time = ttk.Label(self.master, text='Время торможения')
        self.label_deccel_time.place(x=155, y=110, anchor='ne')
        self.label_work_time = ttk.Label(self.master, text='Время работы')
        self.label_work_time.place(x=155, y=140, anchor='ne')

        self.entry_speed = ParamEntry(self.master, app=self, textvariable=self.speed, font=font_mean)
        self.entry_speed.place(x=165, y=50, width=60)
        self.entry_accel_time = ParamEntry(self.master, app=self, textvariable=self.accel_time, font=font_mean)
        self.entry_accel_time.place(x=165, y=80, width=60)
        self.entry_deccel_time = ParamEntry(self.master, app=self, textvariable=self.deccel_time, font=font_mean)
        self.entry_deccel_time.place(x=165, y=110, width=60)
        self.entry_work_time = ParamEntry(self.master, app=self, textvariable=self.work_time, font=font_mean)
        self.entry_work_time.place(x=165, y=140, width=60)

        img_temp = Image.open('img/error2.png').resize((20, 20), Image.ANTIALIAS)
        img_temp = ImageTk.PhotoImage(img_temp)
        self.image_speed_error = ttk.Label(image=img_temp)
        self.image_speed_error.image = img_temp
        # app.image_speed_error.place(x=230, y=50)

        logo_temp = Image.open('img/logo.png').resize((130, 130), Image.ANTIALIAS)
        logo_temp = ImageTk.PhotoImage(logo_temp)
        self.image_logo = ttk.Label(image=logo_temp)
        self.image_logo.image = logo_temp
        self.image_logo.place(x=245, y=40)

        self.combobox_preset_groups = ttk.Combobox(self.master, state='readonly', textvariable=self.preset_group_var,
                                             font=font_mean)
        self.combobox_preset_groups.bind('<<ComboboxSelected>>', None)
        self.combobox_preset_groups.place(x=20, y=180)

        self.combobox_presets = ttk.Combobox(self.master, state='readonly', textvariable=self.preset_var, font=font_mean)
        self.combobox_presets.bind('<<ComboboxSelected>>', self.preset_selected)
        self.combobox_presets.place(x=20, y=220)
        self.btn_add_preset = CButton(self.master, text='+', style='Mini.TButton')
        self.btn_add_preset.place(x=205, y=220, width=30)
        self.btn_del_preset = CButton(self.master, text='-', style='Mini.TButton')
        self.btn_del_preset.place(x=235, y=220, width=30)
        self.btn_up_preset = CButton(self.master, text='/\\', style='Mini.TButton')
        self.btn_up_preset.place(x=265, y=220, width=30)
        self.btn_down_preset = CButton(self.master, text='\\/', style='Mini.TButton')
        self.btn_down_preset.place(x=295, y=220, width=30)


class AutoModePart(UIPart):
    btn_start = None
    btn_stop = None
    btn_change_mode = None
    switch_reverse = None
    label_move_state = None
    progressbar_motor = None
    def __init__(self, master):
        super().__init__(master, x=0, y=260, relwidth=1, height=100)
        self.master = master
        self.ui_init()

    def ui_init(self):
        self.btn_start = CButton(self.frame_part, text='Старт')
        self.btn_start.place(x=20, y=0)
        self.btn_stop = CButton(self.frame_part, text='Стоп')
        self.btn_stop.place(x=130, y=0)
        self.btn_change_mode = CButton(self.frame_part, text='Авто режим')
        self.btn_change_mode.place(x=240, y=0, width=140)

        self.label_reverse = ttk.Label(self.frame_part, text='Реверс')
        self.label_reverse.place(x=20, y=45)
        self.switch_reverse = SwitchButton(self.frame_part)
        self.switch_reverse.place(x=80, y=43, width=60)
        self.label_move_state = ttk.Label(self.frame_part, text='Движение на себя')
        self.label_move_state.place(x=190, y=45)

        self.progressbar_motor = ttk.Progressbar(self.frame_part, orient="horizontal", mode="determinate")
        self.progressbar_motor.place(x=0, y=80, relwidth=1, height=20)

class ManualModePart(UIPart):
    btn_forward = None
    btn_back = None
    btn_change_mode = None

    def __init__(self, master):
        super().__init__(master, x=0, y=260, relwidth=1, height=100)
        self.master = master
        self.ui_init()

    def ui_init(self):
        self.btn_back = CButton(self.frame_part, text='\\/ На себя')
        self.btn_back.place(x=20, y=0)
        self.btn_forward = CButton(self.frame_part, text='/\\ От себя')
        self.btn_forward.place(x=130, y=0)
        self.btn_change_mode = CButton(self.frame_part, text='Ручной режим')
        self.btn_change_mode.place(x=240, y=0, width=140)


class AdditionalForm(Form):
    width = 300
    height = 100
    def __init__(self, main_master, master):
        super().__init__(master)
        self.main_master = main_master
        self.master = master
        self.set_size()

    def set_size(self, width=None, height=None):
        if width:
            self.width = width
        if height:
            self.height = height
        self.posx = self.main_master.winfo_x() + (self.main_master.winfo_width() - self.width) / 2
        self.posy = self.main_master.winfo_y() + (self.main_master.winfo_height() - self.height) / 2
        self.master.geometry('%dx%d+%d+%d' % (self.width, self.height, self.posx, self.posy))

    def set_title(self, title):
        self.master.winfo_toplevel().title(title)

    def close(self):
        self.master.destroy()

class NotifyForm(AdditionalForm):
    def __init__(self, main_master, master):
        super().__init__(main_master, master)
        self.master.resizable(False, False)
        self.ui_init()

    def ui_init(self):
        self.message_notify = Message(self.master, text='', width=self.width * 0.9, font=font_mean)
        self.message_notify.place(relx=0.5, rely=0.3, anchor='center')

        self.btn_ok = CButton(self.master, text='Ok')
        self.btn_ok.bind_release(self.close)
        self.btn_ok.place(relx=0.5, rely=0.8, anchor='center')

    def set_text(self, text):
        self.message_notify['text'] = text

class AddPresetForm(AdditionalForm):
    def __init__(self, main_master, master):
        super().__init__(main_master, master)
        self.master.resizable(False, False)
        self.vars_init()
        self.ui_init()

    def vars_init(self):
        self.name = StringVar()

    def ui_init(self):
        self.label_msg = ttk.Label(self.master, text='Добавить пресет')
        self.label_msg.place(relx=0.5, y=15, anchor='center')

        self.entry_preset_name = ttk.Entry(self.master, textvariable=self.name, font=font_mean)
        self.entry_preset_name.place(relx=0.5, y=45, relwidth=0.8, anchor='center')
        self.entry_preset_name.focus()

        self.btn_ok = CButton(self.master, text='Ok')
        self.btn_ok.bind_release(self.add_preset)
        self.btn_ok.place(relx=0.5, y=78, relwidth=0.4, anchor='e')

        self.btn_cancel = CButton(self.master, text='Отмена')
        self.btn_cancel.bind_release(self.close)
        self.btn_cancel.place(relx=0.5, y=78, relwidth=0.4, anchor='w')
