import tkinter as tk
from design import *
from ctypes import windll

from modbus import Modbus
import os
import pickle
from servo_reg import ServoReg
from modes import *
from additional_windows import *
from preset import Preset

appdata_path = os.getenv('APPDATA') + '\\ServolineMotor\\'
if not os.path.exists(appdata_path):
    os.makedirs(appdata_path)


class ServolineMotorApp(MainForm):
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

    auto_presets = []
    manual_presets = []
    auto_presets_id = -1
    manual_presets_id = -1

    sync_param_process = False

    entry_com = None
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

    def save_params(self):
        #print('save params')
        try:
            with open(appdata_path + 'settings.txt', 'w') as f:
                f.write(str(self.com.get()) + '\n')
                f.write(str(self.auto_speed) + '\n')
                f.write(str(self.auto_accel_time) + '\n')
                f.write(str(self.auto_deccel_time) + '\n')
                f.write(str(self.auto_work_time) + '\n')
                f.write(str(self.auto_presets_id) + '\n')
                f.write(str(self.reverse) + '\n')
                f.write(str(self.manual_speed) + '\n')
                f.write(str(self.manual_accel_time) + '\n')
                f.write(str(self.manual_deccel_time) + '\n')
                f.write(str(self.manual_presets_id) + '\n')
        except:
            print('save params error')

    def load_params(self):
        #print('load params')
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
                self.auto_presets_id = int(f.readline())
                self.reverse = f.readline().strip() == 'True'
            else:
                for i in range(4):
                    f.readline()
            manual_speed = int(f.readline())
            if manual_speed != -1:
                self.manual_speed = manual_speed
                self.manual_accel_time = int(f.readline())
                self.manual_deccel_time = int(f.readline())
                self.manual_presets_id = int(f.readline())
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

    def enable_buttons(self, val):
        #print('enable buttons', val)
        self.auto.enable_buttons(val)
        self.manual.enable_buttons(val)

    def change_connect(self):
        if not self.motor.is_connect:
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        self.motor.connect(self.com.get(), self)
        if self.motor.is_connect:
            self.btn_connect['text'] = 'Отключиться'
            self.switch_motor['state'] = 'normal'
        self.servo_sync_params()
        self.preset_var.set('Выбрать пресет')

    def disconnect(self):
        self.motor.disconnect()
        if not self.motor.is_connect:
            self.btn_connect['text'] = 'Подключиться'
            self.switch_motor.set_val(False)
            self.switch_motor['state'] = 'disabled'
            self.enable_buttons(True)

    def motor_change_state(self, value):
        if value:
            def check_motor_is_on(*args, **kwargs):
                ans = kwargs['ans']
                right_ans = kwargs['right_ans']
                print(ans, right_ans)
                if ans == right_ans:
                    print(value)
                    self.enable_buttons(value)

            self.motor.servo_on(right_func=check_motor_is_on)
        else:
            self.motor.servo_off()
            self.enable_buttons(value)

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
                self.enable_buttons(True)

        self.check_param_equals()
        self.save_params()

    def servo_sync_params(self):
        self.sync_param_process = True
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
        if self.motor.is_connect:
            def apply_param(*args, **kwargs):
                ans = kwargs['ans']
                right_ans = kwargs['right_ans']
                if ans == right_ans:
                    register = int(ans[5:9], 16)
                    value = int(ans[9:13], 16)
                    self.set_param_in_entry(register, value)
                else:
                    self.error('param apply on motor error')

            speed = self.speed.get()
            accel_time = self.accel_time.get()
            deccel_time = self.deccel_time.get()
            values = [speed, accel_time, deccel_time]
            registers = [ServoReg.SPEED, ServoReg.ACCEL_TIME, ServoReg.DECCEL_TIME]
            self.sync_param_process = True
            for i, val in enumerate(values):
                def set_param_on_motor(*args, **kwargs):
                    try:
                        ans = kwargs['ans']
                        current_val = kwargs['current_val']
                        register = kwargs['register']
                        # set_param if difference
                        if (ans[:7] == ':010302' and int(ans[7:11], 16) != current_val) or (ans[:7] != ':010302'):
                            try:
                                if current_val < 0:
                                    current_val = 0
                                if i == 0 and current_val == 0:
                                    current_val = 100
                                self.motor.set_param(register=register, value=current_val, right_func=apply_param)
                            except:
                                self.error('error set param on motor in if')
                    except:
                        self.error('error set param on motor')

                self.motor.get_param(register=registers[i], right_func=set_param_on_motor, current_val=val)

            try:
                self.auto_work_time = int(self.work_time.get())
            except:
                pass
            self.save_params()
            self.enable_buttons(self.switch_motor.val)

    def param_changed(self):
        values = ['speed', 'accel_time', 'deccel_time']
        for val in values:
            if eval('self.' + str(self.mode) + '_' + str(val) +'!=self.' + str(val) + '.get()')or\
                    (self.auto_work_time!=self.work_time.get()):
                self.image_speed_error.place(x=230, y=50)


    def param_change_complete(self):
        values = ['speed', 'accel_time', 'deccel_time']
        for val in values:
            if eval('self.' + str(self.mode) + '_' + str(val) +'!=self.' + str(val) + '.get()')or\
                    (self.auto_work_time!=self.work_time.get()):
                self.save_params()
                self.servo_set_params()
                if self.mode == 'auto':
                    self.auto_presets_id = -1
                else:
                    self.manual_presets_id = -1
                break

        if (self.mode == 'auto' and self.auto_presets_id == -1)or\
                (self.mode == 'manual' and self.manual_presets_id == -1):
            self.preset_var.set('Выбрать пресет')

        self.image_speed_error.place_forget()

    def change_mode(self):
        self.enable_buttons(False)
        if self.mode == 'auto':
            self.mode = 'manual'
            self.auto.hide()
            self.manual.show()
            self.speed.set(self.manual_speed)
            self.accel_time.set(self.manual_accel_time)
            self.deccel_time.set(self.manual_deccel_time)
            id_pres = self.manual_presets_id
        else:
            self.mode = 'auto'
            self.manual.hide()
            self.auto.show()
            self.speed.set(self.auto_speed)
            self.accel_time.set(self.auto_accel_time)
            self.deccel_time.set(self.auto_deccel_time)
            id_pres = self.auto_presets_id

        self.servo_set_params()
        self.update_presets_combobox()
        if id_pres > -1:
            self.combobox_presets.current(id_pres)
        else:
            self.preset_var.set('Выбрать пресет')

    def show_add_preset_window(self):
        self.add_preset_master = Toplevel(self.master)
        self.add_preset_window = AddPresetWindow(self, self.add_preset_master)

    def add_preset(self, name):
        preset = Preset(name, self.speed.get(), self.accel_time.get(), self.deccel_time.get())
        if self.mode == 'auto':
            preset.work_time = self.work_time.get()
            self.auto_presets.append(preset)
        else:
            self.manual_presets.append(preset)

        self.save_presets()
        self.update_presets_combobox()
        index = len(self.combobox_presets['values']) - 1
        self.combobox_presets.current(index)

    def change_preset(self):
        index = self.combobox_presets.current()
        if self.mode == 'auto':
            preset = self.auto_presets[index]
            preset.work_time = self.work_time.get()
        else:
            preset = self.manual_presets[index]
        preset.speed = self.speed.get()
        preset.accel_time = self.accel_time.get()
        preset.deccel_time = self.deccel_time.get()
        self.save_presets()

    def del_preset(self):
        index = self.combobox_presets.current()
        if self.mode == 'auto':
            del self.auto_presets[index]
        else:
            del self.manual_presets[index]
        self.update_presets_combobox()
        self.preset_var.set('Выбрать пресет')
        self.save_presets()

    def preset_selected(self, event):
        index = self.combobox_presets.current()
        if self.mode == 'auto':
            preset = self.auto_presets[index]
            self.auto_speed = preset.speed
            self.auto_accel_time = preset.accel_time
            self.auto_deccel_time = preset.deccel_time
            self.auto_work_time = preset.work_time
            self.auto_presets_id = self.combobox_presets.current()
        else:
            preset = self.manual_presets[index]
            self.manual_speed = preset.speed
            self.manual_accel_time = preset.accel_time
            self.manual_deccel_time = preset.deccel_time
            self.manual_presets_id = self.combobox_presets.current()
        self.speed.set(preset.speed)
        self.accel_time.set(preset.accel_time)
        self.deccel_time.set(preset.deccel_time)
        self.work_time.set(preset.work_time)

        self.servo_set_params()
        self.save_params()

    def update_presets_combobox(self):
        preset_names = []
        if self.mode == 'auto':
            preset_list = self.auto_presets
        else:
            preset_list = self.manual_presets
        for preset in preset_list:
            preset_names.append(preset.name)
        self.combobox_presets['values'] = preset_names

    def show_notify_window(self, title, text):
        self.notify_master = Toplevel(self.master)
        self.notify_window = NotifyWindow(self, self.notify_master, title, text)

    def error(self, text):
        self.show_notify_window('Ошибка', text)

    def set_default_settings(self):
        # self.com = IntVar()
        # self.speed = IntVar()
        # self.accel_time = IntVar()
        # self.deccel_time = IntVar()
        # self.work_time = IntVar()
        # self.preset_var = StringVar()
        self.preset_var.set('Выбрать пресет')
        self.width = 400
        self.height = 320
        self.master.geometry('%dx%d' % (self.width, self.height))
        self.master.resizable(False, False)


    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        self.set_default_settings()
        self.load_params()
        self.load_presets()
        #ui_setup(self)
        self.update_presets_combobox()
        if self.auto_presets_id > -1:
            self.combobox_presets.current(self.auto_presets_id)

        self.auto = AutoMode(self)
        self.manual = ManualMode(self)
        self.auto.show()

        self.btn_connect.bind_release(self.change_connect)

        self.switch_motor.bind_sw(self.motor_change_state)
        self.switch_motor.val = True
        self.switch_motor.change_val()

        self.btn_add_preset.bind_release(self.show_add_preset_window)
        self.btn_change_preset.bind_release(self.change_preset)
        self.btn_del_preset.bind_release(self.del_preset)



if __name__ == '__main__':
    # user32 = windll.user32
    # user32.SetProcessDPIAware()
    root = tk.Tk()
    app = ServolineMotorApp(root)

    root.mainloop()
