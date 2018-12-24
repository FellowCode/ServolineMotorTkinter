class File:

    def open(self, do='r'):
        self.file = open(self.path, do)

    def close(self):
        self.file.close()

    def save_param(self, tag, value):
        self.file.write(tag + str(value))

    def write_mark(self, tag):
        self.file.write('############\n' + tag.upper() + '############\n')

    def load_param(self, tag):
        pass

    def __init__(self, path):
        self.path = path