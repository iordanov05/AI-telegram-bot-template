from aiogram.fsm.state import StatesGroup, State


class ChatStates(StatesGroup):
    """FSM state for tracking conversation with context."""

    chatting = State()
