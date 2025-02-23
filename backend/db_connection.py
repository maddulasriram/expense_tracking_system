import mysql.connector

connection = mysql.connector.connect(
    host = '127.0.0.1',
    port = 3307,
    user = 'root',
    password = 'root',
    database = 'expense_manager'
)

if connection.is_connected():
      print('successful')
else:
      print('error')

cursor = connection.cursor(dictionary=True)
cursor.execute('SELECT * FROM expenses;')
data = cursor.fetchall()
print(data)
cursor.close()
connection.close()