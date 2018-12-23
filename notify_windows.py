import tkinter.ttk as ttk

class NotifyWindow:
    def __init__(self, app):
        self.app = app
        self.master = app.notify_master

        self.frame = ttk.Frame(self.master)
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)

        print('200x70' +  app.master.geometry()[6:])
        self.master.geometry('200x70' +  app.master.geometry()[3:])
        self.master.resizable(False, False)
        self.master.overrideredirect(True)