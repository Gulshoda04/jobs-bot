import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

# from config import TELEGRAM_TOKEN
from services.api_client import get_jobs   # API xizmatidan ishlar ro‘yxatini olish

TELEGRAM_TOKEN = "8340986151:AAF2NEC4zTCg-mXIT-c_z_qREkOqN-YtAmk"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start", "help"]))
async def send_welcome(message: types.Message):
    await message.reply("👋 Ish o‘rinlari botiga xush kelibsiz!\n"
                        "🔎 Qidirish uchun inline rejimidan foydalaning:\n"
                        "`@DevVakansBot kalit_so'z`")


@dp.inline_query()
async def inline_jobs(query: types.InlineQuery):
    keyword = query.query.strip()
    offset = int(query.offset or 0)

    if not keyword:
        await query.answer([], cache_time=1)
        return

    jobs = await get_jobs(keyword)

    results = []
    for job in jobs[offset: offset + 10]:
        title = (job.get("slug") or "").strip()
        if not title:
            continue
        company = (job.get("company") or "").strip()
        url = (job.get("url") or "").strip()
        _id = str(job.get("id") or "1")

        results.append(
            InlineQueryResultArticle(
                id=_id,
                title=title,
                description=company,
                input_message_content=InputTextMessageContent(
                    message_text=f"💼 {title}\n🏢 {company}\n🔗 {url}" if url else f"💼 {title}\n🏢 {company}"
                ),
            )
        )

    next_offset = str(offset + 10) if len(jobs) > offset + 10 else ""

    await query.answer(results, cache_time=1, is_personal=True, next_offset=next_offset)


async def main():
    logging.info("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
