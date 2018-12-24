import tkinter.ttk as ttk
from tkinter import *
from design import ui_notify_window, ui_add_preset_window

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

class NotifyWindow(AdditionalWindow):
    def __init__(self, app, title, text):
        self.app = app
        self.master = app.notify_master
        super().__init__(app, self.master)

        self.set_title(title)
        self.text = text

        self.posx = self.app.master.winfo_x() + (self.app.width - self.width)/2
        self.posy = self.app.master.winfo_y() + (self.app.height - self.height)/2
        self.master.geometry('%dx%d+%d+%d' % (self.width, self.height, self.posx, self.posy))

        self.master.resizable(False, False)

        ui_notify_window(self)


class AddPresetWindow(AdditionalWindow):
    def __init__(self, app):
        self.app = app
        self.master = app.add_preset_master
        super().__init__(app, self.master)

        self.set_title('Добавить пресет')

        self.name = StringVar()
        ui_add_preset_window(self)

    def add_preset(self):
        self.app.add_preset(self.name.get())
        self.close()

