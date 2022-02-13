import tkinter as tk
import winsound
import os

import meta
import model


if __name__ == "__main__":
    root = tk.Tk()
    meta.Geometry.set_screen_geometry(root.winfo_screenwidth(), root.winfo_screenheight())

    root.title(meta.title)
    root.geometry(meta.Geometry.get_geometry())
    root.resizable(False, False)
    root.focus_force()

    if os.path.exists(meta.folder_path):
        root.iconbitmap(default=meta.icon_path)
        app = model.App(root)

    else:
        winsound.MessageBeep()
        tk.Label(root, text='ERROR: Please run the app in the default folder!', fg='red').pack()

        root.mainloop()
