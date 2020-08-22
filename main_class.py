# Application language: en
# Author: willy14620
# Import package
import sqlite3
import tkinter as tk
import pandas as pd
import tkinter.messagebox as tkmsg
from tkinter import ttk
from tkcalendar import DateEntry
from os import path

# Solve the problem of displaying Chinese format
pd.set_option('display.unicode.ambiguous_as_wide',True)
pd.set_option('display.unicode.east_asian_width',True)

# Database filename
DBNAME = 'accounting_book.db'
POPUP_EXIST_WIN = False

# Database method
def database_method(method, data=None, bMethod=None):
    global DBNAME
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()

    if method == 'initialize':
        cursor.execute('DROP TABLE IF EXISTS book')
        cursor.execute('CREATE TABLE IF NOT EXISTS book('
                    'id INTEGER PRIMARY KEY, '
                    'method TEXT, '
                    'amount INTEGER, '
                    'notes TEXT,'
                    'date TEXT )')
    elif method == 'insert':
        cursor.execute('INSERT INTO book VALUES(?, ?, ?, ?, ?)', data)
    elif method == 'list':
        cursor.execute('SELECT method, amount, notes, date FROM book WHERE method="{0}"'.format(bMethod))
        df = pd.DataFrame(columns=['Amount', 'Notes', 'Date'])
        for row in cursor.fetchall():
            temp = [row[1], row[2], row[3]]
            df = df.append(pd.Series(temp,df.columns),ignore_index=True)
        if not df.empty:
            print(df)
        else:
            print('尚未有任何資料！')
    elif method == 'update':
        temp = 0
        cursor.execute('SELECT method, amount FROM book')
        for row in cursor.fetchall():
            if row[0] == 'Income':
                temp = temp + row[1]
            elif row[0] == 'Expenditure':
                temp = temp - row[1]
        return temp
    elif method == 'export':
        cursor.execute('SELECT method, amount, notes, date FROM book')
        df = pd.DataFrame(cursor.fetchall(), columns=['income/expenditure','amount','notes','date'])
        df.to_csv('book.csv', index=0)
    conn.commit()
    conn.close()

