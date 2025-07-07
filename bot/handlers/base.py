from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.states import ChatStates
from bot.keyboards import get_main_keyboard
from bot.services.openrouter_client import get_openrouter_response
from bot.services.logger import logger

router = Router()

# Memory context store
user_histories: dict[int, list[dict[str, str]]] = {}


@router.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    if message.from_user is None:
        logger.warning("/start received with no from_user")
        await message.answer("⚠️ Не удалось определить пользователя.")
        return

    logger.info(f"/start command from user_id={message.from_user.id}")

    await state.set_state(ChatStates.chatting)
    user_histories[message.from_user.id] = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]
    await message.answer(
        "🤖 Привет! Я AI-бот на OpenRouter. Напиши что-нибудь!",
        reply_markup=get_main_keyboard(),
    )


@router.message(ChatStates.chatting)
async def chat_handler(message: types.Message, state: FSMContext) -> None:
    if message.from_user is None:
        logger.warning("Message received with no from_user")
        await message.answer("⚠️ Не удалось определить пользователя.")
        return

    if not message.text:
        logger.warning(f"Empty message from user_id={message.from_user.id}")
        await message.answer("⚠️ Пустое сообщение не отправлено.")
        return

    if message.bot is None:
        logger.error(f"Bot is None for user_id={message.from_user.id}")
        await message.answer("⚠️ Ошибка: бот не найден.")
        return

    user_id = message.from_user.id
    logger.info(f"User {user_id} says: {message.text}")

    history = user_histories.get(user_id)
    if not history:
        history = [{"role": "system", "content": "You are a helpful AI assistant."}]
        user_histories[user_id] = history

    history.append({"role": "user", "content": message.text})

    await message.bot.send_chat_action(message.chat.id, "typing")

    try:
        response = await get_openrouter_response(history)
    except Exception as e:
        logger.exception(f"Error calling OpenRouter for user_id={user_id}: {e}")
        await message.answer(f"⚠️ Ошибка запроса: {e}")
        return

    history.append({"role": "assistant", "content": response})
    await message.answer(response, reply_markup=get_main_keyboard())
