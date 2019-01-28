import tkinter.ttk as ttk


class CButton(ttk.Button):
    def bind_release(self, func, args=(), kwargs={}):
        try:
            self.bind('<ButtonRelease-1>', lambda ev: func(*args, **kwargs) if str(self['state']) != 'disabled' else None)
        except:
            print('Error btn binding')

    def bind_hold(self, func_press, func_release):
        try:
            self.bind('<ButtonPress-1>', lambda ev: func_press() if str(self['state']) != 'disabled' else None)
            self.bind('<ButtonRelease-1>', lambda ev: func_release() if str(self['state']) != 'disabled' else None)
        except:
            print('Error btn binding')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SwitchButton(CButton):
    val = False
    func = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['text'] = 'OFF'
        self.bind_release(self.change_val)
        if 'func' in kwargs.keys():
            self.fswitch_func = kwargs['func']

    def change_val(self):
        self.val = not self.val
        if self.val:
            self['text'] = 'ON'
            self['style'] = 'SwitchOn.TButton'
        else:
            self['text'] = 'OFF'
            self['style'] = 'TButton'
        if self.func:
            self.func(self.val)

    def set_val(self, val):
        self.val = not val
        self.change_val()

    def bind_sw(self, func):
        self.func = func


class IntegerEntry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<KeyRelease>', self.entry_changed)

    def entry_changed(self, event):
        for index, char in enumerate(self.get()):
            if not char in '0123456789':
                self.delete(index, index+1)

class ParamEntry(IntegerEntry):
    def __init__(self, *args, **kwargs):
        self.app = kwargs['app']
        del kwargs['app']
        super().__init__(*args, **kwargs)
        self.bind('<FocusOut>', (lambda _: self.app.param_change_complete()))
        self.bind('<Return>', (lambda _: self.app.param_change_complete()))
        self.bind('<KeyRelease>', self.entry_changed)

    def entry_changed(self, event):
        super().entry_changed(event)
        self.app.param_changed()
