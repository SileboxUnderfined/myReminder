from telebot.async_telebot import AsyncTeleBot
from os import environ
from datetime import datetime, timedelta
import asyncio, aiosqlite

bot = AsyncTeleBot(token=environ['TOKEN'])

timeFormat = "%Y%m%d%H%M%S"

async def getNextTime():
    r = datetime.now() + timedelta(seconds=5)
    return r.strftime(timeFormat)

async def getDateTime(s):
    return datetime.strptime(s, timeFormat)

async def checkReminders():
    async with aiosqlite.connect("data.db") as db:
        async with db.execute("SELECT next_date, user_id, text FROM users") as cursor:
            data = await cursor.fetchall()
            if len(data) > 0:
                for user in data:
                    print(user)
                    print(await getDateTime(user[0]))
                    print(datetime.now().replace(microsecond=0))
                    if await getDateTime(user[0]) == datetime.now().replace(microsecond=0):
                       await bot.send_message(chat_id=int(data[1]), text=data[2])

    await asyncio.sleep(int(environ['DELAY']))

@bot.message_handler(commands=["start"])
async def start(message):
    await bot.reply_to(message, "Приветствую тебя. Используй команду /new чтобы добавить новое напоминание каждый час")

@bot.message_handler(commands=["new"])
async def new_cmd(message):
    text = message.text.split()
    text.pop(0)
    text = ''.join(text)
    if len(text) == 0:
        await bot.reply_to(message, "нужно ввести команду в виде /new {текст}")
        return

    user_id = message.from_user.id
    next_date = await getNextTime()
    async with aiosqlite.connect('data.db') as db:
        await db.execute(f"INSERT INTO users (user_id, text, next_date) VALUES ({user_id}, {text}, {next_date})")
        await db.commit()

    await bot.reply_to(message, f'Напоминание успешно создано!\nСледующее напоминание будет: {await getDateTime(next_date)}')

async def main():
    loop = asyncio.get_running_loop()
    bot_task = loop.create_task(bot.polling())
    check_reminders = loop.create_task(checkReminders())
    loop.run_until_complete(asyncio.wait([bot_task,check_reminders]))

asyncio.run(main())
