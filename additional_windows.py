import tkinter.ttk as ttk
from tkinter import *
from design import *
import tkinter as tk

class AdditionalWindow:
    width = 300
    height = 100

    def __init__(self, app, master):
        self.posx = app.master.winfo_x() + (app.width - self.width) / 2
        self.posy = app.master.winfo_y() + (app.height - self.height) / 2
        master.geometry('%dx%d+%d+%d' % (self.width, self.height, self.posx, self.posy))
        self.master = master

        self.master.bind('<ntilde>', self.copy)
        self.master.bind('<igrave>', self.paste)
        self.master.root.bind('<Control-Cyrillic_em>', self.paste)

    @staticmethod
    def copy(event):
        widget = event.widget
        try:
            start = widget.index("sel.first")
            end = widget.index("sel.last")
        except tk.TclError:
            pass
        else:
            widget.clipboard_clear()
            widget.clipboard_append(widget.get(start, end))

    @staticmethod
    def paste(event):
        widget = event.widget
        try:
            start = widget.index("sel.first")
            end = widget.index("sel.last")
            widget.delete(start, end)
        except tk.TclError:
            pass
        clipboard = widget.clipboard_get()
        widget.insert("insert", clipboard)

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


class GroupSettingsWindow(GroupSettingsForm):
    def __init__(self, app, master, group_id=-1):
        self.app = app
        self.group_id=group_id
        super().__init__(app.master, master)

        self.set_title('Группа')

        for preset in self.app.auto_presets:
            self.lb.insert(END, preset.name)

        if self.group_id > -1:
            self.name.set(self.app.auto_groups[self.group_id].name)

        self.bind_buttons()

    def bind_buttons(self):
        self.btn_save.configure(command=self.save)
        self.btn_delete.configure(command=self.delete)

    def save(self):
        preset_ids = list(self.lb.curselection())
        self.app.save_group(self.name.get(), preset_ids, group_id=self.group_id)
        self.close()

    def delete(self):
        self.app.delete_group(self.group_id)
        self.close()


class PresetSettingsWindow(PresetSettingsForm):
    def __init__(self, app, master, preset):
        self.app = app
        self.preset = preset
        super().__init__(app.master, master)
        self.set_title('Пресет')
        self.bind_buttons()
        self.set_vars()


    def bind_buttons(self):
        self.btn_save.configure(command=self.save)
        self.btn_delete.configure(command=self.delete)

    def set_vars(self):
        self.name.set(self.preset.name)
        self.speed.set(self.preset.speed)
        self.accel_time.set(self.preset.accel_time)
        self.deccel_time.set(self.preset.deccel_time)
        self.work_time.set(self.preset.work_time)

    def save(self):
        self.preset.name = self.name.get()
        self.preset.speed = self.speed.get()
        self.preset.accel_time = self.accel_time.get()
        self.preset.deccel_time = self.deccel_time.get()
        self.work_time = self.work_time.get()

        self.app.save_preset(self.preset)

        self.close()

    def delete(self):
        self.app.del_preset()
        self.close()