# Graphical User Interface
class application:
    # Initialize frame
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.config(bg='white')
        self.widget_style()
        self.create_widget()
        self.frame.pack()
    # Widget style
    def widget_style(self):
        ttk.Style().configure('TLabel', font=('Consolas', 12), background='white', foreground='black')
        ttk.Style().configure('r.TLabel', font=('Consolas', 12), width=30, background='white', foreground='black')
        ttk.Style().configure('TButton', font=('Consolas',10), background='white', foreground='black', width=7)
    # Create widget
    def create_widget(self):
        # Label frame
        self.input_group = tk.LabelFrame(self.frame, text='Input Group', padx=10, pady=10, bg='white')
        self.input_group.grid(column=1, row=2, columnspan=100,rowspan=100,pady=10)
        # Label
        self.var_balance = tk.StringVar()
        self.var_balance.set('Balance: (Click update button!)')
        self.amount_lbl = ttk.Label(self.input_group, text='Amount:')
        self.note_lbl = ttk.Label(self.input_group, text='Note:')
        self.date_lbl = ttk.Label(self.input_group, text='Date:')
        self.balance_lbl = ttk.Label(self.frame, textvariable=self.var_balance, style='r.TLabel')
        self.amount_lbl.grid(column=0, row=0)
        self.note_lbl.grid(column=0, row=1)
        self.date_lbl.grid(column=0, row=2)
        self.balance_lbl.grid(column=1, row=0, sticky=tk.W, padx=10)
        # Entry
        self.var_amount = tk.StringVar()
        self.var_note = tk.StringVar()
        self.amount_ety = ttk.Entry(self.input_group, textvariable=self.var_amount)
        self.note_ety = ttk.Entry(self.input_group, textvariable=self.var_note)
        self.amount_ety.grid(column=1, row=0, columnspan=5)
        self.note_ety.grid(column=1, row=1, columnspan=5)
        # ComboBox
        self.control_cb = ttk.Combobox(self.frame, values=['Income','Expenditure'], state='readonly', width=10)
        self.control_cb.current(0)
        self.control_cb.grid(column=1, row=1, sticky=tk.W, padx=10)
        # DateEntry
        self.cal = DateEntry(self.input_group, width=15, bg='white', fg='white', date_pattern='yyyy/MM/dd')
        self.cal.grid(column=1, row=2,sticky='w',columnspan=5)
        # Button
        self.list_btn = ttk.Button(self.frame, text='List', command=self.list_clicked)
        self.export_btn = ttk.Button(self.frame, text='Export', command=self.export_clicked)
        self.update_btn = ttk.Button(self.frame, text='Update', command=self.update_clicked)
        self.initialize_btn = ttk.Button(self.input_group, text='Initialize', command=self.initialize_clicked)
        self.insert_btn = ttk.Button(self.input_group, text='Insert', command=self.insert_clicked)
        self.close_btn = ttk.Button(self.frame, text='Close', command=self.close_clicked)
        self.list_btn.grid(column=0, row=0, padx=5, pady=2.5)
        self.export_btn.grid(column=0, row=1, padx=5, pady=2.5)
        self.update_btn.grid(column=0, row=2, padx=5, pady=2.5)
        self.initialize_btn.grid(column=0, row=3, pady=5)
        self.insert_btn.grid(column=1, row=3, pady=5)
        self.close_btn.grid(column=0, row=3, padx=5, pady=2.5)
    # Button clicked event
    def list_clicked(self):
        global POPUP_EXIST_WIN
        if not POPUP_EXIST_WIN:
            POPUP_EXIST_WIN = True
            self.popup_win = tk.Toplevel(self.master)
            self.popup_win.protocol("WM_DELETE_WINDOW", disable_event)
            self.popup_win.title('Popup Window')
            self.popup_win.geometry('300x70')
            self.popup_win.config(bg='white')
            self.popup_win.resizable(0, 0)
            self.app = popup_window(self.popup_win)
        else:
            return
    def export_clicked(self):
        database_method('export')
    def update_clicked(self):
        result = database_method('update')
        self.var_balance.set('Balance: {0} (TWD)'.format(result))
    def close_clicked(self):
        if tkmsg.askyesno('Tip!','Do you want to close this application?'):    
            self.master.destroy()
    def initialize_clicked(self):
        if tkmsg.askyesno('Initialize','Do you want to initialize database?'):
            database_method('initialize')
    def insert_clicked(self):
        if len(self.var_amount.get()) > 0 and len(self.var_note.get()) and len(self.cal.get()):
            data = (None, self.control_cb.get(), int(self.var_amount.get()), self.var_note.get(), self.cal.get())
            database_method('insert', data)
        else:
            tkmsg.showerror('Error','Input entry cannnot be empty, please fill in completely!')

class popup_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.config(bg='white')
        self.create_widget()
        self.frame.pack()
    def create_widget(self):
        # Label
        self.top_text = ttk.Label(self.frame, text='Choose you want to see')
        self.top_text.grid(column=0, row=0, columnspan=3, sticky=tk.E+tk.W, padx=15)

        # Button
        ttk.Style().configure('e.TButton',font=('Consolas', 10), background='white', foreground='black', width=12)
        self.income_btn = ttk.Button(self.frame, text='Income', command=self.ib_clicked)
        self.expenditure_btn = ttk.Button(self.frame, text='Expenditure', command=self.eb_clicked, style='e.TButton')
        self.close_btn = ttk.Button(self.frame, text='Close', command=self.close_clicked)
        self.income_btn.grid(column=0,row=1,padx=5)
        self.expenditure_btn.grid(column=1,row=1,padx=5)
        self.close_btn.grid(column=2,row=1,padx=5)
    
    # Button clicked
    def ib_clicked(self):
        database_method('list', bMethod='Income')
    def eb_clicked(self):
        database_method('list', bMethod='Expenditure')
    def close_clicked(self):
        global POPUP_EXIST_WIN
        if tkmsg.askyesno('Tip!','Do you want to close popup window?'):    
            POPUP_EXIST_WIN = False
            self.master.destroy()

def disable_event():
    tkmsg.showinfo('Tip','Please click close button to close this application!')

def main():
    root = tk.Tk()
    root.title('Bookkeeping')
    root.geometry('400x240+250+250')
    root.protocol("WM_DELETE_WINDOW", disable_event)
    root.config(bg='white')
    root.resizable(0, 0)
    app = application(root)
    if not path.isfile('./accounting_book.db'):
        tkmsg.showinfo('Tip','First open this application must click initial button\n, otherwise it will go wrong!')
    root.mainloop()

# Main
if __name__ == '__main__':
    main()