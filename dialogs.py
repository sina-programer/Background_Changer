# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import simpledialog, messagebox

import webbrowser
import winsound

import meta


class AboutDialog(simpledialog.Dialog):
    def __init__(self, parent):
        winsound.MessageBeep()
        super().__init__(parent, 'About us')

    def body(self, frame):
        tk.Label(self, text='This program made by Sina.f').pack(pady=12)
        kwargs = {'row': 1, 'padx': 10, 'pady': 5}

        tk.Button(frame, text='GitHub', width=9, command=lambda: webbrowser.open(meta.links['github'])).grid(column=1, **kwargs)
        tk.Button(frame, text='Instagram', width=9, command=lambda: webbrowser.open(meta.links['instagram'])).grid(column=2, **kwargs)
        tk.Button(frame, text='Telegram', width=9, command=lambda: webbrowser.open(meta.links['telegram'])).grid(column=3, **kwargs)

        self.geometry('300x100')
        self.resizable(False, False)

        return frame

    def buttonbox(self):
        pass
