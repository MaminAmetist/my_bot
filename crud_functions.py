import sqlite3

connection = sqlite3.connect('products.db')
cursor = connection.cursor()

connection_user = sqlite3.connect('users.db')
cursor_user = connection_user.cursor()


def initiate_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL
    )
    """)
    cursor_user.execute("""
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    """)
    connection.commit()
    connection_user.commit()


def create_products():
    medicine_list_crud = ['catharsis', 'nostalgia', 'relax', 'smile']
    vitamine_list_crud = ['радостин', 'ностальгиксин', 'релаксин', 'пакостин']
    for i in range(len(medicine_list_crud)):
        cursor.execute(f"INSERT INTO Products ('id', 'title', 'description', 'price') VALUES (?, ?, ?, ?)",
                       (f'{i + 1}', f'{medicine_list_crud[i]}', f'{vitamine_list_crud[i]}', f'{(i + 1) * 100}'))
    connection.commit()


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.commit()
    return products


def add_user(username, email, age):
    cursor_user.execute('INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)',
                        (f'{username}', f'{email}', f'{age}', '1000'))
    connection_user.commit()


def is_included(username):
    users = cursor_user.execute('SELECT username FROM Users').fetchall()
    while len(users):
        flag = False
        for user in users:
            if username in user:
                flag = True
            else:
                continue
        return flag
    connection_user.commit()


#initiate_db()
# create_products()
#get_all_products()
#connection.commit()
# connection.close()
