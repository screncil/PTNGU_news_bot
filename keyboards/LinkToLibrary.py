from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def LinkToLibraryKB() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📚 Наша бібліотека", url="https://inter.ptngu.com/"))
    return builder