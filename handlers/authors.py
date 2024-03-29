from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import Message



router = Router()

@router.message(F.text == "👨 Автори бота")
async def authors(msg: Message):
    await msg.answer(
        "<b>🧑‍💻 Розробники бота новин коледжу</b>\n\n🧙 <a href='https://t.me/tonadoo'>Селіхов Ілля (гр. КІ-2-21)</a> - розробник програмного забезпечення\n🧑‍🎨 <a href='https://t.me/dukki_777'>Огли Рустам (гр. КІ-2-21)</a> - розробник архітектури та новатор проекту",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )