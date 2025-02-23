from mysql.connector.pooling import MySQLConnectionPool
from contextlib import contextmanager

class Database:
    def __init__(self):
        """Initialize the database connection pool"""
        self.db_config = {
            "host": "127.0.0.1",
            "port": 3307,
            "user": "root",
            "password": "root",
            "database": "expense_manager"
        }
        self.pool = MySQLConnectionPool(pool_name="mypool", pool_size=5, **self.db_config)

    @contextmanager
    def get_db_connection(self, commit=False):
        """Context manager for getting a database connection"""
        connection = self.pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            yield cursor
            if commit:
                connection.commit() 
        except Exception as e:
            connection.rollback()  
            print(f"Database error: {e}")
        finally:
            cursor.close()
            connection.close()

    def fetch_db(self, expense_date):
        """Fetch expenses for a specific date"""
        with self.get_db_connection() as cursor:
            cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
            return cursor.fetchall()

    def insert_into_db(self, expense_date, amount, category, notes):
        """Insert an expense (commit required)"""
        with self.get_db_connection(commit=True) as cursor:
            cursor.execute(
                "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
                (expense_date, amount, category, notes)
            )

    def delete_from_db(self, expense_date):
        """Delete expenses for a specific date (commit required)"""
        with self.get_db_connection(commit=True) as cursor:
            cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

    def fetch_expense_summary(self, start_date, end_date):
        """Fetch total expense summary by category"""
        with self.get_db_connection() as cursor:
            cursor.execute(
                "SELECT category, SUM(amount) as total FROM expenses WHERE expense_date BETWEEN %s AND %s GROUP BY category",
                (start_date, end_date)
            )
            return cursor.fetchall()

def main():
    db = Database()
    
    db.insert_into_db("2025-02-22", 100, "Food", "Lunch")
    data = db.fetch_db("2025-02-22")
    print("Fetched Data:", data)

if __name__ == '__main__':
    main()
