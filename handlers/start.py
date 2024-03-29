from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.MainMenuKB import MainMenuKB
from keyboards.LinkToLibrary import LinkToLibraryKB

from vspDB import User

import time

db_user = User()
router = Router()

@router.message(Command("start"))
async def start(msg: Message):
    if not db_user.checkUserExists(msg.from_user.id):
        if msg.from_user.username is not None:
            db_user.addUser(user_id=msg.from_user.id, username=msg.from_user.username, join_time=int(time.time()))
        else:
            db_user.addUser(user_id=msg.from_user.id, username=msg.from_user.first_name, join_time=int(time.time()))

    await msg.answer(f"Привіт {msg.from_user.first_name} 🙋", reply_markup=MainMenuKB())
    await msg.answer(
        "Зараз ти перебуваєш у боті коледжу \n<a href='https://ptngu.com'>ВСП 'Павлоградський фаховий коледж' НТУ 'ДП'</a>\n\n Тут ти можеш залишити свою заявку на новину про наш навчальний заклад!\n\n Знизу ти можеш перейти до нашої бібліотеки та дізнатися подробиці про наші спеціальності 👇",
        reply_markup=LinkToLibraryKB().as_markup(), parse_mode=ParseMode.HTML)