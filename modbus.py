import serial
from commands import *
from threading import Thread
from queue import Queue
import time

q = Queue()

class Command:
    def func(self, *args, **kwargs):
        if 'right_func' in self.kw and self.kw['right_func']:
            self.kw['right_func'](*args, **kwargs)

    def __init__(self, **kwargs):
        self.cm = kwargs['cm']
        self.kw = kwargs
        # self.right_ans = kwargs['right_ans']
        # self.error_func = kwargs['error_func']
        # self.right_func = kwargs['func']
        # self.register = kwargs['register']

    def error(self, *args, **kwargs):
        if 'error_func' in self.kw and self.kw['error_func']:
            self.kw['error_func'](*args, **kwargs)

class SendCommandThread(Thread):
    work = True

    def __init__(self, ser, app):
        """Инициализация потока"""
        Thread.__init__(self)
        self.ser = ser
        self.app = app
        self.daemon = True

    def run(self):
        while self.work:
            time.sleep(0.01)
            if q.not_empty:
                try:
                    command = q.get()
                    print('send', command.cm[:-2])
                    self.ser.write(command.cm.encode('utf-8'))
                    ans = self.ser.readline().decode('utf-8')[:-2]
                    print('get ', ans)
                    if 'right_ans' in command.kw:
                        right_ans = command.kw['right_ans'][:-2]
                    else:
                        right_ans = None
                    kw = command.kw
                    kw['ans'] = ans
                    kw['right_ans'] = right_ans
                    command.func(**kw)
                    if 'right_ans' in command.kw and command.kw['right_ans'] and command.kw['right_ans'][:-2] != ans:
                        command.error()
                    q.task_done()
                except:
                    if self.work:
                        self.app.error('Потеряно соединение с двигателем')
                    q.empty()


class Modbus:
    is_connect = False

    def connect(self, com_num, app):
        if not self.is_connect:
            try:
                self.ser = serial.Serial('COM' + str(com_num), 57600, timeout=1, parity=serial.PARITY_ODD)
                print(self.ser)
                self.is_connect = True
                self.command_worker = SendCommandThread(self.ser, app)
                self.command_worker.start()
                self.JOG_On()
                if self.is_connect:
                    self.servo_off()
            except:
                self.is_connect = False

    def disconnect(self):
        if self.is_connect:
            self.servo_off()
            self.JOG_Off()
            time.sleep(0.1)
            self.command_worker.work = False
            self.is_connect = False
            self.ser.close()


    def send_command(self, **kwargs):
        command = Command(**kwargs)
        q.put(command)

    def set_param(self, **kwargs):
        kwargs['cm'] = set_param_command(kwargs['register'], kwargs['value'])
        kwargs['right_ans'] = kwargs['cm']
        command = Command(**kwargs)
        q.put(command)

    def get_param(self, **kwargs):
        cm = get_param_command(kwargs['register'])
        kwargs['cm'] = cm
        command = Command(**kwargs)
        q.put(command)

    def JOG_On(self):
        cm = JOG_on_command()
        self.send_command(cm=cm, right_ans=':0103020032C8')

    def JOG_Off(self):
        cm = JOG_off_command()
        self.send_command(cm=cm, right_ans=':011009000003E3')

    def servo_on(self, **kwargs):
        kwargs['cm'] = servo_on_command()
        kwargs['right_ans'] = kwargs['cm']
        command = Command(**kwargs)
        q.put(command)

    def servo_off(self):
        cm = servo_off_command()
        self.send_command(cm=cm, right_ans=cm)

    def servo_forward_start(self):
        cm = servo_forward_start_command()
        self.send_command(cm=cm, right_ans=cm)

    def servo_forward_stop(self):
        cm = servo_forward_stop_command()
        self.send_command(cm=cm, right_ans=cm)

    def servo_reverse_start(self):
        cm = servo_reverse_start_command()
        self.send_command(cm=cm, right_ans=cm)

    def servo_reverse_stop(self):
        cm = servo_reverse_stop_command()
        self.send_command(cm=cm, right_ans=cm)