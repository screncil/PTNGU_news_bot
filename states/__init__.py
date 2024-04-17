from aiogram.fsm.state import State, StatesGroup

class Question(StatesGroup):
    text = State()

class Answer(StatesGroup):
    text = State()

class News(StatesGroup):
    title = State()
    description = State()
    media = State()
    confirm = State()
