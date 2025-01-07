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

    connection.commit()
    connection.close()

initiate_db()

def get_all_products():
    connection = sqlite3.connect("bot_products.db")
    cursor = connection.cursor()
    cursor.execute('SELECT title, description, price FROM Products')
    products_db = cursor.fetchall()
    connection.commit()
    connection.close()
    return list(products_db)


