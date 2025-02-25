from backend import db_helper
import pytest

@pytest.mark.asyncio
async def test_fetch_expenses_for_date(db):
    expenses = await db.fetch_expenses_for_date('2024-08-15')

    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10.0
    assert expenses[0]['category'] == 'Shopping'
    assert expenses[0]['notes'] == 'Bought potatoes'


@pytest.mark.asyncio
async def test_fetch_expenses_for_invalid_date(db):
    expenses = await db.fetch_expenses_for_date('1999-08-15')
    assert len(expenses)==0

@pytest.mark.asyncio
async def test_fetch_expense_summary_invalid_range(db):
    summary = await db.fetch_expense_summary('2099-08-15', '2099-12-30')
    assert len(summary)==0