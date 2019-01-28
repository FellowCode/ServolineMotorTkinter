from threading import Thread
from time import sleep
from serial import Serial


class EndstopListener(Thread):
    work = True
    motorIsStoped = False

    def __init__(self, app, ser):
        self.daemon = True
        super().__init__()
        self.app = app
        self.ser = ser

    def run(self):
        while self.work:
            if self.ser.is_open and self.ser.inWaiting():
                s = self.ser.readline().decode('utf-8').strip()
                if s == 'stop':
                    self.app.motor_stop()
                    counter = 0
                    while not self.motorIsStoped and counter < 50:
                        counter += 1
                        sleep(0.001)
                    if self.motorIsStoped:
                        self.ser.write('motor stop'.encode('utf-8'))
                elif s=='endstop OK':
                    self.app.es_update_status()
