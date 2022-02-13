# -*- coding: utf-8 -*-

import tkinter as tk

import meta


class Monitor:
    width = meta.Geometry.width - 50
    height = meta.Geometry.height - 100
    __slots__ = ['master', 'monitor']

    def __init__(self, master):
        self.master = master

        self.monitor = tk.Label(self.master, width=self.width, height=self.height)
        self.monitor.pack(pady=10)

    def show(self, photo):
        self.monitor.config(image=photo)
        self.master.mainloop()


class Entry:
    _hover_color = '#DBDBDB'
    _leave_color = '#F0F0F0'
    __slots__ = ['master', 'is_active', '_variable', 'entry']

    def __init__(self, master, width, x, y):
        self.master = master
        self.is_active = False
        self._variable = tk.StringVar()

        self.entry = tk.Entry(self.master, width=width, textvariable=self._variable)
        self.entry.place(x=x, y=y)
        self.entry.bind('<Enter>', self._hover)
        self.entry.bind('<Leave>', self._leave)

        self.unfocus()

    def _hover(self, event):
        self.is_active = True
        self.entry.config(bg=self._hover_color)
        self.entry.focus_force()

    def _leave(self, event):
        self.entry.config(bg=self._leave_color)

    def unfocus(self):
        self.is_active = False
        self.entry.select_clear()
        self.entry.icursor('end')
        self.master.focus_force()

    def insert(self, text):
        self._variable.set(text)
        self.entry.icursor('end')

    def get(self):
        return self._variable.get()


class Button:
    __slots__ = ['x', 'y', 'button']

    def __init__(self, master, text, func, x, y):
        self.x = x
        self.y = y

        self.button = tk.Button(master, text=text, width=8, height=1, bd=2, command=func)
        self.button.bind('<Enter>', self._hover)
        self.button.bind('<Leave>', self._leave)
        self.button.place(x=self.x, y=self.y)

    def _hover(self, event):
        self.button.config(border=4)
        self.button.place(x=self.x - 2, y=self.y - 2)

    def _leave(self, event):
        self.button.config(border=2)
        self.button.place(x=self.x, y=self.y)


class Label:
    _hover_color = '#0000ee'
    _leave_color = '#000000'
    __slots__ = ['_variable', 'label']

    def __init__(self, master, text, x, y, **kwargs):
        self._variable = tk.StringVar()
        self._variable.set(text)

        self.label = tk.Label(master, textvariable=self._variable, **kwargs)
        self.label.place(x=x, y=y)
        self.label.bind('<Enter>', self._hover)
        self.label.bind('<Leave>', self._leave)

    def _hover(self, event):
        self.label.config(relief='groove', fg=self._hover_color)

    def _leave(self, event):
        self.label.config(relief='flat', fg=self._leave_color)

    def change(self, text):
        self._variable.set(text)
