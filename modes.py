from design import *
from threading import Timer

class AutoMode:
    reverse = False
    def initial_ui_vars(self):
        self.btn_start = None
        self.btn_stop = None
        self.btn_change_mode = None
        self.switch_reverse = None
        self.label_move_state = None

    def show(self):
        self.app.frame_auto_mode.place(x=0, y=220, relwidth=1, height=100)
        self.app.entry_work_time['state'] = 'normal'

    def hide(self):
        self.app.frame_auto_mode.place_forget()
        self.app.entry_work_time['state'] = 'disabled'

    def start_servo_time_work(self):
        self.motor_timer = Timer(int(self.app.work_time.get()) / 1000, self.stop_servo_time_work)
        self.motor_timer.start()
        self.btn_start['state'] = 'disabled'
        self.switch_reverse['state'] = 'disabled'
        if not self.reverse:
            self.app.motor.servo_forward_start()
        else:
            self.app.motor.servo_reverse_start()

    def stop_servo_time_work(self):
        self.motor_timer.cancel()
        self.btn_start['state'] = 'normal'
        self.switch_reverse['state'] = 'normal'
        if not self.reverse:
            self.app.motor.servo_forward_stop()
        else:
            self.app.motor.servo_reverse_stop()

    def change_reverse(self, value):
        self.reverse = self.app.reverse = value
        if self.reverse:
            self.label_move_state['text'] = 'Движение на себя'
        else:
            self.label_move_state['text'] = 'Движение от себя'
        self.app.save_params()

    def enable_buttons(self, val):
        print('disable buttons')
        if val:
            state = 'normal'
        else:
            state = 'disabled'
        self.btn_start['state'] = state
        self.btn_stop['state'] = state
        #self.btn_change_mode['state'] = state
        self.switch_reverse['state'] = state

    def __init__(self, app):
        self.app = app
        ui_setup_auto_mode(self.app, self)
        self.btn_start.bind_release(self.start_servo_time_work)
        self.btn_stop.bind_release(self.stop_servo_time_work)
        self.btn_change_mode.bind_release(self.app.change_mode)
        self.switch_reverse.bind_sw(self.change_reverse)
        self.switch_reverse.set_val(self.app.reverse)

class ManualMode:

    def initial_ui_vars(self):
        self.btn_forward = None
        self.btn_back = None
        self.btn_change_mode = None

    def show(self):
        self.app.frame_manual_mode.place(x=0, y=220, relwidth=1, height=100)

    def hide(self):
        self.app.frame_manual_mode.place_forget()

    def disable_buttons(self, val):
        if val:
            state = 'normal'
        else:
            state = 'disabled'
        self.btn_forward['state'] = state
        self.btn_back['state'] = state
        #self.btn_change_mode['state'] = state

    def __init__(self, app):
        self.app = app
        ui_setup_manual_mode(app, self)
        self.btn_forward.bind_hold(func_press=self.app.motor.servo_forward_start,
                                   func_release=self.app.motor.servo_forward_stop)
        self.btn_back.bind_hold(func_press=self.app.motor.servo_reverse_start,
                                func_release=self.app.motor.servo_reverse_stop)
        self.btn_change_mode.bind_release(self.app.change_mode)