from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "7797685631:AAGpndoOqsnkCjQAofaMzmw3Vfp0lIe7zxA"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет я бот помогающий твоему здоровью.")

@dp.message_handler()
async def all_massages(message):
    await message.answer("Введите команду /start, чтоб начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
