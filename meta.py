# -*- coding: utf-8 -*-

import os


class Geometry:
    width = 650
    height = 480

    scr_width = 0
    scr_height = 0

    start_width = 0
    start_height = 0

    @staticmethod
    def set_screen_geometry(w, h):
        Geometry.scr_width = int(w)
        Geometry.start_width = int((Geometry.scr_width / 2) - 325)
        Geometry.scr_height = int(h)
        Geometry.start_height = int((Geometry.scr_height / 2) - 300)

    @staticmethod
    def get_geometry():
        return f"{Geometry.width}x{Geometry.height}+{Geometry.start_width}+{Geometry.start_height}"


class Monitor:
    width = Geometry.width - 50
    height = Geometry.height - 100


links = {
    'github': 'https://github.com/sina-programer',
    'instagram': 'https://www.instagram.com/sina.programer',
    'telegram': 'https://t.me/sina_programer'
}


errors = {
    'empty': 'Address field is empty!',
    'invalid': 'Your image address is invalid!',
    'unsupport': 'Format your file unsupported!'
}

helps = {
    'shortcuts': """
<Enter>  Refresh preview
<Left>     Previous button
<Right>  Next button
<Esc>      Unfocus from address bar to use other shortcuts
<b>         Browse
<s>          Submit
""",

    'preview': """
* Enter the address of your image manualy and <Enter>
* Use browse button to select your image
* Use the next & previous buttons
* Use the presets in menu
""",

    'usage': """
1_ Select desired image(see preview)
2_ in preview you can see and detect if it is a good image
3_ finally click on submit and enjoy your new background
"""
}


title = 'Background Changer'

folder_name = 'Files'
icon_name = 'icon.ico'
main_root = os.getcwd()
folder_path = os.path.join(main_root, folder_name)
icon_path = os.path.join(folder_path, icon_name)


prev_name = 'previous.png'
prev_path = os.path.join(folder_path, prev_name)

next_name = 'next.png'
next_path = os.path.join(folder_path, next_name)


presets_folder_name = r'Files\Presets'
presets_folder = os.path.join(main_root, presets_folder_name)
presets = [os.path.join(presets_folder, f'{i}.jpg') for i in range(10)]
presets_label = [rf'Presets\{i}' for i in range(1, 10)]
presets_label.insert(0, r'Presets\Default')


supported_formats = ('.jpg', '.png', '.gif', '.tiff', '.bmp', '.jpe',
                     '.dib', '.wdp', '.ico', '.jpeg', '.jfif')

file_types = (('All Files', '*'), ('JPG File', '*.jpg'),
              ('JPG File', '*.jpe'), ('JPG File', '*.jpeg'), ('JPG File', '*.jfif'),
              ('PNG File', '*.png'), ('GIF File', '*.gif'),
              ('ICON File', '*.ico'), ('TIFF File', '*.tiff'),
              ('TIFF File', '*.tif'), ('Bitmap File', '*.bmp'),
              ('Bitmap File', '*.dib'), ('Windows Media Photo', '*.wdp'))
