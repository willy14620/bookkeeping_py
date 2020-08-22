# import package
import sqlite3
import os
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

# update result
def print_update():
    global DBNAME
    result = 0
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute('SELECT mode, amount FROM acbook')
    for row in cursor.fetchall():
        if row[0] == 'income':
            result = result + row[1]
        elif row[0] == 'expenditure':
            result = result - row[1]
    var_remain.set('餘額: {0}元'.format(result))
    conn.commit()
    conn.close()

# export to csv file
def export_csvfile():
    global DBNAME
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    cursor.execute('SELECT mode, amount, notes, date FROM acbook')
    df = pd.DataFrame(cursor.fetchall(),columns=['支出/收入','金額', '備註', '日期'])
    df.to_csv('記帳簿.csv',index=0)
    conn.commit()
    conn.close()

cn2en_dict = {'收入':'income' ,'支出':'expenditure'}

## button function
# create button clicked
def create_clicked():
    if tkmsg.askyesno('初始化','確定要初始化?'):
        create_table()
    else:
        return

# insert button clicked
def insert_clicked():
    if len(var_amount.get()) > 0 and len(var_description.get()) > 0 and len(cal.get()) > 0:
        data = (None, cn2en_dict[control_cb.get()], int(var_amount.get()), var_description.get(), cal.get())
        insert_data(data)
    else:
        tkmsg.showerror('錯誤','輸入不得為空值，請填寫完整！')
    
    var_amount.set('')
    var_description.set('')

pop_win_exist = False

# search button clicked
def list_clicked():
    global pop_win_exist
    if pop_win_exist:
        print('here')
        return
    else:
        pop_win_exist = True
        # create pop window
        pop_win = tk.Toplevel()
        pop_win.title('')
        pop_win.geometry('180x60+500+500')
        pop_win.config(bg='white')
        pop_win.resizable(0, 0)
        # pop_win.grab_set()

        # label
        top_text = ttk.Label(pop_win, text='請選擇要查看的列表')
        top_text.grid(column=0, row=0, columnspan=3, sticky=tk.E+tk.W,padx=15)
        
        # when button clicked
        def ib_clicked():
            print_list('income')
        def eb_clicked():
            print_list('expenditure')
        def qt_clicked():
            global pop_win_exist
            pop_win_exist = False
            pop_win.destroy()

        # button
        income_btn = ttk.Button(pop_win, text='收入', command=ib_clicked)
        expenditure_btn = ttk.Button(pop_win, text='支出', command=eb_clicked)
        quit_btn = ttk.Button(pop_win, text='離開', command=qt_clicked)
        income_btn.grid(column=0,row=1,padx=5)
        expenditure_btn.grid(column=1,row=1,padx=5)
        quit_btn.grid(column=2,row=1,padx=5)

# update button clicked
def update_clicked():
    print_update()

# export button clicked
def export_clicked():
    export_csvfile()


# graphical user interface
app = tk.Tk()
app.title('記帳')
app.geometry('300x200+250+250')
app.config(bg='white')
app.resizable(0,0)

# widget

## label frame

input_group = tk.LabelFrame(app, text='輸入',padx=10,pady=10,bg='white')
input_group.grid(column=1,row=1,columnspan=100,rowspan=100,padx=10)

## label
var_remain = tk.StringVar()
ttk.Style().configure('TLabel',font=('微軟正黑體',12), background='white')
amount_lbl = ttk.Label(input_group, text='金額:')
description_lbl = ttk.Label(input_group, text='備註:')
date_lbl = ttk.Label(input_group, text='日期:')
remain_lbl = ttk.Label(app, textvariable=var_remain)
amount_lbl.grid(column=0, row=0)
description_lbl.grid(column=0, row=1)
date_lbl.grid(column=0, row=2)
remain_lbl.grid(column=2,row=0,padx=2.5)
var_remain.set('餘額: (點擊更新鍵)')

## entry
var_amount = tk.StringVar()
var_description = tk.StringVar()
amount_ety = ttk.Entry(input_group, textvariable=var_amount)
description_ety = ttk.Entry(input_group, textvariable=var_description)
amount_ety.grid(column=1, row=0,columnspan=5)
description_ety.grid(column=1, row=1,columnspan=5)

## combobox
values = ['收入','支出']
control_cb = ttk.Combobox(app, values=values, state='readonly',width=5)
control_cb.current(0)
control_cb.grid(column=1,row=0,sticky='w',padx=10)

## button
ttk.Style().configure('TButton',font=('微軟正黑體',10), width=5)
ttk.Style().map("TButton",foreground=[('pressed', '#323232'), ('active', 'blue')],background=[('pressed', '#323232'), ('active', 'blue')])
create_btn = ttk.Button(input_group, text='初始化', command=create_clicked)
insert_btn = ttk.Button(input_group, text='新增', command=insert_clicked)
list_btn = ttk.Button(app, text='列表', command=list_clicked)
export_btn = ttk.Button(app, text='匯出', command=export_clicked)
update_btn = ttk.Button(app, text='更新', command=update_clicked)
create_btn.grid(column=0,row=3,pady=5)
insert_btn.grid(column=1,row=3,pady=5)
list_btn.grid(column=0,row=0,padx=5,pady=2.5)
export_btn.grid(column=0,row=1,padx=5,pady=2.5)
update_btn.grid(column=0,row=2,padx=5,pady=2.5)

## date picker
cal = DateEntry(input_group,width=15,bg="white",fg="white", date_pattern='yyyy/MM/dd')
cal.grid(column=1, row=2,sticky='w',columnspan=5)

# first open 
if not os.path.isfile('./accounting_book.db'):
    tkmsg.showinfo('提示!','第一次使用請先點擊初始化!')

# main 
if __name__ == '__main__':
    # gui start
    app.mainloop()
    