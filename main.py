#  |-----------------------------------------------------|
#  | \                                                 / |
#  |  \/-27|09|2026-------------------------------16-\/  |
#  |   |                                             |   |
#  |   |----->___(Resender-Assistant-Bot-0-3)___ <---|   |
#  |   |                                             |   |
#  |  /\-14:53-----------------------------------182-/\  |
#  | /                                                 \ |
#  |-----------------------------------------------------|



#1st----------> libs/modules 

#---------- import

import asyncio
import logging
import os

#---------- from ... import ...

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

#1fn----------> libs/modules 

#2st----------> logging for errors 

logging.basicConfig(level = logging.INFO)

#2fn----------> logging for errors 



#3st----------> bot settings  

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN не найден. Добавьте его в файл .env")

bot = Bot(token=TOKEN)

dp = Dispatcher()

#3fn----------> bot setting



#4st---------> ADMIN settings

ADMIN_ID_RAW = os.getenv("ADMIN_ID_RAW", "")

try:
    ADMIN_ID = int(ADMIN_ID_RAW)
except ValueError:
    ADMIN_ID = 0

#4fn---------> ADMIN settings



#5st---------> FSM (Waiting for message)

class ContactStates(StatesGroup):
    waiting_for_message = State()

#5fn---------> FSM (Waiting for message)



#6st--------> Keyboards 

def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✉️ Написать разработчику", callback_data="btn_write"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🛠 Стек технологий", callback_data="btn_stack"
                ),
                InlineKeyboardButton(
                    text="💼 Проекты (GitHub)",
                    url="https://github.com/Nortueso",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📄 О разработчике", callback_data="btn_about"
                )
            ],
        ]
    )


def get_cancel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="btn_cancel")]
        ]
    )

#6fn--------> Keyboards 



#7st----------> /start

@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    text = (
        f"👋 Здравствуйте, {message.from_user.first_name}!\n\n"
      "Я — **персональный ассистент разработчика Nortueso**.\n\n"
      "🔹 **Специализация:** Python Backend Developer\n"
      "🔹 **Основной стек:** FastAPI · PostgreSQL · Docker · aiogram\n\n"
        "Вы можете ознакомиться с информацией о навыках или "
        "**отправить сообщение напрямую автору** через этого бота."
    )
    await message.answer(
        text, parse_mode="Markdown", reply_markup=get_main_keyboard()
    )

#7st----------> /start



#7.1st--------> /start(stack)

@dp.callback_query(F.data == "btn_stack")
async def cb_stack(callback: types.CallbackQuery):
    text = (
      "🛠 **Технологический стек Nortueso:**\n\n"
      "• **Языки:** Python (3.11+), SQL, Bash\n"
      "• **Фреймворки:** FastAPI, aiogram 3.x\n"
      "• **Базы данных:** PostgreSQL, SQLite, SQLAlchemy 2.0 (async), Alembic\n"
      "• **Кэш и очереди:** Redis, Celery (базовый уровень)\n"
      "• **DevOps & окружение:** Docker, Docker Compose, Git, Linux/macOS\n"
      "• **Тестирование:** Pytest"
    )
    await callback.message.answer(
        text, parse_mode="Markdown", reply_markup=get_main_keyboard()
    )
    await callback.answer()

#7.1fn--------> /start(stack)



#7.2st---------> /start(about me)

@dp.callback_query(F.data == "btn_about")
async def cb_about(callback: types.CallbackQuery):
    text = (
      "👨‍💻 **О разработчике:**\n\n"
        "Backend-разработчик, специализируюсь на создании асинхронных микросервисов, "
        "проектировании REST API, интеграции баз данных и разработке Telegram-ботов.\n\n"
        "📍 Локация: Remote / Relocation ready\n"
        "🌐 GitHub: [github.com/Nortueso](https://github.com/Nortueso)"
    )
    await callback.message.answer(
        text,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=get_main_keyboard(),
    )
    await callback.answer()

#7.2st---------> /start(about me)



#7.3st-----------> start to sendung messages

@dp.callback_query(F.data == "btn_write")
async def cb_write(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
      "📝 **Напишите ваше сообщение** (предложение о работе, проект или вопрос).\n\n"
        "Вы можете отправить текст, файл или голосовое сообщение. Я мгновенно передам его разработчику.",
        parse_mode="Markdown",
        reply_markup=get_cancel_keyboard(),
    )
    await state.set_state(ContactStates.waiting_for_message)
    await callback.answer()


@dp.callback_query(F.data == "btn_cancel")
async def cb_cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "Действие отменено.", reply_markup=get_main_keyboard()
    )
    await callback.answer()

#7.3fn-----------> start to sendung messages



#7.4st-----------> sending message to you

@dp.message(ContactStates.waiting_for_message)
async def process_user_message(message: types.Message, state: FSMContext):
    await state.clear()

    if not ADMIN_ID:
        await message.answer(
        "⚠️ Ошибка конфигурации бота: ADMIN_ID не настроен.",
        reply_markup=get_main_keyboard(),
    )
        return

    sender = message.from_user
    username = f"@{sender.username}" if sender.username else "без username"
    sender_info = (
      f"📬 **Новое входящее сообщение от рекрутера/клиента!**\n\n"
      f"👤 **От:** {sender.full_name} ({username})\n"
      f"🆔 **ID:** `{sender.id}`\n\n"
      f"⬇️ *Сообщение прикреплено ниже (для ответа сделай Reply на него):*"
    )

    # Отправляем карточку отправителя и пересылаем сам контент
    await bot.send_message(ADMIN_ID, sender_info, parse_mode="Markdown")
    await message.forward(ADMIN_ID)

    await message.answer(
      "✅ **Ваше сообщение передано разработчику!**\n\n"
        "Nortueso ответит вам здесь в ближайшее время.",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(),
    )

#7.4fn-----------> sending message to you



#7.5st------------> sending your answer

dp.message(F.chat.id == ADMIN_ID, F.reply_to_message)
async def admin_reply(message: types.Message):
    replied = message.reply_to_message
    target_user_id = None

    # Проверяем, откуда брать ID пользователя
    if replied.forward_from:
        target_user_id = replied.forward_from.id
    else:
    # Если пересылка скрыта приватностью пользователя Telegram
        lines = (replied.text or "").split("\n")
    for line in lines:
      if "🆔 **ID:**" in line:
        raw_id = line.replace("🆔 **ID:**", "").replace("`", "").strip()
        if raw_id.isdigit():
            target_user_id = int(raw_id)
            break

    if not target_user_id:
        await message.answer(
        "❌ Не удалось определить адресата. Сделай ответ (Reply) на карточку с ID пользователя."
    )
        return

    try:
        if message.text:
            await bot.send_message(
            target_user_id,
            f"💬 **Ответ от Nortueso:**\n\n{message.text}",
            parse_mode="Markdown",
            )
        else:
            await message.copy_to(target_user_id)

        await message.answer("✅ Ответ успешно доставлен собеседнику!")
    except Exception as e:
        await message.answer(f"❌ Ошибка отправки: {e}")


#7.5st------------> sending your answer



#8st--------------> turning on

async def main():
    print("🚀 Бот-ассистент Nortueso готов к приёму сообщений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

#8fn--------------> turning on
