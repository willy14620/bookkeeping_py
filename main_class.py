# Application language: en
# Author: willy14620
# Import package
import tkinter as tk
import tkinter.messagebox as tkmsg
from tkinter import ttk
from tkcalendar import DateEntry
from os import path
from database_api import database_method

# Determine whether objects exist
LIST_WINDOW = False
EXPORT_WINDOW = False

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
    # Custom widget style
    def widget_style(self):
        ttk.Style().configure('TLabel', font=('Consolas', 12), background='white', foreground='black')
        ttk.Style().configure('a.TLabel', font=('Consolas', 10), background='white', foreground='black')
        ttk.Style().configure('b.TLabel', font=('Consolas', 12), width=32, background='white', foreground='black')
        ttk.Style().configure('TButton', font=('Consolas',10), background='white', foreground='black', width=7)
        ttk.Style().configure('e.TButton',font=('Consolas', 10), background='white', foreground='black', width=12)
        ttk.Style().configure('TRadiobutton', font=('Consolas', 10), background='white', foreground='black')
    # Create widget
    def create_widget(self):
        # Label frame
        self.input_group = tk.LabelFrame(self.frame, text='Input Group', padx=10, pady=10, bg='white')
        self.input_group.grid(column=1, row=1, columnspan=100,rowspan=100,pady=10)
        # Label
        self.var_balance = tk.StringVar()
        self.var_balance.set('Balance: (Click update button!)')
        self.amount_lbl = ttk.Label(self.input_group, text='Amount:')
        self.note_lbl = ttk.Label(self.input_group, text='Note:')
        self.date_lbl = ttk.Label(self.input_group, text='Date:')
        self.balance_lbl = ttk.Label(self.frame, textvariable=self.var_balance, style='b.TLabel')
        self.author_lbl = ttk.Label(self.frame, text='Last Modified: 2020/08/24 Made by Willy14620', style='a.TLabel')
        self.amount_lbl.grid(column=0, row=1)
        self.note_lbl.grid(column=0, row=2)
        self.date_lbl.grid(column=0, row=3)
        self.balance_lbl.grid(column=1, row=0, sticky=tk.W, padx=10)
        self.author_lbl.grid(column=1,row=101, sticky=tk.E)
        # Entry
        self.var_amount = tk.StringVar()
        self.var_note = tk.StringVar()
        self.amount_ety = ttk.Entry(self.input_group, textvariable=self.var_amount)
        self.note_ety = ttk.Entry(self.input_group, textvariable=self.var_note)
        self.amount_ety.grid(column=1, row=1, columnspan=5)
        self.note_ety.grid(column=1, row=2, columnspan=5)
        # ComboBox
        self.control_cb = ttk.Combobox(self.input_group, values=['Income','Expenditure'], state='readonly', width=10)
        self.control_cb.current(0)
        self.control_cb.grid(column=0, row=0, pady=5, sticky=tk.W)
        # DateEntry
        self.cal = DateEntry(self.input_group, width=15, bg='white', fg='white', date_pattern='yyyy-MM-dd')
        self.cal.grid(column=1, row=3,sticky='w',columnspan=5)
        # Button
        self.list_btn = ttk.Button(self.frame, text='List', command=self.list_clicked)
        self.export_btn = ttk.Button(self.frame, text='Export', command=self.export_clicked)
        self.update_btn = ttk.Button(self.frame, text='Update', command=self.update_clicked)
        self.initialize_btn = ttk.Button(self.input_group, text='Initialize', command=self.initialize_clicked)
        self.insert_btn = ttk.Button(self.input_group, text='Insert', command=self.insert_clicked)
        self.weekly_btn = ttk.Button(self.frame, text='Weekly', command=self.weekly_clicked)
        self.close_btn = ttk.Button(self.frame, text='Close', command=self.close_clicked)
        self.list_btn.grid(column=0, row=0, padx=5, pady=2.5)
        self.export_btn.grid(column=0, row=1, padx=5, pady=2.5)
        self.update_btn.grid(column=0, row=2, padx=5, pady=2.5)
        self.initialize_btn.grid(column=0, row=4, pady=5, sticky=tk.E+tk.W)
        self.insert_btn.grid(column=1, row=4, pady=5)
        self.weekly_btn.grid(column=0, row=3, padx=5, pady=2.5)
        self.close_btn.grid(column=0, row=4, padx=5, pady=2.5)
    # Button clicked event
    def list_clicked(self):
        global LIST_WINDOW
        if not LIST_WINDOW:
            LIST_WINDOW = True
            self.popup_list = tk.Toplevel(self.master)
            self.popup_list.protocol("WM_DELETE_WINDOW", disable_event)
            self.popup_list.title('List Window')
            self.popup_list.geometry('300x70')
            self.popup_list.config(bg='white')
            self.popup_list.resizable(0, 0)
            self.app = List_win(self.popup_list)
        else:
            return
    def export_clicked(self):
        global EXPORT_WINDOW
        if not EXPORT_WINDOW:
            EXPORT_WINDOW = True
            self.popup_export = tk.Toplevel(self.master)
            self.popup_export.protocol("WM_DELETE_WINDOW", disable_event)
            self.popup_export.title('Export Window')
            self.popup_export.geometry('300x100')
            self.popup_export.config(bg='white')
            self.popup_export.resizable(0, 0)
            self.app = Export_win(self.popup_export)
        else:
            return
        # database_method('export')
    def update_clicked(self):
        result = database_method('update')
        self.var_balance.set('Balance: {0} (TWD)'.format(result))
    def close_clicked(self):
        if tkmsg.askyesno('Tip!','Do you want to close this application?'):    
            self.master.destroy()
    def weekly_clicked(self):
        database_method('weekly')
    def initialize_clicked(self):
        if tkmsg.askyesno('Initialize','Do you want to initialize database?'):
            database_method('initialize')
    def insert_clicked(self):
        if len(self.var_amount.get()) > 0 and len(self.var_note.get()) and len(self.cal.get()):
            data = (None, self.control_cb.get(), int(self.var_amount.get()), self.var_note.get(), self.cal.get())
            database_method('insert', data)
            self.var_amount.set('')
            self.var_note.set('')
        else:
            tkmsg.showerror('Error','Input entry cannnot be empty, please fill in completely!')

