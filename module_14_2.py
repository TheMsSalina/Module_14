import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL)
''')

'''
cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users(email)')
for i in range(1, 11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'User{i}', f'{i}ex@gmail.com', f'{i*10}', '1000'))

for i in range(1, 11):
    if i % 2:
        cursor.execute('UPDATE Users SET balance = 500 WHERE id = ?',(i,))

for i in range(1, 11):
    if i % 3 == 1:
        cursor.execute('DELETE FROM Users WHERE id = ?',(i,))

cursor.execute("SELECT * FROM Users WHERE age <> 60")
users = cursor.fetchall()
for user in users:
    id, username, email, age, balance = user
    print(f'Имя: {username}|' f'Почта: {email}|' f'Возраст: {age}|' f'Баланс: {balance}')
'''

cursor.execute('DELETE FROM Users WHERE id = ?',(6,))

cursor.execute('SELECT COUNT(*) FROM Users')
total = cursor.fetchone()[0]
#print(total)

cursor.execute('SELECT SUM(balance) FROM Users')
total_balance = cursor.fetchone()[0]
#print(total_balance)

print(total_balance/total)


connection.commit()
connection.close()
