from sqlalchemy.future import select
from models import Expense
from database import async_session
from datetime import datetime
import httpx

async def convert_to_usd(amount_uah):
    async with httpx.AsyncClient() as client:
        res = await client.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
        rate = next((float(item['sale']) for item in res.json() if item['ccy'] == 'USD'), 0)
        return round(amount_uah / rate, 2)

async def add_expense(title, date, amount_uah):
    amount_usd = await convert_to_usd(amount_uah)
    async with async_session() as session:
        expense = Expense(title=title, date=date, amount_uah=amount_uah, amount_usd=amount_usd)
        session.add(expense)
        await session.commit()
        return expense

async def list_expenses():
    async with async_session() as session:
        result = await session.execute(select(Expense))
        return result.scalars().all()

async def delete_expense(expense_id):
    async with async_session() as session:
        expense = await session.get(Expense, expense_id)
        if expense:
            await session.delete(expense)
            await session.commit()

async def toggle_status(expense_id):
    async with async_session() as session:
        expense = await session.get(Expense, expense_id)
        if expense:
            expense.is_paid = not expense.is_paid
            await session.commit()
            return expense

