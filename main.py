import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from config_reader import config

#Логирование
logging.basicConfig(level=logging.INFO)
#Бот
bot = Bot(token=config.bot_token.get_secret_value())
#Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Добавить блюдо")],
        [types.KeyboardButton(text="Удалить блюдо")],
        [types.KeyboardButton(text="Посмотреть список всех блюд")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите желаемое действие"
    )
    await message.answer("Привет, я бот для составления домашнего меню. Для удобства пользования используйте кнопки ниже!", reply_markup=keyboard)

@dp.message(F.text.lower() == "добавить блюдо")
async def new_dish(message: types.Message):
    await message.reply("Укажите название блюда для добавления!")

@dp.message(F.text.lower() == "удалить блюдо")
async def delete_dish(message: types.Message):
    await message.reply("Укажите название блюда для удаления!")

@dp.message(F.text.lower() == "посмотреть список всех блюд")
async def list_dish(message: types.Message):
    await message.reply("А БИЛЯ Я ЕЩЕ НИЧЕГО НЕ СДЕЛАЛЬ")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())