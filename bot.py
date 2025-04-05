import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import httpx

API_TOKEN = 'TOKEN'
API_URL = 'http://localhost:8000'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать! Используй команды: /add, /list, /delete, /toggle")

@dp.message(Command("add"))
async def cmd_add(message: types.Message):
    try:
        text = message.text.removeprefix("/add").strip()

        *title_parts, date_str, amount_str = text.rsplit(" ", 2)

        title = " ".join(title_parts)
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{API_URL}/expenses",
                params={"title": title, "date": date_str, "amount_uah": float(amount_str)}
            )
            await message.answer(f"✅ Добавлено: {res.json()}")
    except Exception as e:
        print(e)
        await message.answer("⚠️ Используй формат: /add название дата(01-04-2025) сумма(в грн)")

@dp.message(Command("list"))
async def cmd_list(message: types.Message):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{API_URL}/expenses")
        lines = []
        for exp in res.json():
            status = '✅' if exp['is_paid'] else '❌'
            lines.append(f"#{exp['id']} {exp['title']} | {exp['date']} | {exp['amount_uah']}₴ ({exp['amount_usd']}$) {status}")
        await message.answer("\n".join(lines) if lines else "Пока пусто")

@dp.message(Command("delete"))
async def cmd_delete(message: types.Message):
    try:
        _, eid = message.text.split()
        async with httpx.AsyncClient() as client:
            await client.delete(f"{API_URL}/expenses/{eid}")
            await message.answer("Удалено")
    except:
        await message.answer("Формат: /delete ID")

@dp.message(Command("toggle"))
async def cmd_toggle(message: types.Message):
    try:
        _, eid = message.text.split()
        async with httpx.AsyncClient() as client:
            res = await client.put(f"{API_URL}/expenses/{eid}/toggle")
            await message.answer(f"Статус обновлён: {res.json()['is_paid']}")
    except:
        await message.answer("Формат: /toggle ID")

if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling(bot))
    except KeyboardInterrupt:
        print('Close telegram bot polling...')
