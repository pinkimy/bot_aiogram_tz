from fastapi import FastAPI
from models import Base
from database import engine
from crud import add_expense, list_expenses, delete_expense, toggle_status
from datetime import datetime

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/expenses")
async def create_expense(title: str, date: str, amount_uah: float):
    date_obj = datetime.strptime(date, "%d-%m-%Y").date()
    return await add_expense(title, date_obj, amount_uah)

@app.get("/expenses")
async def get_expenses():
    return await list_expenses()

@app.delete("/expenses/{expense_id}")
async def remove_expense(expense_id: int):
    await delete_expense(expense_id)
    return {"ok": True}

@app.put("/expenses/{expense_id}/toggle")
async def change_status(expense_id: int):
    return await toggle_status(expense_id)

