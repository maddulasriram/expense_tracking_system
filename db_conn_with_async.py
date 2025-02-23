import aiomysql
from contextlib import asynccontextmanager
import asyncio

class Database:
    def __init__(self):
        self.pool = None  

    async def init_pool(self):
        """Initialize the database connection pool"""
        self.pool = await aiomysql.create_pool(
            host='127.0.0.1',
            port=3307,
            user='root',
            password='root',
            db='expense_manager',
            minsize=1,
            maxsize=5
        )

    @asynccontextmanager
    async def get_db_connection(self, commit=False):
        """Get a database connection from the pool with commit control"""
        if self.pool is None:
            raise RuntimeError("Database pool is not initialized. Call init_pool() first.")
        
        conn = await self.pool.acquire()
        cursor = await conn.cursor(aiomysql.DictCursor)
        try:
            yield cursor
            if commit:
                await conn.commit()  
        except Exception as e:
            await conn.rollback()  
            print(f"Database error: {e}")
        finally:
            await cursor.close() 
            self.pool.release(conn)  

    async def fetch_db(self, expense_date):
        """Fetch expenses for a specific date"""
        async with self.get_db_connection() as cursor:
            await cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
            return await cursor.fetchall()

    async def insert_into_db(self, expense_date, amount, category, notes):
        """Insert an expense (Needs commit)"""
        async with self.get_db_connection(commit=True) as cursor:
            await cursor.execute(
                "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
                (expense_date, amount, category, notes)
            )

    async def delete_from_db(self, expense_date):
        """Delete expenses for a specific date (Needs commit)"""
        async with self.get_db_connection(commit=True) as cursor:
            await cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

    async def fetch_expense_summary(self, start_date, end_date):
        """Fetch total expense summary by category"""
        async with self.get_db_connection() as cursor:
            await cursor.execute(
                "SELECT category, SUM(amount) as total FROM expenses WHERE expense_date BETWEEN %s AND %s GROUP BY category;",
                (start_date, end_date)
            )
            return await cursor.fetchall()

    async def close_pool(self):
        """Properly close the database connection pool"""
        if self.pool:
            self.pool.close()  
            await self.pool.wait_closed()  
            print("Database connection pool closed.")

async def main():
    db = Database()
    await db.init_pool() 

    await db.insert_into_db("2025-02-22", 100, "Food", "Lunch") 
    data = await db.fetch_db("2025-02-22")
    print("Fetched Data:", data)

    await db.close_pool()  

if __name__ == "__main__":
    asyncio.run(main())
