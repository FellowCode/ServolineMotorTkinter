class Preset:
    work_time = 0
    def __init__(self, name, speed, accel_time, deccel_time):
        self.name = name
        self.speed = speed
        self.accel_time = accel_time
        self.deccel_time = deccel_time