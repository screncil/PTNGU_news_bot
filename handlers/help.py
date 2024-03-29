from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


from keyboards.QuestionKB import QuestionKB
from keyboards.MainMenuKB import MainMenuKB

from states import Question, Answer
import random

from vspDB import Questions, Admin

from bot import bot

router = Router()

question_db = Questions()
admin_db = Admin()

@router.message(StateFilter(None), F.text == "❓ Задати питання")
async def help(msg: Message, state: FSMContext):
    if not question_db.checkUser(msg.from_user.id):
        await msg.answer(
            "✏️ Напишіть у текстове поле запитання на яке хочете отримати відповідь"
        )
        await state.set_state(Question.text)
    else:
        await msg.answer("🤦‍♀️ Ви вже надіслали запитання")


@router.callback_query(lambda call: call.data.startswith("dislinequestion"))
async def dislineQuestion(call: CallbackQuery):
    question_id = call.data.split("_")[-1]
    question = question_db.getQuestion(question_id)
    await call.message.edit_text(
        inline_message_id=str(call.message.message_id),
        text="✅ Запитання успішно відхилено",
        reply_markup=None
    )
    await bot.send_message(
        chat_id=question[0][2],
        text=f"❌ <b>Ваше питання</b> '<i>{question[0][4]}</i>' <b>відхилено</b>",
        reply_markup=MainMenuKB(),
        parse_mode=ParseMode.HTML
    )

    question_db.deleteQuestion(question_id)


@router.message(Question.text, F.text)
async def set_question(msg: Message, state: FSMContext):
    quest_id = random.randint(1, 100000)
    await state.update_data(text=msg.text)
    data = await state.get_data()
    question_db.addQuestion(question_id=quest_id, questioner_id=msg.from_user.id, text=data['text'], username=msg.from_user.first_name)
    await msg.answer("✅ Ваше запитання відправлено на опрацювання адміністрацією")
    for admin in admin_db.getAllAdminIds():
        await bot.send_message(
            chat_id=admin,
            text=f"🔔 <b>Нове запитання від користувача <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.first_name}</a></b>\n\n<i>{data['text']}</i>",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=QuestionKB(question_id=quest_id).as_markup()
        )

    await state.clear()


@router.callback_query(lambda call: call.data.startswith("acceptquestion"))
async def acceptQuestion(call: CallbackQuery, state: FSMContext) -> None:
    question_id = call.data.split("_")[-1]
    if not question_db.getStatus(question_id):
        question_db.updateStatus(question_id)
        question = question_db.getQuestion(question_id)
        await call.message.edit_text(
            f"🔔 <b>Запитання від користувача <a href='tg://user?id={question[0][2]}'>{question[0][5]}</a></b>\n\n<i>{question[0][4]}</i>\n\nНапишіть відповідь у текстове поле а потім відправте 👇",
            inline_message_id=str(call.message.message_id),
            parse_mode=ParseMode.HTML,
            reply_markup=None
        )
        await state.update_data(question_id=question_id, questioner_id=question[0][2], question_text=question[0][4])
        await state.set_state(Answer.text)
    else:
        await call.answer("На це запитання вже відповідає інший адміністратор 🤷")


@router.message(Answer.text, F.text)
async def answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(
        chat_id=data['questioner_id'],
        text=f"🔔 <b>Відповідь на запитання</b> '{data['question_text']}'\n\n<i>{msg.text}</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=MainMenuKB()
    )

    question_db.deleteQuestion(data['question_id'])
    await state.clear()

    await msg.answer("✅ Відповідь успішно відправлена", reply_markup=MainMenuKB())




