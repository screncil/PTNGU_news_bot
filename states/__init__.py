from aiogram.fsm.state import State, StatesGroup



class Question(StatesGroup):
    text = State()


class Answer(StatesGroup):
    text = State()