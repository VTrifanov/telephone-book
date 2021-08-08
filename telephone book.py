import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
from tkinter.messagebox import showinfo

def add_contact(): #добавление контакта в БД
    name = app.frame.input_name.get()
    telephone = app.frame.input_telephone.get()

    reqest = f'insert into contacts (name, telephone) values("{name}", "{telephone}")'
    with sqlite3.connect('telephone.db') as db:
        cursor = db.cursor()
        try:
            cursor.execute(reqest)
        except (sqlite3.IntegrityError):
            showinfo(title='Information', message='попробуйте другое имя')
        db.commit()
        app.refresh()

def delete_contact(): # удаление контаката из БД
    reqest = f'delete from contacts where name="{entry}"'
    with sqlite3.connect('telephone.db') as db:
        cursor = db.cursor()
        cursor.execute(reqest)
        db.commit()
        app.refresh()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('телефонная книжка')
        self.geometry('400x430')
        self.put_frame()
        self.put_frame2()
    def put_frame(self):
        self.frame = Frame(self)
        self.frame.grid(row=0, column=0, sticky = tk.EW)
    def put_frame2(self):
        self.frame2 = Frame2(self)
        self.frame2.grid(row=1, column=0)
    def refresh(self):
        self.put_frame()
        self.put_frame2()
        with sqlite3.connect('telephone.db') as db:
            cursor = db.cursor()
            reqest = """select name, telephone from contacts """
            cursor.execute(reqest)
            contacts = []
            for res in cursor:
                contacts.append(res)
            for contact in contacts:
                app.frame2.tree.insert('', tk.END, values=contact)
            db.commit()

class Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.config(bd=10)
        self.label_name = tk.Label(self, text='имя')
        self.label_name.grid(row=0, column=0)
        self.input_name = tk.Entry(self, width=14, font="Arial 12", validate='key', validatecommand=(self.register(self.find_record),'%P'))
        self.input_name.grid(row=1, column=0, padx=5)
        self.label_telephone = tk.Label(self, text='телефон')
        self.label_telephone.grid(row=0, column=1)
        self.input_telephone = tk.Entry(self, width=14, font="Arial 12")
        self.input_telephone.grid(row=1, column=1, padx=5)
        self.button1 = tk.Button(self, text='добавить контакт', command=add_contact)
        self.button1.grid(row=1, column=2)

    def find_record(self, input):
        self.master.put_frame2()
        with sqlite3.connect('telephone.db') as db:
            cursor = db.cursor()
            reqest = f'select name, telephone from contacts where name like "%{input}%" '
            print(reqest)
            cursor.execute(reqest)
            contacts = []
            for res in cursor:
                contacts.append(res)
            for contact in contacts:
                app.frame2.tree.insert('', tk.END, values=contact)
            db.commit()
        return True

class Frame2(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.button2 = tk.Button(self, text='удалить', command=delete_contact)
        self.button2.grid(row=1, column=0, padx = 5, pady = 5, sticky=tk.E)
        self.tree = ttk.Treeview(self, height=15, columns=('#1', '#2'), show='headings')
        self.tree.column('#1', width=185)
        self.tree.column('#2', width=185)
        self.tree.heading('#1', text='Имя')
        self.tree.heading('#2', text='телефон')
        self.tree.bind('<<TreeviewSelect>>', item_selected)
        self.tree.grid(row=0, column=0)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky='ns')


def item_selected(event):
     global entry
     for selected_item in app.frame2.tree.selection():
        item = app.frame2.tree.item(selected_item)
        record = item['values']
        entry = record[0]

app=App()
with sqlite3.connect('telephone.db') as db:
    cursor = db.cursor()
    cursor.execute('CREATE TABLE if NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, telephone TEXT)')
    reqest = """select name, telephone from contacts """
    cursor.execute(reqest)
    contacts = []
    for res in cursor:
        contacts.append(res)
    for contact in contacts:
        app.frame2.tree.insert('', tk.END, values=contact)
    db.commit()


app.mainloop()