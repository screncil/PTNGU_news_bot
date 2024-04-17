from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton


def MainMenuKB() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="📰 Запропонувати новину"), KeyboardButton(text="❓ Задати питання")],
        [KeyboardButton(text="👨 Автори бота")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
