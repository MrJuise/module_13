from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

api = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет я бот помогающий твоему здоровью. Введите Calories, чтоб подсчитать калории.")


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()
    level_activ = State()


@dp.message_handler(text="Calories")
async def set_gender(message):
    await message.answer("Введите свой пол (М / Ж):")
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_age(message, state):
    try:
        gender = str(message.text.casefold())
        if gender in ["м", "ж"]:
            await state.update_data(gender=gender)
            await message.answer("Введите свой возраст:")
            await UserState.age.set()
        else:
            await message.answer("Введите корректный пол (М / Ж).")
    except ValueError:
        await message.answer("Введите корректный пол (М / Ж).")


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    try:
        age = float(message.text)
        if age in range(13, 81):
            await state.update_data(age=age)
            await message.answer("Введите свой рост:")
            await UserState.growth.set()
        else:
            await message.answer("Данная формула актуальна только для лиц в возрасте от 13 до 80 лет.")
    except ValueError:
        await message.answer("Введите возраст в числовом формате.")


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    try:
        growth = float(message.text)
        if growth > 0:
            await state.update_data(growth=growth)
            await message.answer("Введите свой вес:")
            await UserState.weight.set()
        else:
            await message.answer("Рост не может быть меньше 0. Введите корректное значение!")
    except ValueError:
        await message.answer("Введите возраст в числовом формате.")


@dp.message_handler(state=UserState.weight)
async def set_level_active(message, state):
    try:
        weight = float(message.text)
        if weight > 0:
            await state.update_data(weight=weight)
            await message.answer("Введите свой уровень активности согласно номеру в таблице: \n "
                                 "1 - Минимальная активность \n 2 - Слабая активность\n "
                                 "3 - Средняя активность \n 4 - Высокая активность \n "
                                 "5 - Экстра-активность")
            await UserState.level_activ.set()
        else:
            await message.answer("Вес не может быть меньше 0. Введите корректный вес!")
    except ValueError:
        await message.answer("Введите вес в числовом формате.")


@dp.message_handler(state=UserState.level_activ)
async def send_calories(message, state):
    activ_value = {
        1: 1.2,
        2: 1.375,
        3: 1.55,
        4: 1.725,
        5: 1.9
    }
    try:
        level_active = int(message.text)
        if level_active in range(1, 6):
            await state.update_data(level_active=level_active)
            data = await state.get_data()
            if data["gender"] == "м":
                calories = (10 * float(data["weight"]) + 6.25 * float(data["growth"]) - 5 *
                            float(data["age"]) + 5) * activ_value[level_active]
                await message.answer(f"Норма калорий в день составляет: {round(calories)}")
            elif data["gender"] == "ж":
                calories = (10 * float(data["weight"]) + 6.25 * float(data["growth"]) - 5 *
                            float(data["age"]) + 5) * activ_value[level_active]
                await message.answer(f"Норма калорий в день составляет: {round(calories)}")
            await state.finish()
        else:
            await message.answer("Введите значение от 1 до 5 согласно таблице.")
    except ValueError:
        await message.answer("Введите значение от 1 до 5 согласно таблице.")

@dp.message_handler()
async def all_massages(message):
    await message.answer("Введите Calories, чтоб подсчитать калории.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