# Custom pop up window
class Popup_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.config(bg='white')
        self.create_widget()
        self.frame.pack()
    def create_widget(self):
        pass

# When List button be clicked, then pop up a window
# Extend  class: Popup_window __init__
class List_win(Popup_window):
    def __init__(self, master):
        super().__init__(master)
    def create_widget(self):
        # Label
        self.top_text = ttk.Label(self.frame, text='Choose what you want to know')
        self.top_text.grid(column=0, row=0, columnspan=4, sticky=tk.E+tk.W, padx=15)

        # Button
        self.income_btn = ttk.Button(self.frame, text='Income', command=self.income_clicked)
        self.expenditure_btn = ttk.Button(self.frame, text='Expenditure', command=self.expenditure_clicked, style='e.TButton')
        self.both_btn = ttk.Button(self.frame, text='Both', command=self.both_clicked)
        self.close_btn = ttk.Button(self.frame, text='Close', command=self.close_clicked)
        self.income_btn.grid(column=0, row=1, padx=1, pady=7.5)
        self.expenditure_btn.grid(column=1, row=1, padx=1, pady=7.5)
        self.both_btn.grid(column=2, row=1, padx=1, pady=7.5)
        self.close_btn.grid(column=3, row=1, padx=1, pady=5)
    
    # Button clicked
    def income_clicked(self):
        database_method('list', bMethod='Income')
    def expenditure_clicked(self):
        database_method('list', bMethod='Expenditure')
    def both_clicked(self):
        database_method('list', bMethod='Both')
    def close_clicked(self):
        global LIST_WINDOW
        if tkmsg.askyesno('Tip!','Do you want to close popup window?'):    
            LIST_WINDOW = False
            self.master.destroy()

# When Export button be clicked, then pop up a window
# Extend  class: Popup_window __init__
class Export_win(Popup_window):

    def __init__(self, master):
        super().__init__(master)
    def create_widget(self):
        # Label
        self.top_text = ttk.Label(self.frame, text='Choose what you want to export')
        self.top_text.grid(column=0, row=0, columnspan=3, sticky=tk.E+tk.W, padx=15)

        # Radiobutton
        self.var_radio = tk.IntVar()
        self.income_rb = ttk.Radiobutton(self.frame, text='Income', variable=self.var_radio, value=1)
        self.expenditure_rb = ttk.Radiobutton(self.frame, text='expenditure', variable=self.var_radio, value=2)
        self.both_rb = ttk.Radiobutton(self.frame, text='Both', variable=self.var_radio, value=3)
        self.income_rb.grid(column=0, row=1, padx=1, pady=5)
        self.expenditure_rb.grid(column=1, row=1, padx=1, pady=5)
        self.both_rb.grid(column=2, row=1, padx=1, pady=5)
        self.income_rb.invoke()

        # Button
        self.confirm_btn = ttk.Button(self.frame, text='Confirm', command=self.confirm_clicked)
        self.close_btn = ttk.Button(self.frame, text='Close', command=self.close_clicked)
        self.confirm_btn.grid(column=0, row=2, padx=1, pady=5)
        self.close_btn.grid(column=1, row=2, padx=1, pady=5, sticky=tk.W)

    # Button clicked
    def confirm_clicked(self):
        if self.var_radio.get() == 1:
            selected = 'Income'
        elif self.var_radio.get() == 2:
            selected = 'Expenditure'
        elif self.var_radio.get() == 3:
            selected = 'Both'
        database_method('export', bMethod=selected)
    def close_clicked(self):
        global EXPORT_WINDOW
        if tkmsg.askyesno('Tip!','Do you want to close popup window?'):    
            EXPORT_WINDOW = False
            self.master.destroy()

# When you click the close icon in the upper right corner, it will pop up a tip window
def disable_event():
    tkmsg.showinfo('Tip','Please click close button to close this application!')

# Initialize application interface and method etc.
def main():
    root = tk.Tk()
    root.title('Book Keeping')
    root.geometry('400x260+250+250')
    # root.protocol("WM_DELETE_WINDOW", disable_event)
    root.config(bg='white')
    root.resizable(0, 0)
    app = application(root)
    if not path.isfile('./accounting_book.db'):
        tkmsg.showinfo('Tip','First open this application must click initial button\n, otherwise it will go wrong!')
    root.mainloop()

# Main
if __name__ == '__main__':
    main()