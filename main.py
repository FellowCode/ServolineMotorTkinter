from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from design import design_wrap
from ctypes import windll
from threading import Timer


class ServolineMotorApp:
    def __init__(self, master):
        self.master = master
        self.set_default_settings()
        design_wrap(self)

    def set_default_settings(self):
        self.com_var = StringVar()
        self.speed = StringVar()
        self.accel_time = StringVar()
        self.deccel_time = StringVar()
        self.work_time = StringVar()
        self.preset = StringVar()
        self.preset.set('Пресеты')
        self.master.geometry('400x320')
        self.master.resizable(False, False)

class AutoMode:
    reverse = False

    def start_servo_time_work(self, instance):
        self.motor_timer = Timer(int(app.work_time.get()) / 1000, self.stop_servo_time_work)
        self.motor_timer.start()
        self.start_button.disabled = True
        self.reverse_switch.disabled = True
        # if not self.reverse:
        #     myApp.root_widget.motor.servo_forward_start()
        # else:
        #     myApp.root_widget.motor.servo_reverse_start()
        myApp.root_widget.motor.servo_reverse_start()

    def stop_servo_time_work(self, instance=None):
        self.motor_timer.cancel()
        self.start_button.disabled = False
        self.reverse_switch.disabled = False
        # if not self.reverse:
        #     myApp.root_widget.motor.servo_forward_stop()
        # else:
        #     myApp.root_widget.motor.servo_reverse_stop()
        myApp.root_widget.motor.servo_reverse_stop()

    def change_reverse(self, instance, value):
        self.reverse = myApp.root_widget.reverse = value
        myApp.root_widget.save_params()

    def disable_buttons(self, val):
        self.start_button.disabled = val
        self.stop_button.disabled = val
        self.mode_button.disabled = val
        self.reverse_switch.disabled = val

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('start build auto_widget')
        self.start_button.bind(on_press=self.start_servo_time_work)
        self.stop_button.bind(on_press=self.stop_servo_time_work)
        self.mode_button.bind(on_press=myApp.change_mode)
        self.reverse_switch.bind(active=self.change_reverse)
        self.reverse_switch.active = myApp.root_widget.reverse
        print('auto_widget builded')

if __name__ == '__main__':
    # user32 = windll.user32
    # user32.SetProcessDPIAware()
    root = tk.Tk()
    app = ServolineMotorApp(root)

    root.mainloop()

