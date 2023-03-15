import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'gif', 'tif', 'bmp', 'png', 'pcx'}


def get_image_files(folder):
    image_files = []
    for file in os.listdir(folder):
        if file.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
            image_files.append(file)
    return image_files


def get_image_info(file_path):
    image = Image.open(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    file_type = image.format
    size = f"{image.width}x{image.height}"
    dpi = image.info.get('dpi')
    if dpi is not None:
        h_dpi, v_dpi = dpi
    else:
        h_dpi, v_dpi = '96', '96'
    if h_dpi == v_dpi == 0:
        h_dpi = v_dpi = 96
    mode = image.mode
    if mode == 'L':
        mode = 8
    elif mode == 'RGB':
        mode = 24
    elif mode == 'RGBA':
        mode = 32
    compression = image.info.get('compression')
    if compression is None:
        compression = '-1'
    return file_name, file_type, size, h_dpi, v_dpi, mode, compression


def choose_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:

        for row in data_table.get_children():
            data_table.delete(row)

        image_files = get_image_files(folder_path)

        for file in image_files:
            file_path = os.path.join(folder_path, file)
            info = get_image_info(file_path)
            data_table.insert('', 'end', values=info)


root = tk.Tk()
root.title('Image Info Reader')

data_table = tk.ttk.Treeview(root, columns=(
    'File Name', 'File Type', 'Image Size', 'H Resolution (dpi)',
    'V Resolution (dpi)', 'Color Depth', 'Compression'))

data_table.heading('#1', text='File Name')
data_table.heading('#2', text='File Type')
data_table.heading('#3', text='Image Size')
data_table.heading('#4', text='H Resolution (dpi)')
data_table.heading('#5', text='V Resolution (dpi)')
data_table.heading('#6', text='Color Depth')
data_table.heading('#7', text='Compression')
data_table.column('#0', width=1)
data_table.column('#1', width=200, anchor='center')
data_table.column('#2', width=100, anchor='center')
data_table.column('#3', width=100, anchor='center')
data_table.column('#4', width=120, anchor='center')
data_table.column('#5', width=120, anchor='center')
data_table.column('#6', width=100, anchor='center')
data_table.column('#7', width=120, anchor='center')

data_table_scrollbar = tk.Scrollbar(root, orient='vertical', command=data_table.yview)
data_table.configure(yscrollcommand=data_table_scrollbar.set)

choose_folder_button = tk.Button(root, text='选择文件夹', command=choose_folder)

data_table.pack(side='left', fill='both', expand=True)
data_table_scrollbar.pack(side='right', fill='y')
choose_folder_button.pack(side='bottom', pady=10)

root.mainloop()
