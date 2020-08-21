# import package
import sqlite3
import pandas as pd 
import tkinter as tk
import tkinter.messagebox as tkmsg
from tkinter import ttk
from tkcalendar import Calendar,DateEntry

pd.set_option('display.unicode.ambiguous_as_wide',True)
pd.set_option('display.unicode.east_asian_width',True)

# database filename
DBNAME = 'accounting_book.db'

# create table
def create_table():
    global DBNAME
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS acbook')
    cursor.execute('CREATE TABLE IF NOT EXISTS acbook('
               'id INTEGER PRIMARY KEY, '
               'mode TEXT, '
               'amount INTEGER, '
               'notes TEXT, '
               'date TEXT )')
    conn.commit()
    conn.close()

# insert data in table
def insert_data(data):
    global DBNAME
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO acbook VALUES(?, ?, ?, ?, ?)',data)
    conn.commit()
    conn.close()


# print list
def print_list(control):
    global DBNAME
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute('SELECT mode, amount, notes, date FROM acbook WHERE mode="{0}"'.format(control))
    df = pd.DataFrame(columns=['金額', '備註', '日期'])
    for row in cursor.fetchall():
        temp = [row[1], row[2], row[3]]
        df = df.append(pd.Series(temp,df.columns),ignore_index=True)
    if not df.empty:
        print(df)
    else:
        print('尚未有任何資料！')
    conn.commit()
    conn.close()

# print result
def print_result():
    pass

# export to csv file
def export_csvfile():
    global DBNAME
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute('SELECT mode, amount, notes, date FROM acbook')
    df = pd.DataFrame(cursor.fetchall(),columns=['支出/收入','金額', '備註', '日期'])
    df.to_csv('temp.csv',index=0)
    conn.commit()
    conn.close()

cn2en_dict = {'收入':'income' ,'支出':'expenditure'}

## button function
# create button clicked
def create_clicked():
    create_table()

# insert button clicked
def insert_clicked():
    if len(var_amount.get()) > 0 and len(var_description.get()) > 0 and len(cal.get()) > 0:
        data = (None, cn2en_dict[control_cb.get()], int(var_amount.get()), var_description.get(), cal.get())
        insert_data(data)
    else:
        tkmsg.showerror('錯誤','輸入不得為空值，請填寫完整！')
    
    var_amount.set('')
    var_description.set('')

# search button clicked
def list_clicked():
    print_list(cn2en_dict[control_cb.get()])

# result button clicked
def result_clicked():
    print_result()

# export button clicked
def export_clicked():
    export_csvfile()


# graphical user interface
app = tk.Tk()
app.title('記帳')
app.geometry('300x160+250+250')
app.config(bg='white')
app.resizable(0,0)

# widget

## label frame

input_group = tk.LabelFrame(app, text='輸入',padx=10,pady=10,bg='white')
input_group.grid(column=1,row=1,columnspan=5,rowspan=4,padx=10)

## label
ttk.Style().configure('TLabel',font=('微軟正黑體',12), background='white')
amount_lbl = ttk.Label(input_group, text='金額:')
description_lbl = ttk.Label(input_group, text='備註:')
date_lbl = ttk.Label(input_group, text='日期:')
amount_lbl.grid(column=0, row=0)
description_lbl.grid(column=0, row=1)
date_lbl.grid(column=0, row=2)

## entry
var_amount = tk.StringVar()
var_description = tk.StringVar()
amount_ety = ttk.Entry(input_group, textvariable=var_amount)
description_ety = ttk.Entry(input_group, textvariable=var_description)
amount_ety.grid(column=1, row=0)
description_ety.grid(column=1, row=1)

## combobox
values = ['收入','支出']
control_cb = ttk.Combobox(app, values=values, state='readonly',width=5)
control_cb.current(0)
control_cb.grid(column=1,row=0,sticky='w',padx=10)

## button
ttk.Style().configure('TButton',font=('微軟正黑體',10), width=5)
ttk.Style().map("TButton",foreground=[('pressed', '#323232'), ('active', 'blue')],background=[('pressed', '#323232'), ('active', 'blue')])
create_btn = ttk.Button(app, text='初始化', command=create_clicked)
insert_btn = ttk.Button(app, text='新增', command=insert_clicked)
list_btn = ttk.Button(app, text='列表', command=list_clicked)
export_btn = ttk.Button(app, text='匯出', command=export_clicked)
create_btn.grid(column=0,row=0,padx=5,pady=5)
insert_btn.grid(column=0,row=1,padx=5,pady=5)
list_btn.grid(column=0,row=2,padx=5,pady=5)
export_btn.grid(column=0,row=3,padx=5,pady=5)

## date picker
cal = DateEntry(input_group,width=15,bg="white",fg="white",year=2020)
cal.grid(column=1, row=2,sticky='w')

# main 
if __name__ == '__main__':
    app.mainloop()