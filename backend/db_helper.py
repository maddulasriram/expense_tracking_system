import aiomysql
from contextlib import asynccontextmanager
import asyncio
from logging_setup import setup_logger

logger = setup_logger('db_helper')

class Database:
    def __init__(self):
        self.pool = None
        logger.debug("Database object initialized.")

    async def init_pool(self):
        """Initialize the database connection pool"""
        try:
            logger.info("Initializing database connection pool...")
            self.pool = await aiomysql.create_pool(
                host='127.0.0.1',
                port=3307,
                user='root',
                password='root',
                db='expense_manager',
                minsize=1,
                maxsize=5
            )
            logger.info("Database connection pool initialized.")
        except Exception as e:
            logger.error(f"Error initializing pool: {e}")
            raise

    @asynccontextmanager
    async def get_db_connection(self, commit=False):
        """Get a database connection from the pool with commit control"""
        if self.pool is None:
            logger.error("Database pool is not initialized. Call init_pool() first.")
            raise RuntimeError("Database pool is not initialized. Call init_pool() first.")
        
        conn = await self.pool.acquire()
        cursor = await conn.cursor(aiomysql.DictCursor)
        try:
            yield cursor
            if commit:
                logger.debug("Committing transaction...")
                await conn.commit()
        except Exception as e:
            logger.error(f"Database error: {e}")
            await conn.rollback()
        finally:
            await cursor.close()
            self.pool.release(conn)
            logger.debug("Connection released back to the pool.")

    async def fetch_expenses_for_date(self, expense_date):
        """Fetch expenses for a specific date"""
        try:
            logger.info(f"Fetching expenses for date: {expense_date}")
            async with self.get_db_connection() as cursor:
                await cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
                result = await cursor.fetchall()
                logger.info(f"Fetched {len(result)} expenses.")
                return result
        except Exception as e:
            logger.error(f"Error fetching expenses: {e}")
            raise

    async def insert_into_db(self, expense_date, amount, category, notes):
        """Insert an expense (Needs commit)"""
        try:
            logger.info(f"Inserting expense: {expense_date}, {amount}, {category}, {notes}")
            async with self.get_db_connection(commit=True) as cursor:
                await cursor.execute(
                    "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
                    (expense_date, amount, category, notes)
                )
                logger.info(f"Expense for {expense_date} inserted.")
        except Exception as e:
            logger.error(f"Error inserting expense: {e}")
            raise

    async def delete_from_db(self, expense_date):
        """Delete expenses for a specific date (Needs commit)"""
        try:
            logger.info(f"Deleting expenses for date: {expense_date}")
            async with self.get_db_connection(commit=True) as cursor:
                await cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))
                logger.info(f"Expenses for {expense_date} deleted.")
        except Exception as e:
            logger.error(f"Error deleting expenses: {e}")
            raise

    async def fetch_expense_summary(self, start_date, end_date):
        """Fetch total expense summary by category"""
        try:
            logger.info(f"Fetching expense summary between {start_date} and {end_date}")
            async with self.get_db_connection() as cursor:
                await cursor.execute(
                    "SELECT category, SUM(amount) as total FROM expenses WHERE expense_date BETWEEN %s AND %s GROUP BY category;",
                    (start_date, end_date)
                )
                result = await cursor.fetchall()
                logger.info(f"Fetched expense summary: {result}")
                return result
        except Exception as e:
            logger.error(f"Error fetching expense summary: {e}")
            raise
    
    async def close_pool(self):
        """Properly close the database connection pool"""
        if self.pool:
            logger.info("Closing database connection pool...")
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("Database connection pool closed.")
    
async def main():
    db = Database()
    await db.init_pool()

    await db.insert_into_db("2025-02-22", 100, "Food", "Lunch")
    data = await db.fetch_expenses_for_date("2025-02-22")
    print("Fetched Data:", data)

    await db.close_pool()

if __name__ == "__main__":
    asyncio.run(main())
