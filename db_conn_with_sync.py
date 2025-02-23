##without pooling
import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
@contextmanager
def get_db_connection(commit=False):
    connection = mysql.connector.connect(
        host = '127.0.0.1',
        port = 3307,
        user = 'root',
        password = 'root',
        database = 'expense_manager'
    )
    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
        if commit:
            connection.commit()
    except Exception:
        print('failed to get connection')
    finally:
        cursor.close()
        connection.close()

def fetch_db(expense_date):
    with get_db_connection() as cursor:
        cursor.execute('SELECT * FROM expenses WHERE expense_date =  %s', (expense_date,))
        return cursor.fetchall()
def insert_into_db(expense_date, amount, category, notes):
    with get_db_connection(commit=True) as cursor:
        cursor.execute('INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s,%s,%s,%s)', (expense_date, amount, category, notes))

def delete_from_db(expense_date):
    with get_db_connection(commit=True) as cursor:
        cursor.execute('DELETE FROM expenses WHERE expense_date = %s', (expense_date,))
def fetch_expense_summary(start_date, end_date):
    with get_db_connection() as cursor:
        cursor.execute(
            "SELECT  category, SUM(amount) as total \
            FROM expenses WHERE expense_date \
            BETWEEN %s and %s \
            GROUP BY category;", (start_date, end_date))
        return cursor.fetchall()
    

