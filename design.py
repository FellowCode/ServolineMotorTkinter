from tkinter import *
import tkinter.ttk as ttk

def design_wrap(app):
    app.style = ttk.Style()
    app.style.theme_use('vista')
    app.style.configure('TLabel', font=('Calibri', 12))
    app.style.configure('TButton', font=('Calibri', 12))
    app.style.configure('Mini.TButton', font=('Calibri', 10))
    app.style.configure('MotorOn.TButton', background='blue')
    app.style.configure('TCombobox', font=('Calibri', 14))

    app.frame = ttk.Frame(app.master)

    app.label_com = ttk.Label(app.frame, text='COM')
    app.label_com.place(x=10, y=10)

    app.entry_com = ttk.Entry(app.frame, textvariable=app.com_var)
    app.entry_com.place(x=50, y=10, width=30)

    app.btn_connect = ttk.Button(app.frame, text='Подключиться', style='Mini.TButton')
    app.btn_connect.place(x=90, y=8)

    app.label_motor = ttk.Label(app.frame, text='Motor')
    app.label_motor.place(x=250, y=10)

    app.btn_motor = ttk.Button(app.frame, text='Off')
    app.btn_motor.place(x=300, y=7, width=60)

    app.label_speed = ttk.Label(app.frame, text='Скорость')
    app.label_speed.place(x=20, y=50)
    app.label_accel_time = ttk.Label(app.frame, text='Время ускорения')
    app.label_accel_time.place(x=20, y=80)
    app.label_deccel_time = ttk.Label(app.frame, text='Время торможения')
    app.label_deccel_time.place(x=20, y=110)
    app.label_work_time = ttk.Label(app.frame, text='Время работы')
    app.label_work_time.place(x=20, y=140)

    app.entry_speed = ttk.Entry(app.frame, textvariable=app.speed)
    app.entry_speed.place(x=165, y=50, width=60)
    app.entry_accel_time = ttk.Entry(app.frame, textvariable=app.accel_time)
    app.entry_accel_time.place(x=165, y=80, width=60)
    app.entry_deccel_time = ttk.Entry(app.frame, textvariable=app.deccel_time)
    app.entry_deccel_time.place(x=165, y=110, width=60)
    app.entry_work_time = ttk.Entry(app.frame, textvariable=app.work_time)
    app.entry_work_time.place(x=165, y=140, width=60)

    app.combobox_presets = ttk.Combobox(app.frame, state='readonly', textvariable=app.preset)
    app.combobox_presets.place(x=20, y=180)
    app.btn_add_preset = ttk.Button(app.frame, text='+', style='Mini.TButton')
    app.btn_add_preset.place(x=165, y=178, width=30)
    app.btn_del_preset = ttk.Button(app.frame, text='-', style='Mini.TButton')
    app.btn_del_preset.place(x=195, y=178, width=30)

    app.frame_auto_mode = ttk.Frame(app.frame)
    app.btn_auto_start = ttk.Button(app.frame_auto_mode, text='Старт')
    app.btn_auto_start.place(x=20, y=0)
    app.btn_auto_stop = ttk.Button(app.frame_auto_mode, text='Стоп')
    app.btn_auto_stop.place(x=130, y=0)
    app.btn_auto_change_mode = ttk.Button(app.frame_auto_mode, text='Ручной режим')
    app.btn_auto_change_mode.place(x=240, y=0, width=140)

    app.label_reverse = ttk.Label(app.frame_auto_mode, text='Реверс')
    app.label_reverse.place(x=20, y=50)
    app.btn_reverse = ttk.Button(app.frame_auto_mode, text='Off')
    app.btn_reverse.place(x=80, y=48, width=60)
    app.label_move_state = ttk.Label(app.frame_auto_mode, text='Движения на себя')
    app.label_move_state.place(x=190, y=50)

    app.frame_auto_mode.place(x=0, y=220, relwidth=1, height=100)
    app.frame.place(x=0, y=0, relwidth=1, relheight=1)

def bind_buttons(app):
    pass

def bind_entry(app):
    pass