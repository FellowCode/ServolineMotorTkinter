import tkinter.ttk as ttk
from tkinter import *
from design import *

class AdditionalWindow:
    width = 300
    height = 100

    def __init__(self, app, master):
        self.posx = app.master.winfo_x() + (app.width - self.width) / 2
        self.posy = app.master.winfo_y() + (app.height - self.height) / 2
        master.geometry('%dx%d+%d+%d' % (self.width, self.height, self.posx, self.posy))
        self.master = master

    def set_title(self, title):
        self.master.winfo_toplevel().title(title)

    def close(self):
        self.master.destroy()

class NotifyWindow(NotifyForm):
    def __init__(self, app, master, title, text):
        super().__init__(app.master, master)
        self.set_title(title)
        self.set_text(text)


class AddPresetWindow(AddPresetForm):
    def __init__(self, app, master):
        self.app = app
        super().__init__(app.master, master)

        self.set_title('Добавить пресет')

    def add_preset(self):
        self.app.add_preset(self.name.get())
        self.close()

