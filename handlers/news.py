import random
from datetime import datetime

# aiogram libraries importing
from aiogram import Router, F
from aiogram.enums import ParseMode, parse_mode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, InputMediaPhoto, CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram_media_group import media_group_handler

from typing import List, Dict, Any

#aiogram keyboards
from keyboards.News import NewsKB, dontSendMedia
from keyboards.MainMenuKB import MainMenuKB

from states import News

import vspDB

import config
import bot

admin_db = vspDB.Admin()

router = Router()


@router.message(F.text == "📰 Запропонувати новину")
async def title(msg: Message, state: FSMContext):
    await msg.answer("Надішліть заголовок 🪧")
    await state.set_state(News.title)


@router.message(News.title, F.text)
async def description(msg: Message, state: FSMContext):
    await state.update_data(title=msg.text)
    await msg.answer("Надішліть текст новини 🗞")
    await state.set_state(News.media)

@router.message(News.media, F.text)
async def media(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text, user_id=msg.from_user.id, chat_id=msg.from_user.id, username=msg.from_user.first_name)
    await msg.answer("Надішліть медіа-контент якщо в цьому є потреба\n\n<i>Натисніть кнопку знизу для відправки без контенту 👇</i>", parse_mode=ParseMode.HTML, reply_markup=dontSendMedia())
    await state.set_state(News.confirm)


@router.message(News.confirm, F.text == "Не надсилати медіа ❌")
async def dislineMedia(msg: Message, state: FSMContext):
    data_ = await state.get_data()
    state_with: FSMContext = FSMContext(
        storage=bot.dp.storage,
        key=StorageKey(
            chat_id=data_['user_id'],
            user_id=data_['user_id'],
            bot_id=bot.bot.id
        )
    )

    data = await state_with.update_data(data=data_)
    await msg.answer("Ваша новина відправлена до адміністрації 👨", reply_markup=MainMenuKB())
    for admin in admin_db.getAllAdminIds():
        await bot.bot.send_message(chat_id=admin, text=f"<b>Нове повідомлення від <a href='tg://user?id={data['user_id']}'>{data['username']}</a></b>\n\n{'=' * 20}\n\n<b>{data['title']}</b>\n\n<i>{data['description']}</i>", parse_mode=ParseMode.HTML, reply_markup=NewsKB(data['user_id']).as_markup())


    data = await state_with.update_data(data=data_)
    await state.clear()


@router.callback_query(F.data.startswith("newsaccept"))
async def acceptt(call: CallbackQuery, state: FSMContext):
    await state.clear()
    user = call.data.split("_")
    state_with: FSMContext = FSMContext(
        storage=bot.dp.storage,
        key=StorageKey(
            chat_id=int(user[-1]),
            user_id=int(user[-1]),
            bot_id=bot.bot.id
        )
    )
    data = await state_with.get_data()

    if "media" in data:
        if isinstance(data["media"], list):
            data['media'][0].caption = f"<b>{data['title']}</b>\n\n<i>{data['description']}</i>\n\n{datetime.now().strftime('%Y/%m/%d %H:%M')}"
            await bot.bot.send_media_group(chat_id=config.CHANNEL_ID, media=data['media'])

            await call.message.delete()

            await state_with.clear()
            await state.clear()

            await call.message.answer("Новина відправлена у новосний канал 😚", reply_markup=MainMenuKB())
            await bot.bot.send_message(chat_id=data['user_id'], text="Ваша новина у каналі 😚")

        else:
            await bot.bot.send_photo(chat_id=config.CHANNEL_ID, photo=data['media'], caption=f"<b>{data['title']}</b>\n\n<i>{data['description']}</i>\n\n{datetime.now().strftime('%Y/%m/%d %H:%M')}", parse_mode=ParseMode.HTML)

            await call.message.delete()

            await call.message.answer("Новина відправлена у новосний канал 😚", reply_markup=MainMenuKB())
            await bot.bot.send_message(chat_id=data['user_id'], text="Ваша новина у каналі 😚")

            await state_with.clear()
            await state.clear()
    else:
        await bot.bot.send_message(chat_id=config.CHANNEL_ID, text=f"<b>{data['title']}</b>\n\n<i>{data['description']}</i>\n\n{datetime.now().strftime('%Y/%m/%d %H:%M')}", parse_mode=ParseMode.HTML)
        await state_with.clear()
        await call.message.delete()
        await call.message.answer("Новина відправлена у новосний канал 😚", reply_markup=MainMenuKB())


@router.callback_query(F.data.startswith("newsdisline"))
async def newsdisline(call: CallbackQuery, state: FSMContext):
    await state.clear()
    user = call.data.split("_")
    state_with: FSMContext = FSMContext(
        storage=bot.dp.storage,
        key=StorageKey(
            chat_id=int(user[-1]),
            user_id=int(user[-1]),
            bot_id=bot.bot.id
        )
    )
    await state_with.clear()
    await call.message.delete()
    await call.message.answer("Новина відхилена ❌", reply_markup=MainMenuKB())
    await bot.bot.send_message(chat_id=user[-1], text="Ваша новина відхилена адміністратором ❌", reply_markup=MainMenuKB())


@router.message(News.confirm, F.media_group_id ,F.content_type.in_({'photo'}))
@media_group_handler(only_album=True)
async def mediaa(msgs: List[Message], state: FSMContext):
    data_ = await state.get_data()
    media = [InputMediaPhoto(media=m.photo[-1].file_id) for m in msgs]
    media[0].caption = f"<b>Нове повідомлення від <a href='tg://user?id={data_['user_id']}'>{data_['username']}</a></b> 🔔\n\n{'=' * 20}\n\n<b>{data_['title']}</b>\n\n<i>{data_['description']}</i>"
    media[0].parse_mode = ParseMode.HTML
    data_ = await state.update_data(media=media)
    state_with: FSMContext = FSMContext(
        storage=bot.dp.storage,
        key=StorageKey(
            chat_id=data_['user_id'],
            user_id=data_['user_id'],
            bot_id=bot.bot.id
        )
    )
    data = await state_with.update_data(data=data_)

    for admin in admin_db.getAllAdminIds():
        await bot.bot.send_media_group(chat_id=admin, media=data['media'])
        await bot.bot.send_message(chat_id=admin,
                                   text=f"Вибір 🙌🏻",
                                   parse_mode=ParseMode.HTML, reply_markup=NewsKB(data['user_id']).as_markup())

    await bot.bot.send_message(chat_id=data['user_id'], text="Ваша новина відправлена до адміністрації 👨", reply_markup=MainMenuKB())



@router.message(News.confirm, F.photo)
async def photo(msg: Message, state: FSMContext):
    media = msg.photo[-1].file_id
    data_ = await state.update_data(media=media)
    state_with: FSMContext = FSMContext(
        storage=bot.dp.storage,
        key=StorageKey(
            chat_id=data_['user_id'],
            user_id=data_['user_id'],
            bot_id=bot.bot.id
        )
    )
    data = await state_with.update_data(data=data_)
    for admin in admin_db.getAllAdminIds():
        await bot.bot.send_photo(chat_id=admin, photo=data['media'], caption=f"<b>Нове повідомлення від <a href='tg://user?id={data['user_id']}'>{data['username']}</a></b> 🔔\n\n{'=' * 20}\n\n<b>{data['title']}</b>\n\n<i>{data['description']}</i>", parse_mode=ParseMode.HTML, reply_markup=NewsKB(data['user_id']).as_markup())

    await bot.bot.send_message(chat_id=data['user_id'], text="Ваша новина відправлена до адміністрації 👨", reply_markup=MainMenuKB())
