import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config_reader import config
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

# Логирование
logging.basicConfig(level=logging.INFO)

# Бот и его ключ полученный из get_secret_value
bot = Bot(token=config.bot_token.get_secret_value())

# Диспетчер
dp = Dispatcher(storage=MemoryStorage())

# Имя файла для хранения данных
DATA_FILE = 'dishes.json'

# Функция для загрузки данных из файла
def load_dishes():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Функция для сохранения данных в файл
def save_dishes(dishes):
    with open(DATA_FILE, 'w') as f:
        json.dump(dishes, f)

# Загрузка данных при запуске
dishes = load_dishes()

class DishForm(StatesGroup):
    waiting_for_dish_name = State()
    waiting_for_delete_index = State()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для хранения названий блюд. Введите /add для добавления нового блюда, /list для отображения всех блюд и /delete для удаления блюда по порядковому номеру.")

@dp.message(Command("add"))
async def add_dish(message: types.Message, state: FSMContext):
    await message.reply("Введите название блюда:")
    await state.set_state(DishForm.waiting_for_dish_name)

@dp.message(Command("list"))
async def list_dishes(message: types.Message):
    if not dishes:
        await message.reply("Список блюд пуст.")
    else:
        await message.reply("Список блюд:\n" + "\n".join(f"{idx + 1}. {dish}" for idx, dish in enumerate(dishes)))

@dp.message(Command("delete"))
async def delete_dish(message: types.Message, state: FSMContext):
    if not dishes:
        await message.reply("Список блюд пуст, удалять нечего.")
    else:
        await message.reply("Введите номер блюда, которое хотите удалить:")
        await state.set_state(DishForm.waiting_for_delete_index)

@dp.message(DishForm.waiting_for_dish_name)
async def handle_dish_name(message: types.Message, state: FSMContext):
    dishes.append(message.text)
    save_dishes(dishes)
    await message.reply("Блюдо добавлено!")
    await state.clear()

@dp.message(DishForm.waiting_for_delete_index)
async def handle_delete_index(message: types.Message, state: FSMContext):
    try:
        index = int(message.text) - 1
        if 0 <= index < len(dishes):
            deleted_dish = dishes.pop(index)
            save_dishes(dishes)
            await message.reply(f"Блюдо '{deleted_dish}' удалено!")
        else:
            await message.reply("Неверный номер блюда. Попробуйте еще раз.")
    except ValueError:
        await message.reply("Пожалуйста, введите корректный номер.")
    await state.clear()

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
