# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox

from ctypes import windll, c_char_p
from PIL import Image, ImageTk

import subprocess
import winreg
import os

import meta
import dialogs
import elements


class App:
    __slots__ = ['master', 'presets', 'photos', 'photo',
                 'adrs_bar', 'photo_width_lbl', 'photo_height_lbl',
                 'photo_size_lbl', 'prev_btn', 'next_btn', 'monitor']

    def __init__(self, master):
        self.master = master
        self.master.config(menu=self.init_menu())
        self.set_shortcuts()

        self.presets = self.load_presets()
        self.photos = self.presets.copy()
        self.photo = self.photos[-1]

        # Widgets
        self.adrs_bar = elements.Entry(master, 74, 100, 410)

        self.photo_width_lbl = elements.Label(master, "", 20, 445)
        self.photo_height_lbl = elements.Label(master, "", 150, 445)
        self.photo_size_lbl = elements.Label(master, "", 275, 445)
        elements.Label(master, f"Screen width: {meta.Geometry.scr_width}", 400, 445)
        elements.Label(master, f"Screen height: {meta.Geometry.scr_height}", 530, 445)

        elements.Button(master, 'Browse', self.browse, 565, 406)
        elements.Button(master, 'Submit', self.submit, 20, 407)

        prev_img = tk.PhotoImage(file=meta.prev_path)
        self.prev_btn = tk.Button(self.master, image=prev_img, bd=0, command=lambda: self.slide_left())
        self.prev_btn.place(x=0, y=150)
        next_img = tk.PhotoImage(file=meta.next_path)
        self.next_btn = tk.Button(self.master, image=next_img, bd=0, command=lambda: self.slide_right())
        self.next_btn.place(x=meta.Geometry.width - 25, y=150)

        self.monitor = elements.Monitor(master)
        self.show(self.presets[0])

    def show(self, photo):
        if photo != self.photo:
            if photo.basedir != self.photo.basedir:
                self.photos = self.load_images(photo.basedir)

            self.photo = photo
            self.photo.load_image()

            self.photo_width_lbl.change(f"Photo width: {self.photo.real_dims[0]}")
            self.photo_height_lbl.change(f"Photo height: {self.photo.real_dims[1]}")
            self.update_image_size(self.photo.size)

            self.master.title(f'{meta.title} - {self.photo.title}')
            self.adrs_bar.insert(self.photo.label)

            self.check_index()
            self.monitor.show(self.photo.image)

    def submit(self):
        windll.user32.SystemParametersInfoA(20, 0, c_char_p(self.photo.path.encode()), 0)

        command = rf'reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d "{self.photo.path}" /f'
        cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        cmd.stdin.write('RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters'.encode())

        messagebox.showinfo('Background Changer', 'Your background changed successfully')

    def browse(self):
        ''' this method for browse button '''
        new_path = filedialog.askopenfilename(filetypes=meta.file_types)
        new_path = new_path.replace('/', '\\')

        if new_path:
            if new_path.endswith(meta.supported_formats):
                index = self.get_index(new_path)
                self.show(Photo(new_path, index))

            else:
                messagebox.showwarning('ERROR', meta.errors['unsupport'])

    def relode(self):
        ''' this method for relode preview image with press <Enter> '''
        new_path = self.adrs_bar.get().replace('/', '\\')

        if new_path in meta.presets_label:
            index = meta.presets_label.index(new_path)
            return self.show(self.presets[index])

        if os.path.exists(new_path):
            if new_path.endswith(meta.supported_formats):
                new_photo = Photo(new_path, index=self.get_index(new_path))
                self.show(new_photo)

            else:
                messagebox.showwarning('ERROR', meta.errors['unsupport'])

        else:
            messagebox.showwarning('ERROR', meta.errors['invalid'])

    def slide_right(self):
        if self.photo.index != len(self.photos) - 1:
            self.show(self.photos[self.photo.index + 1])

    def slide_left(self):
        if self.photo.index:
            self.show(self.photos[self.photo.index - 1])

    def check_index(self):
        if not self.photo.index:
            self.prev_btn.config(state='disabled')
        else:
            self.prev_btn.config(state='normal')

        if self.photo.index == len(self.photos) - 1:
            self.next_btn.config(state='disabled')
        else:
            self.next_btn.config(state='normal')

    def load_images(self, path):
        if path == meta.presets_folder:
            return self.presets
        else:
            files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(meta.supported_formats)]
            photos = [Photo(file, idx) for idx, file in enumerate(files)]
            return photos

    def load_presets(self):
        presets = []
        for idx, path in enumerate(meta.presets):
            title = f"Preset {idx}" if idx else "Preset Default"
            label = rf"Presets\{idx}" if idx else r"Presets\Default"
            preset = Photo(path, idx, title=title, label=label, is_preset=True)
            presets.append(preset)

        return presets

    def update_image_size(self, size):
        ''' this method update photo size label '''
        KBs = size / 1024
        MBs = KBs / 1024

        if MBs >= 1:
            txt = f"Photo size: {MBs:.2f} MB"
        elif KBs >= 1:
            txt = f"Photo size: {KBs:.1f} KB"
        else:
            txt = f"Photo size: {size:.0f} B"

        self.photo_size_lbl.change(txt)

    def get_current_background(self):
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_READ)
        path, regtype = winreg.QueryValueEx(registry_key, 'WallPaper')
        path = path.replace('/', '\\')
        winreg.CloseKey(registry_key)

        index = self.get_index(path)
        basedir, filename = os.path.split(path)
        if basedir == meta.presets_folder:
            return self.presets[index]
        else:
            return Photo(path, index)

    def get_index(self, filepath):
        basepath, basename = os.path.split(filepath)

        if basepath == meta.presets_folder:
            return meta.presets.index(filepath)

        elif basepath == 'Presets':
            if basename == 'Default':
                return 0
            else:
                return int(basename)

        else:
            files = os.listdir(basepath)
            images = [filename for filename in files if filename.endswith(meta.supported_formats)]
            return images.index(basename)

    def hotkey_handler(self, func, *args, **kwargs):
        if not self.adrs_bar.is_active:
            return func(*args, **kwargs)

    def set_shortcuts(self):
        self.master.bind('<Escape>', lambda _: self.adrs_bar.unfocus())
        self.master.bind('<Return>', lambda _: self.relode())
        self.master.bind('<Right>', lambda _: self.hotkey_handler(self.slide_right))
        self.master.bind('<Left>', lambda _: self.hotkey_handler(self.slide_left))
        self.master.bind('<b>', lambda _: self.hotkey_handler(self.browse))
        self.master.bind('<s>', lambda _: self.hotkey_handler(self.submit))

    def init_menu(self):
        menu = tk.Menu(self.master)

        presets_menu = tk.Menu(menu, tearoff=0)
        presets_menu.add_command(label='Current', command=lambda: self.show(self.get_current_background()))
        presets_menu.add_separator()
        presets_menu.add_command(label="Default", command=lambda: self.show(self.presets[0]))
        presets_menu.add_separator()
        presets_menu.add_command(label="Preset 1", command=lambda: self.show(self.presets[1]))
        presets_menu.add_command(label="Preset 2", command=lambda: self.show(self.presets[2]))
        presets_menu.add_command(label="Preset 3", command=lambda: self.show(self.presets[3]))
        presets_menu.add_command(label="Preset 4", command=lambda: self.show(self.presets[4]))
        presets_menu.add_command(label="Preset 5", command=lambda: self.show(self.presets[5]))
        presets_menu.add_command(label="Preset 6", command=lambda: self.show(self.presets[6]))
        presets_menu.add_command(label="Preset 7", command=lambda: self.show(self.presets[7]))
        presets_menu.add_command(label="Preset 8", command=lambda: self.show(self.presets[8]))
        presets_menu.add_command(label="Preset 9", command=lambda: self.show(self.presets[9]))
        
        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label='Shortcuts', command=lambda: messagebox.showinfo('Shortcuts', meta.helps['shortcuts']))
        help_menu.add_command(label='Preview', command=lambda: messagebox.showinfo('Preview', meta.helps['preview']))
        help_menu.add_command(label='Usage', command=lambda: messagebox.showinfo('Usage', meta.helps['usage']))

        menu.add_cascade(label='Presets', menu=presets_menu)
        menu.add_cascade(label='Help', menu=help_menu)
        menu.add_command(label="About us", command=lambda: dialogs.AboutDialog(self.master))

        return menu


