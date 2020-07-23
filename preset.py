class Preset:
    def __init__(self, name, speed, accel_time, deccel_time):
        self.work_time = 0
        self.name = name
        self.speed = speed
        self.accel_time = accel_time
        self.deccel_time = deccel_time

class Group:
    def __init__(self, name, preset_ids):
        self.name = name
        self.preset_ids = preset_ids