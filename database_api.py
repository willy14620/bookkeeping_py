# Author: willy14620
# Import package
import sqlite3
import pandas as pd
from tkinter import filedialog

# Solve the problem of displaying Chinese format
pd.set_option('display.unicode.ambiguous_as_wide',True)
pd.set_option('display.unicode.east_asian_width',True)

# Database filename
DBNAME = 'accounting_book.db'

# Database method
def database_method(method, data=None, bMethod=None):
    global DBNAME
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()

    # Initialize database
    if method == 'initialize':
        cursor.execute('DROP TABLE IF EXISTS book')
        cursor.execute('CREATE TABLE IF NOT EXISTS book('
                    'id INTEGER PRIMARY KEY, '
                    'method TEXT, '
                    'amount INTEGER, '
                    'notes TEXT,'
                    'date TEXT )')
    
    # Insert data to the table of database
    elif method == 'insert':
        cursor.execute('INSERT INTO book VALUES(?, ?, ?, ?, ?)', data)
    
    # Select data from the table of database, then show list on terminal
    elif method == 'list':
        df = pd.DataFrame(columns=['Amount', 'Notes', 'Date'])
        print('_'*15 + '{0}'.format(bMethod) + '_'*15 + '\n')
        if bMethod == 'Both':
            cursor.execute('SELECT method, amount, notes, date FROM book ORDER BY date DESC')
            for row in cursor.fetchall():
                temp = [row[1], row[2], row[3]]
                df = df.append(pd.Series(temp,df.columns),ignore_index=True)

        else:
            cursor.execute('SELECT method, amount, notes, date FROM book WHERE method="{0}" ORDER BY date DESC'.format(bMethod))
            for row in cursor.fetchall():
                temp = [row[1], row[2], row[3]]
                df = df.append(pd.Series(temp,df.columns),ignore_index=True)
        
        # Determine whether the dataframe has any data
        if not df.empty:
            print('{0}\n'.format(df))
        else:
            print('尚未有任何資料！\n')

    # Show the balance on GUI
    elif method == 'update':
        temp = 0
        cursor.execute('SELECT method, amount FROM book')
        for row in cursor.fetchall():
            if row[0] == 'Income':
                temp = temp + row[1]
            elif row[0] == 'Expenditure':
                temp = temp - row[1]
        return temp

    # Export csv file
    elif method == 'export':
        filepath =  filedialog.asksaveasfilename(initialfile='book', defaultextension='.csv', initialdir = "/", title = "Save as", filetypes = (("csv files","*.csv"),("all files","*.*")))
        
        if bMethod == 'Both':
            cursor.execute('SELECT method, amount, notes, date FROM book ORDER BY date DESC')
            df = pd.DataFrame(cursor.fetchall(), columns=['income/expenditure','amount','notes','date'])
            df.to_csv(filepath, index=0)
        else:
            cursor.execute('SELECT method, amount, notes, date FROM book WHERE method="{0}" ORDER BY date DESC'.format(bMethod))
            df = pd.DataFrame(cursor.fetchall(), columns=['income/expenditure','amount','notes','date'])
            df.to_csv(filepath, index=0)
    
    # Show total spend in a week
    elif method == 'weekly':
        # cursor.execute('SELECT datetime(\'now\',\'start of day\',\'-7 day\',\'weekday 1\')') MONDAY
        # cursor.execute('SELECT datetime(\'now\',\'start of day\',\'+0 day\',\'weekday 1\')') SUNDAY
        income_result = 0
        expenditure_result = 0
        df = pd.DataFrame(columns=['Amount', 'Notes', 'Date'])
        cursor.execute('SELECT method, amount, date FROM book where date >= datetime(\'now\',\'start of day\',\'-7 day\',\'weekday 1\') AND date < datetime(\'now\',\'start of day\',\'+0 day\',\'weekday 1\') ORDER BY date ASC')
        for row in cursor.fetchall():
            if row[0] == 'Income':
                income_result = income_result + row[1]
            elif row[0] == 'Expenditure':
                expenditure_result = expenditure_result + row[1]
            temp = [row[0], row[1], row[2]]
            df = df.append(pd.Series(temp,df.columns),ignore_index=True)
        print(df)
        print('\nIncome in a week: {0}\nExpenditure in a week: {1}\n'.format(income_result,expenditure_result))

    conn.commit()
    conn.close()