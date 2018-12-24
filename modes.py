from design import *
from threading import Timer, Thread
import time

class AutoMode:
    reverse = False

    btn_start = None
    btn_stop = None
    btn_change_mode = None
    switch_reverse = None
    label_move_state = None
    progressbar_motor = None

    progress_run = False

    def show(self):
        self.app.frame_auto_mode.place(x=0, y=220, relwidth=1, height=100)
        self.app.entry_work_time['state'] = 'normal'

    def hide(self):
        self.app.frame_auto_mode.place_forget()
        self.app.entry_work_time['state'] = 'disabled'

    def motor_progress(self, work_time):
        time_unit = work_time / 100
        stop_pb_step = 5
        stop_time_unit = self.app.deccel_time.get()/(1000*100/stop_pb_step)

        i=0
        while self.progress_run and i<100:
            i+=1
            self.progressbar_motor['value'] = i
            time.sleep(time_unit)
        i=100
        while i>0:
            i-=stop_pb_step
            self.progressbar_motor['value'] = i
            time.sleep(stop_time_unit)

    def start_servo_time_work(self):
        work_time = int(self.app.work_time.get()) / 1000
        self.motor_timer = Timer(work_time, self.stop_servo_time_work)
        self.motor_timer.start()
        self.btn_start['state'] = 'disabled'
        self.switch_reverse['state'] = 'disabled'
        if not self.reverse:
            self.app.motor.servo_forward_start()
        else:
            self.app.motor.servo_reverse_start()

        self.progress_run = True
        self.progressbar_thread = Thread(target=self.motor_progress, args=(work_time,)).start()


    def stop_servo_time_work(self):
        self.motor_timer.cancel()
        self.btn_start['state'] = 'normal'
        self.switch_reverse['state'] = 'normal'
        if not self.reverse:
            self.app.motor.servo_forward_stop()
        else:
            self.app.motor.servo_reverse_stop()
        self.progress_run = False
        self.progressbar_motor['value'] = 0

    def change_reverse(self, value):
        self.reverse = self.app.reverse = value
        if self.reverse:
            self.label_move_state['text'] = 'Движение на себя'
        else:
            self.label_move_state['text'] = 'Движение от себя'
        self.app.save_params()

    def enable_buttons(self, val):
        if val:
            state = 'normal'
        else:
            state = 'disabled'
        self.btn_start['state'] = state
        self.btn_stop['state'] = state
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
    btn_forward = None
    btn_back = None
    btn_change_mode = None

    def show(self):
        self.app.frame_manual_mode.place(x=0, y=220, relwidth=1, height=100)

    def hide(self):
        self.app.frame_manual_mode.place_forget()

    def enable_buttons(self, val):
        if val:
            state = 'normal'
        else:
            state = 'disabled'
        self.btn_forward['state'] = state
        self.btn_back['state'] = state

    def key_forward_btn_press(self):
        if self.app.mode == 'manual':
            if self.btn_forward['state'] == 'normal':
                self.btn_forward.state(['pressed'])
                self.app.motor.servo_forward_start()

    def key_forward_btn_release(self):
        if self.app.mode == 'manual':
            if self.btn_forward['state'] == 'normal':
                self.btn_forward.state(['!pressed'])
                self.app.motor.servo_forward_stop()

    def key_back_btn_press(self):
        if self.app.mode == 'manual':
            if self.btn_back['state'] == 'normal':
                self.btn_back.state(['pressed'])
                self.app.motor.servo_back_start()

    def key_back_btn_release(self):
        if self.app.mode == 'manual':
            if self.btn_back['state'] == 'normal':
                self.btn_back.state(['!pressed'])
                self.app.motor.servo_back_stop()

    def __init__(self, app):
        self.app = app
        ui_setup_manual_mode(app, self)
        self.btn_forward.bind_hold(func_press=self.app.motor.servo_forward_start,
                                   func_release=self.app.motor.servo_forward_stop)
        self.btn_back.bind_hold(func_press=self.app.motor.servo_reverse_start,
                                func_release=self.app.motor.servo_reverse_stop)
        self.btn_change_mode.bind_release(self.app.change_mode)

        self.app.master.bind('<Left>', lambda _:self.key_forward_btn_press())
        self.app.master.bind('<KeyRelease-Left>', lambda _:self.key_forward_btn_release())
        self.app.master.bind('<Right>', lambda _: self.key_back_btn_press())
        self.app.master.bind('<KeyRelease-Right>', lambda _: self.key_back_btn_release())