class Photo:
    __slots__ = ['path', 'basedir', 'filename', 'basename', 'extension', 'size',
                 'index', 'title', 'label', 'is_preset', 'image', 'real_dims', 'dims']

    def __init__(self, path, index, title=None, label=None, is_preset=False):
        self.path = path.replace('/', '\\')
        self.basedir, self.filename = os.path.split(self.path)
        self.basename, self.extension = os.path.splitext(self.filename)
        self.size = os.path.getsize(self.path)

        self.index = index
        self.title = title if title else self.filename  # show in app title
        if len(self.title) > 40:
            self.title = f'{self.title[:37]}...'
        self.label = label if label else self.path  # show in entry
        self.is_preset = is_preset

        self.image = None
        self.real_dims = None
        self.dims = None

    def load_image(self):
        if not self.image:
            self.image = Image.open(self.path)
            self.real_dims = self.image.size
            self.resize()  # set self.dims & self.image in self.resize()

    def resize(self):
        self.dims = tuple(self.get_new_dims())
        self.image = ImageTk.PhotoImage(self.image.resize(self.dims))

    def get_new_dims(self):
        dims = list(self.real_dims)
        if (ratio := dims[0] / elements.Monitor.width) > 1:
            dims[0] = int(dims[0] / ratio)
            dims[1] = int(dims[1] / ratio)

        if (ratio := dims[1] / elements.Monitor.height) > 1:
            dims[0] = int(dims[0] / ratio)
            dims[1] = int(dims[1] / ratio)

        return dims

    def __eq__(self, obj):
        if self.path == obj.path:
            return True
        else:
            return False
