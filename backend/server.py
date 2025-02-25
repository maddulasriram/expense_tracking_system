import db_helper
from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
from pydantic import BaseModel
from contextlib import asynccontextmanager

class Expense(BaseModel):
     amount: float
     category: str
     notes: str
class DateRange(BaseModel):
    startdate: date
    enddate: date
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB connection pool
    db = db_helper.Database()
    await db.init_pool()
    app.state.db = db  

    yield  
    await db.pool.clear()

app = FastAPI(lifespan=lifespan)

@app.get('/expenses/{expense_date}', response_model=List[Expense])
async def get_expenses(expense_date : date):
    try:
        expenses = await app.state.db.fetch_expenses_for_date(expense_date)

        if not expenses:
            raise HTTPException(status_code=404, detail='No expenses found for the given date')

        return expenses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/expenses/{expense_date}')
async def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    if not expenses:
        raise HTTPException(status_code=400, detail='No expenses provided')

    try:
        await app.state.db.delete_from_db(expense_date)
        for expense in expenses:
            await app.state.db.insert_into_db(expense_date, expense.amount, expense.category, expense.notes)
        return {"message": "Expenses added/updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analytics/")
async def get_analytics(date_range: DateRange):
    try:
        data = await app.state.db.fetch_expense_summary(date_range.startdate, date_range.enddate)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    total = sum([row['total'] for row in data])
    breakdown= {}
    for row in data:
            percentage = (row['total']/total)*100 if total!=0 else 0
            breakdown[row['category']] = {
                'total': row['total'],
                'percentage' : percentage
            }
    return breakdown

