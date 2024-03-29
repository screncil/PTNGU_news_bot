
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def QuestionKB(question_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✅ Відповісти", callback_data=f"acceptquestion_{question_id}"))
    builder.row(InlineKeyboardButton(text="❌ Відхилити", callback_data=f"dislinequestion_{question_id}"))
    return builder