import tkinter as tk
from tkinter import ttk
import sqlite3

                            # ГЛАВНОЕ ОКНО
# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

 # Главное окно
    def init_main(self):
        # Панель инструментов
        toolbar = tk.Frame(bg='#d7d7d7', bd = 2)
        # Упаковка
        toolbar.pack(side=tk.TOP, fill=tk.X)

                                  #КНОПКИ
        # Кнопка добавить
        self.img_add = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, text = 'Добавить', bg='#d7d7d7', bd = 1,
                            image=self.img_add, command=self.open_child)
        btn_add.pack(side = tk.LEFT)

        # Кнопка изменить
        self.upd_img = tk.PhotoImage(file='./img/update.png')
        btn_upd = tk.Button(toolbar, text = 'Изменить', bg='#d7d7d7', bd=1, 
                            image=self.upd_img, command=self.open_update_dialog)
        btn_upd.pack(side = tk.LEFT)

       # Кнопка удалить
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_del = tk.Button(toolbar, text = 'Удалить', bg='#d7d7d7', bd=1, 
                            image=self.delete_img, command=self.delete_records)
        btn_del.pack(side = tk.LEFT)

        # Кнопка поиска
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, text = 'Изменить', bg='#d7d7d7', bd=1, 
                            image=self.search_img, command=self.open_search)
        btn_search.pack(side = tk.LEFT)

        # Кнопка обновления
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, text = 'Обновить', bg='#d7d7d7', bd=1,
                            image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side = tk.LEFT)

                                #ТАБЛИЦА
        # Добавление столбцов
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email'),
                                 height=45, show='headings')
        
        # Параметры колонок
        self.tree.column('ID', width = 45, anchor=tk.CENTER)
        self.tree.column('name', width = 300, anchor=tk.CENTER)
        self.tree.column('phone', width = 150, anchor=tk.CENTER)
        self.tree.column('email', width = 150, anchor=tk.CENTER)

        # Название колонок
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')

        # Упаковка
        self.tree.pack(side=tk.LEFT)

        # Ползунок
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

                             # МЕТОДЫ
    # Метод добавления данных
    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()

   # Метод отображения данных
    def view_records (self):
        self.db.cur.execute('''SELECT * FROM users ''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values = row)
        for row in self.db.cur.fetchall()]

    # Метод обновления (изменения) данных
    def update_record(self, name, phone, email):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute(''' UPDATE users SET name=?, phone=?, email=? WHERE ID=?''', 
                            (name, phone, email, id))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления записей
    def delete_records(self):
        #Цикл по выделенным записям
        for row in self.tree.selection():
            # Удаление из БД
            self.db.cur.execute('''DELETE FROM users WHERE ID=?''',
                                (self.tree.set( row, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Метод поиска данных
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute('''SELECT * FROM users WHERE name LIKE ?''', (name, ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end', values=row)
         for row in self.db.cur.fetchall()]

                                   # ВЫЗОВ КЛАССОВ
    # Метод вызывающий дочернее окна
    def open_child(self):
        Child()

    # Метод вызывающий окно изменения(обновления) данных
    def open_update_dialog(self):
        Update()

    # Метод вызывающий окно поиска
    def open_search(self):
        Search()

                     # ДОЧЕРНЕЕ ОКНО
# Окно добавления(дочернее)
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

     # Инициализация виджетов дочернего окна
    def init_child(self):
        # Заголовок окна
        self.title('Добавление контакта')
        # Размер окна
        self.geometry('400x220')
        # Ограничение изменения размеров окна
        self.resizable(False, False)
        # Перехват всех событий, происходящих в приложении
        self.grab_set()
        # Захват фокуса
        self.focus_set()

        # Текст
        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x = 50, y = 50)
        label_phone = tk.Label(self, text='Телефон: ')
        label_phone.place(x = 50, y = 80)
        label_email = tk.Label(self, text='E-mail: ')
        label_email.place(x = 50, y = 110)

        # Виджеты ввода
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x = 200, y = 50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x = 200, y = 80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x = 200, y = 110)

        # Кнопка закрытия дочернего окна
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # Кнопка добавления
        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind('<Button-1>', lambda event:
                    self.view.records(self.entry_name.get(),
                                       self.entry_phone.get(),
                                       self.entry_email.get()))

                            # РЕДАКТИРОВАНИЕ КОНТАКТОВ
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.view = app
        self.db = db
        self.default_data()

    def init_update(self):
        self.title ('Редактировать позицию')
        self.btn_add.destroy()

        self.btn_upd = ttk.Button(self, text="Редактировать")
        self.btn_upd.place(x=200, y=170)
        self.btn_upd.bind('<Button-1>', lambda event:
                    self.view.update_record(self.entry_name.get(),
                                            self.entry_phone.get(),
                                            self.entry_email.get()))
        self.btn_upd.bind('<Button-1>', lambda event: self.destroy(), add='+')

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute(''' SELECT * FROM users WHERE ID=?''', (id, ))
        # Доступ к первой записи из выборки
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])

                                 # ПОИСК
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск по контактам')
        self.geometry('300x100')
        self.resizable(False,False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=20, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=70, y=20)

# Кнопка закрытия
        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=200, y=70)

# Кнопка поиска
        self.btn_search = tk.Button(self, text='Найти')
        self.btn_search.place(x=70, y=70)
        self.btn_search.bind('<Button-1>', lambda event: 
                          self.view.search_records(self.entry_name.get()))
        self.btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

                                # БАЗА ДАННЫХ
# Класс Базы Данных
class DB:
    def __init__(self):
        # Соединение с БД
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY NOT NULL,
                                name TEXT,
                                phone TEXT,
                                email TEXT) """)
        self.conn.commit()

    def insert_data(self, name, phone, email):
        self.cur.execute(""" INSERT INTO users (name, phone, email)
                             VALUES(?, ?, ?)""", (name, phone, email))
        self.conn.commit()

                                  # ЗАПУСК
# Запуск программы
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    # Заголовок окна
    root.title('Список сотрудников в компании')
    # Размер окна
    root.geometry('645x450')
    # Цвет панели
    root.configure(bg ='white')
    # Ограничение изменения размеров окна
    root.resizable(False, False)
    root.mainloop()
