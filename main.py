from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from design import *
from ctypes import windll

from modbus import Modbus
import os
import pickle
from servo_reg import ServoReg
from modes import *
from notify_windows import *


appdata_path = os.getenv('APPDATA') + '\\ServolineMotor\\'
if not os.path.exists(appdata_path):
    os.makedirs(appdata_path)

class ServolineMotorApp:
    reverse = False
    mode = 'auto'
    motor = Modbus()

    auto_speed = 50
    auto_accel_time = 200
    auto_deccel_time = 200
    auto_work_time = 0

    manual_speed = 50
    manual_accel_time = 200
    manual_deccel_time = 200

    auto_presets = manual_presets = []

    sync_param_process = False

    def save_params(self):
        print('save params')
        try:
            with open(appdata_path + 'settings.txt', 'w') as f:
                f.write(str(self.com.get()) + '\n')
                f.write(str(self.auto_speed) + '\n')
                f.write(str(self.auto_accel_time) + '\n')
                f.write(str(self.auto_deccel_time) + '\n')
                f.write(str(self.auto_work_time) + '\n')
                f.write(str(self.reverse) + '\n')
                f.write(str(self.manual_speed) + '\n')
                f.write(str(self.manual_accel_time) + '\n')
                f.write(str(self.manual_deccel_time) + '\n')
        except:
            print('save params error')

    def load_params(self):
        print('load params')
        try:
            f = open(appdata_path + 'settings.txt')
            self.com.set(f.readline().strip())
            auto_speed = f.readline().strip()
            if auto_speed != '-1':
                self.speed.set(int(auto_speed))
                self.accel_time.set(int(f.readline().strip()))
                self.deccel_time.set(int(f.readline().strip()))
                self.work_time.set(int(f.readline().strip()))
                self.auto_speed = self.speed.get()
                self.auto_accel_time = self.accel_time.get()
                self.auto_deccel_time = self.deccel_time.get()
                self.auto_work_time = self.work_time.get()
                self.reverse = f.readline().strip() == 'True'
            else:
                for i in range(4):
                    f.readline()
            manual_speed = int(f.readline())
            if manual_speed != -1:
                self.manual_speed = manual_speed
                self.manual_accel_time = int(f.readline())
                self.manual_deccel_time = int(f.readline())
            f.close()
        except:
            print('load params error')

    def save_presets(self):
        with open(appdata_path + 'presets.prs', 'wb') as f:
            presets = [self.auto_presets, self.manual_presets]
            pickle.dump(presets, f)

    def load_presets(self):
        try:
            with open(appdata_path + 'presets.prs', 'rb') as f:
                presets = pickle.load(f)
                self.auto_presets = presets[0]
                self.manual_presets = presets[1]
        except:
            self.auto_presets = []
            self.manual_presets = []

    def check_param_equals(self):
        pass

    def disable_buttons(self, val):
        #self.buttons_is_disable = val
        self.auto.enable_buttons(val)
        self.manual.disable_buttons(val)

    def change_connect(self):
        if not self.motor.is_connect:
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        self.show_notify_window()
        self.motor.connect(self.com.get(), self)
        if self.motor.is_connect:
            self.btn_connect['text'] = 'Отключиться'
            self.switch_motor['state'] = 'normal'
            #self.apply_param_button.disabled = False
            #self.sync_params_button.disabled = False
        self.servo_sync_params()

    def disconnect(self):
        self.motor.disconnect()
        if not self.motor.is_connect:
            self.btn_connect['text'] = 'Подключиться'
            self.switch_motor.set_val(False)
            self.switch_motor['state'] = 'disabled'
            #self.apply_param_button.disabled = True
            #self.sync_params_button.disabled = True
            self.disable_buttons(True)

    def motor_change_state(self, value):
        if value:
            def check_motor_is_on(*args, **kwargs):
                ans = kwargs['ans']
                right_ans = kwargs['right_ans']
                print(ans, right_ans)
                if ans == right_ans:
                    print(value)
                    self.disable_buttons(value)

            self.motor.servo_on(right_func=check_motor_is_on)
        else:
            self.motor.servo_off()
            self.disable_buttons(value)


    def set_param_in_entry(self, register, value):
        print(register, value)
        if self.mode == 'auto':
            if register == ServoReg.SPEED:
                self.auto_speed = value
                self.speed.set(value)
            elif register == ServoReg.ACCEL_TIME:
                self.auto_accel_time = value
                self.accel_time.set(value)
            elif register == ServoReg.DECCEL_TIME:
                self.auto_deccel_time = value
                self.deccel_time.set(value)
        else:
            if register == ServoReg.SPEED:
                self.manual_speed = value
                self.speed.set(value)
            elif register == ServoReg.ACCEL_TIME:
                self.manual_accel_time = value
                self.accel_time.set(value)
            elif register == ServoReg.DECCEL_TIME:
                self.manual_deccel_time = value
                self.deccel_time.set(value)

        if register == ServoReg.DECCEL_TIME and self.sync_param_process:
            self.sync_param_process = False
            if self.switch_motor.val:
                self.disable_buttons(False)

        self.check_param_equals()
        self.save_params()


    def servo_sync_params(self):
        self.sync_param_process = True
        self.disable_buttons(self.switch_motor.val)
        registers = [ServoReg.SPEED, ServoReg.ACCEL_TIME, ServoReg.DECCEL_TIME]
        for register in registers:
            def check_answer(*args, **kwargs):
                try:
                    ans = kwargs['ans']
                    register = kwargs['register']
                    if ans[:7] == ':010302':
                        self.set_param_in_entry(register, int(ans[7:11], 16))
                except:
                    pass

            self.motor.get_param(register=register, right_func=check_answer)


    def servo_set_params(self):
        def apply_param(*args, **kwargs):
            ans = kwargs['ans']
            right_ans = kwargs['right_ans']
            if ans == right_ans:
                print('param applied on motor')
                register = int(ans[5:9], 16)
                value = int(ans[9:13], 16)
                self.set_param_in_entry(register, value)
            else:
                print('param apply on motor error')

        speed = self.speed.get()
        accel_time = self.accel_time.get()
        deccel_time = self.deccel_time.get()
        values = [speed, accel_time, deccel_time]
        registers = [ServoReg.SPEED, ServoReg.ACCEL_TIME, ServoReg.DECCEL_TIME]
        self.sync_param_process = True
        self.disable_buttons(True)
        for i, val in enumerate(values):
            def set_param_on_motor(*args, **kwargs):
                try:
                    ans = kwargs['ans']
                    current_val = kwargs['current_val']
                    #set_param if difference
                    if (ans[:7] == ':010302' and int(ans[7:11], 16) != current_val)or(ans[:7] != ':010302'):
                        print('value', i, 'difference')
                        try:
                            if current_val < 0:
                                current_val = 0
                            if i == 0 and current_val == 0:
                                current_val = 100
                            self.motor.set_param(register=registers[i], value=current_val, right_func=apply_param)
                        except:
                            pass
                except:
                    pass

            self.motor.get_param(register=registers[i], right_func=set_param_on_motor, current_val=val)

        try:
            self.auto_work_time = int(self.work_time.get())
        except:
            pass
        self.save_params()


    def entry_changed(self, entry):
        if self.mode == 'auto':
            self.auto_speed = self.speed.get()
            self.auto_accel_time = self.accel_time.get()
            self.auto_deccel_time = self.deccel_time.get()
            self.auto_work_time = self.work_time.get()
        else:
            self.manual_speed = self.speed.get()
            self.manual_accel_time = self.accel_time.get()
            self.manual_deccel_time = self.deccel_time.get()
        self.save_params()

    def change_mode(self):
        if self.mode == 'auto':
            self.mode = 'manual'
            self.auto.hide()
            self.manual.show()
            self.speed.set(self.manual_speed)
            self.accel_time.set(self.manual_accel_time)
            self.deccel_time.set(self.manual_deccel_time)
        else:
            self.mode = 'auto'
            self.manual.hide()
            self.auto.show()
            self.speed.set(self.auto_speed)
            self.accel_time.set(self.auto_accel_time)
            self.deccel_time.set(self.auto_deccel_time)

        self.servo_set_params()

    def show_notify_window(self):
        self.notify_master = Toplevel(self.master)
        self.notify_window = NotifyWindow(self)

    def error(self, text):
        print(text)


    def set_default_settings(self):
        self.com = IntVar()
        self.speed = IntVar()
        self.accel_time = IntVar()
        self.deccel_time = IntVar()
        self.work_time = IntVar()
        self.preset = StringVar()
        self.preset.set('Пресеты')
        self.master.geometry('400x320+200+200')
        self.master.resizable(False, False)

    def initial_ui_vars(self):
        self.entry_com = None
        self.btn_connect = None
        self.switch_motor = None
        self.entry_speed = None
        self.entry_accel_time = None
        self.entry_deccel_time = None
        self.entry_work_time = None
        self.combobox_presets = None
        self.btn_add_preset = None
        self.btn_del_preset = None

    def __init__(self, master):
        self.master = master
        self.set_default_settings()
        self.load_params()
        ui_setup(self)

        self.auto = AutoMode(self)
        self.manual = ManualMode(self)
        self.auto.show()

        self.btn_connect.bind_release(self.change_connect)

        self.switch_motor.bind_sw(self.motor_change_state)
        self.switch_motor.val = True
        self.switch_motor.change_val()





if __name__ == '__main__':
    # user32 = windll.user32
    # user32.SetProcessDPIAware()
    root = tk.Tk()
    app = ServolineMotorApp(root)

    root.mainloop()

