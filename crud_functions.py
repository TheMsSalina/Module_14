import sqlite3

connection = sqlite3.connect('bot_products.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)
    ''')
#    for i in range(1,5):
#        cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
#            (f'Продукт {i}', f'Описание {i}', f'Цена: {i*100}'))

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL)
    ''')

    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect("bot_products.db")
    cursor = connection.cursor()
    cursor.execute('SELECT id, title, description, price FROM Products')
    products_db = cursor.fetchall()
    connection.commit()
    connection.close()
    return list(products_db)

def populate_db():
    cursor.executescript('''
        INSERT INTO Products (title, description, price) VALUES (
            "VitaC",
            "Витамин С, в капсулах, 90 шт.",
            40);
        INSERT INTO Products (title, description, price) VALUES (
            "VitaB",
            "Витамин В, в капсулах, 180 шт.",
            32);
        INSERT INTO Products (title, description, price) VALUES (
            "Omega-3",
            "Омега-3, в капсулах, 90 шт.",
            20);
        INSERT INTO Products (title, description, price) VALUES (
            "L-karn",
            "L-карнитин, в капсулах, 30 шт.",
            30);
    ''')
    connection.commit()

if __name__ == '__main__':
    initiate_db()
    populate_db()
    connection.close()

