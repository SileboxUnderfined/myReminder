from telebot.async_telebot import AsyncTeleBot
from os import environ
from datetime import datetime, timedelta
import asyncio, aiosqlite

bot = AsyncTeleBot(token=environ['TOKEN'])

@bot.message_handler(commands=["start"])
async def start(message):
    await bot.reply_to(message, "Приветствую тебя. Используй команду /new чтобы добавить новое напоминание")

@bot.message_handler(commands=["new"])
async def new_cmd(message):
    user_id = message.from_user.id



asyncio.run(bot.polling())