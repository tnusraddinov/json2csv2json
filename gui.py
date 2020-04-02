import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import json
from pandas.io.json import json_normalize
from pathlib import Path


data_list = []
file_names = []
df = None
root = tk.Tk()
root.title('File Conversion Tool')

canvas1 = tk.Canvas(
    root,
    width=310,
    height=360,
    bg='lightsteelblue2',
    relief='raised')
canvas1.pack()

label1 = tk.Label(
    root,
    text='JSON => CSV',
    bg='lightsteelblue2'
)
label1.config(font=('helvetica', 14))
canvas1.create_window(150, 40, window=label1)


def getJSON():
    global data_list
    global file_names
    global df
    filez = filedialog.askopenfilenames(parent=root, title='Choose JSON files')
    read_files = list(filez)
    file_names = [Path(p).stem for p in read_files]
    for fpath in read_files:
        if Path(fpath).is_file():
            with open(fpath, 'r') as f:
                data = json.load(f)
                data_list.append(data)
        else:
            data_list.append(dict())
    df = json_normalize(data_list)

def convertToCSV():
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    df2 = df.transpose()
    df2.to_csv(export_file_path, header=file_names, index=True)
    msg_success()

browseButton_JSON = tk.Button(
    text="Import JSON Files",
    command=getJSON,
    bg='green',
    fg='white',
    font=('helvetica', 10, 'bold')
)
canvas1.create_window(150, 90, window=browseButton_JSON)

saveAsButton_CSV = tk.Button(
    text='Convert JSON to CSV', 
    command=convertToCSV,
    bg='green', 
    fg='white', 
    font=('helvetica', 10, 'bold'))
canvas1.create_window(150, 130, window=saveAsButton_CSV)


# ========== CSV to JSON
csv_path = None

label1 = tk.Label(
    root,
    text='CSV => JSON',
    bg='lightsteelblue2'
)
label1.config(font=('helvetica', 14))
canvas1.create_window(150, 180, window=label1)

def getCSV():
    global csv_path
    csv_path = filedialog.askopenfilename(parent=root, title='Choose CSV file')


def convertToJSON():
    df2 = pd.read_csv(csv_path, index_col=0)
    col_names = df2.columns.tolist()

    df2 = df2.transpose()
    df2.reset_index(drop=True, inplace=True)
    df2.fillna('', inplace=True)

    dir_path = filedialog.askdirectory()

    # back to nested json (2 level supported)
    for i, row in enumerate(df2.to_dict('r')):
        tmp_dict = {}
        for key, val in row.items():
            if '.' in key:
                key1, key2 = key.split('.')
                if not tmp_dict.get(key1):
                    tmp_dict[key1] = {}
                tmp_dict[key1][key2] = val
            else:
                tmp_dict[key] = val

        with open('{}/{}.json'.format(dir_path, col_names[i]), 'w', encoding='utf8') as f:
            json.dump(tmp_dict, f, ensure_ascii=False)

    msg_success()


browseButton_CSV = tk.Button(
    text="Import CSV File",
    command=getCSV,
    bg='blue',
    fg='white',
    font=('helvetica', 10, 'bold')
)

canvas1.create_window(150, 220, window=browseButton_CSV)

saveAsButton_JSON = tk.Button(
    text='Convert CSV to JSON',
    command=convertToJSON,
    bg='blue',
    fg='white',
    font=('helvetica', 12, 'bold')
)
canvas1.create_window(150, 260, window=saveAsButton_JSON)


def msg_success():
    msg = tk.messagebox.showinfo('Success', 'Conversion is done')


def exitApplication():
    MsgBox = tk.messagebox.askquestion(
        'Exit Application', 'Are you sure you want to exit the application', icon='warning')
    if MsgBox == 'yes':
        root.destroy()


exitButton = tk.Button(
    root, 
    text='Exit',
    command=exitApplication, 
    bg='brown', 
    fg='white', 
    font=('helvetica', 12, 'bold')
)
canvas1.create_window(150, 310, window=exitButton)

root.mainloop()
