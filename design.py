import tkinter.ttk as ttk
import Image, ImageTk

style = None


class CButton(ttk.Button):
    def bind_release(self, func, args=(), kwargs={}):
        try:
            self.bind('<ButtonRelease-1>', lambda ev: func(*args, **kwargs))
        except:
            print('Error btn binding')

    def bind_hold(self, func_press, func_release):
        try:
            self.bind('<ButtonPress-1>', lambda ev: func_press())
            self.bind('<ButtonRelease-1>', lambda ev: func_release())
        except:
            print('Error btn binding')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SwitchButton(ttk.Button):
    val = False
    func = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['text'] = 'OFF'
        self.bind('<ButtonRelease-1>', lambda ev: self.change_val())
        if 'func' in kwargs.keys():
            self.fswitch_func = kwargs['func']

    def change_val(self):
        self.val = not self.val
        if self.val:
            self['text'] = 'ON'
            self['style'] = 'SwitchOn.TButton'
        else:
            self['text'] = 'OFF'
            self['style'] = 'TButton'
        if self.func:
            self.func(self.val)

    def set_val(self, val):
        self.val = not val
        self.change_val()

    def bind_sw(self, func):
        self.func = func


class IntegerEntry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<KeyRelease>', self.entry_changed)

    def entry_changed(self, event):
        for index, char in enumerate(self.get()):
            if not char in '0123456789':
                self.delete(index, index+1)

def ui_setup(app):
    style = ttk.Style()
    style.theme_use('vista')
    style.configure('TLabel', font=('Calibri', 12))
    style.configure('Param.TEntry', font=('Calibri', 12))
    style.configure('TButton', font=('Calibri', 12))
    style.configure('Mini.TButton', font=('Calibri', 10))
    style.configure('SwitchOn.TButton', background='blue')
    style.configure('TCombobox', font=('Calibri', 14))

    app.frame = ttk.Frame(app.master)

    app.label_com = ttk.Label(app.frame, text='COM')
    app.label_com.place(x=10, y=10)

    app.entry_com = IntegerEntry(app.frame, textvariable=app.com)
    app.entry_com.bind('<FocusOut>', (lambda _: app.entry_changed(app.entry_com)))
    app.entry_com.place(x=50, y=10, width=30)

    app.btn_connect = CButton(app.frame, text='Подключиться', style='Mini.TButton')
    app.btn_connect.place(x=90, y=8)

    app.label_motor = ttk.Label(app.frame, text='Motor')
    app.label_motor.place(x=250, y=10)

    app.switch_motor = SwitchButton(app.frame, state='disabled')
    app.switch_motor.place(x=300, y=7, width=60)

    app.label_speed = ttk.Label(app.frame, text='Скорость')
    app.label_speed.place(x=155, y=50, anchor='ne')
    app.label_accel_time = ttk.Label(app.frame, text='Время ускорения')
    app.label_accel_time.place(x=155, y=80, anchor='ne')
    app.label_deccel_time = ttk.Label(app.frame, text='Время торможения')
    app.label_deccel_time.place(x=155, y=110, anchor='ne')
    app.label_work_time = ttk.Label(app.frame, text='Время работы')
    app.label_work_time.place(x=155, y=140, anchor='ne')

    app.entry_speed = IntegerEntry(app.frame, textvariable=app.speed, font=('Calibri', 12))
    app.entry_speed.bind('<FocusOut>', (lambda _: app.entry_changed(app.entry_speed)))
    app.entry_speed.place(x=165, y=50, width=60)
    app.entry_accel_time = IntegerEntry(app.frame, textvariable=app.accel_time, font=('Calibri', 12))
    app.entry_accel_time.bind('<FocusOut>', (lambda _: app.entry_changed(app.entry_accel_time)))
    app.entry_accel_time.place(x=165, y=80, width=60)
    app.entry_deccel_time = IntegerEntry(app.frame, textvariable=app.deccel_time, font=('Calibri', 12))
    app.entry_deccel_time.bind('<FocusOut>', (lambda _: app.entry_changed(app.entry_deccel_time)))
    app.entry_deccel_time.place(x=165, y=110, width=60)
    app.entry_work_time = IntegerEntry(app.frame, textvariable=app.work_time, font=('Calibri', 12))
    app.entry_work_time.bind('<FocusOut>', (lambda _: app.entry_changed(app.entry_work_time)))
    app.entry_work_time.place(x=165, y=140, width=60)

    img_temp = Image.open('img/error2.png').resize((20, 20), Image.ANTIALIAS)
    img_temp = ImageTk.PhotoImage(img_temp)
    app.image_speed_error = ttk.Label(image=img_temp)
    app.image_speed_error.image = img_temp
    #app.image_speed_error.place(x=230, y=50)


    app.combobox_presets = ttk.Combobox(app.frame, state='readonly', textvariable=app.preset)
    app.combobox_presets.place(x=20, y=180)
    app.btn_add_preset = CButton(app.frame, text='+', style='Mini.TButton')
    app.btn_add_preset.place(x=165, y=178, width=30)
    app.btn_del_preset = CButton(app.frame, text='-', style='Mini.TButton')
    app.btn_del_preset.place(x=195, y=178, width=30)

    app.frame.place(x=0, y=0, relwidth=1, relheight=1)

def ui_setup_auto_mode(app, auto_part):
    app.frame_auto_mode = ttk.Frame(app.frame)
    auto_part.btn_start = CButton(app.frame_auto_mode, text='Старт')
    auto_part.btn_start.place(x=20, y=0)
    auto_part.btn_stop = CButton(app.frame_auto_mode, text='Стоп')
    auto_part.btn_stop.place(x=130, y=0)
    auto_part.btn_change_mode = CButton(app.frame_auto_mode, text='Ручной режим')
    auto_part.btn_change_mode.place(x=240, y=0, width=140)

    auto_part.label_reverse = ttk.Label(app.frame_auto_mode, text='Реверс')
    auto_part.label_reverse.place(x=20, y=50)
    auto_part.switch_reverse = SwitchButton(app.frame_auto_mode)
    auto_part.switch_reverse.place(x=80, y=48, width=60)
    auto_part.label_move_state = ttk.Label(app.frame_auto_mode, text='Движение на себя')
    auto_part.label_move_state.place(x=190, y=50)


def ui_setup_manual_mode(app, manual_part):
    app.frame_manual_mode = ttk.Frame(app.frame)
    manual_part.btn_back = CButton(app.frame_manual_mode, text='\\/ На себя')
    manual_part.btn_back.place(x=20, y=0)
    manual_part.btn_forward = CButton(app.frame_manual_mode, text='/\\ От себя')
    manual_part.btn_forward.place(x=130, y=0)
    manual_part.btn_change_mode = CButton(app.frame_manual_mode, text='Авто режим')
    manual_part.btn_change_mode.place(x=240, y=0, width=140)
