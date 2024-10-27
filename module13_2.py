from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message):
    print("Привет я бот помогающий твоему здоровью.")


@dp.message_handler()
async def all_massages(message):
    print("Введите команду /start, чтоб начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)