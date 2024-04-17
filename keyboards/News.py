from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




def NewsKB(user_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✅ Викласти", callback_data=f"newsaccept_{user_id}"))
    builder.row(InlineKeyboardButton(text="❌ Відхилити", callback_data=f"newsdisline_{user_id}"))
    return builder


def dontSendMedia():
    kb = [
        [KeyboardButton(text="Не надсилати медіа ❌")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)