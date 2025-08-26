import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from services.api_client import get_jobs, get_job_by_id

TELEGRAM_TOKEN = "8340986151:AAF2NEC4zTCg-mXIT-c_z_qREkOqN-YtAmk"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply(
        "👋 Ish o‘rinlari botiga xush kelibsiz!\n\n"
        "🔊 Ushbu bot sizga ish o‘rinlarini topishda yordam beradi.\n"
        "🔎 Qidirish uchun inline rejimdan foydalaning:\n"
        "@DevVakansBot kalit_so'z"
    )


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.reply(
        "ℹ️ Qo‘llanma:\n"
        "🔎 Inline rejimda qidiring:\n"
        "🔍 Masalan: '@DevVakansBot python' yoki '@DevVakansBot Urganch'\n\n"
        "✅ Bot sizga kompaniya nomi, lavozim va linkni chiqarib beradi."
    )


@dp.message(Command("latest"))
async def latest_jobs_command(message: types.Message):
    try:
        jobs = await get_jobs("")  # bo‘sh kalit so‘z = so‘nggi ishlar
        if not jobs:
            await message.reply("🔎 So‘nggi ishlar topilmadi.")
            return
    except Exception as e:
        logging.error(f"API xatolik: {e}", exc_info=True)
        await message.reply("⚠️ Server xatoligi. Keyinroq urinib ko‘ring.")
        return

    results = jobs[:10]
    response_text = ""
    for job in results:
        title = job.get("slug", "")
        company = job.get("company", "")
        location = (job.get("location") or "").strip()
        url = job.get("url", "")
        response_text += f"💼 {title}\n🏢 {company}"
        if location:
            response_text += f"\n📍 {location}"
        if url:
            response_text += f"\n🔗 {url}"
        response_text += "\n\n"

    await message.reply(response_text)


@dp.inline_query()
async def inline_jobs(query: types.InlineQuery):
    keyword = query.query.strip()
    offset = int(query.offset or 0)
    if not keyword:
        await query.answer([], cache_time=1)
        return

    try:
        jobs = await get_jobs(keyword)
        if not jobs:
            await query.answer([], switch_pm_text="Natija topilmadi.", switch_pm_parameter="start")
            return
    except Exception as e:
        logging.error(f"API xatolik: {e}", exc_info=True)  # to‘liq traceback bilan log
        await query.answer([], switch_pm_text="Server xatoligi", switch_pm_parameter="start")
        return

    results = []
    for job in jobs[offset: offset + 10]:
        title = (job.get("slug") or "").strip()
        if not title:
            continue
        company = (job.get("company") or "").strip()
        url = (job.get("url") or "").strip()
        location = (job.get("location") or "").strip()
        _id = str(job.get("id") or "0")
        text = f"💼 {title}\n🏢 {company}"
        if location:
            text += f"\n📍 {location}"
        if url:
            text += f"\n🔗 {url}"
            results.append(
                InlineQueryResultArticle(
                    id=str(job.get("id", 0)),
                    title=title,
                    description=f"{company} | {location}" if location else company,

                    input_message_content=InputTextMessageContent(message_text=text)
                )
            )
    next_offset = str(offset + 10) if len(jobs) > offset + 10 else ""
    await query.answer(results=results, cache_time=1, next_offset=next_offset, is_personal=True)


@dp.message()
async def show_job_detail(message: types.Message):
    job_id = message.text.strip()
    job = await get_job_by_id(job_id)

    text = f"💼 {job.get('title', '')}\n" \
           f"🏢 {job.get('company', '')}"

    if job.get('location'):
        text += f"\n📍 {job['location']}"
    if job.get('url'):
        text += f"\n🔗 {job['url']}"
    if job.get('posted_at'):
        text += f"\n📅 {job['posted_at']}"

    await message.reply(text)


async def main():
    logging.info("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
