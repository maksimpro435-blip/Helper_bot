import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties

logging.basicConfig(level=logging.INFO)

TOKEN = "8721151214:AAEQFF012KV1ZViqxoiLp523XRV4ZhyG2Bs"
CHAT_LINK = "https://t.me/popa0193"
SUPPORT_USERNAME = "@mix_929"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍏 Вход в РП", callback_data="enter_rp")],
        [InlineKeyboardButton(text="⚙️ Механика", callback_data="mechanics")],
        [InlineKeyboardButton(text="📖 Описание мира", callback_data="world_desc")],
        [InlineKeyboardButton(text="🏛 Создать страну", callback_data="create_country")],
        [InlineKeyboardButton(text="📋 Стартовые условия", callback_data="start_conditions")],
        [InlineKeyboardButton(text="📞 Поддержка", callback_data="support")]
    ])
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "🍎 <b>Добро пожаловать в Яблочное РП!</b>\n\n"
        "Это уникальная ролевая игра, где ты можешь создать свою страну, "
        "развивать её и участвовать в мировых событиях.\n\n"
        "Нажми <b>«Меню»</b> ниже, чтобы увидеть все доступные действия."
    )
    await message.answer(text, reply_markup=main_menu())

@dp.callback_query()
async def handle_callback(call: types.CallbackQuery):
    if call.data == "enter_rp":
        text = (
            "🤖 <b>Проверка на бота</b>\n\n"
            "Подтверди, что ты не бот, нажав кнопку ниже.\n"
            "После подтверждения ты получишь ссылку на чат РП."
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я не бот", callback_data="verify_human")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
        await call.message.edit_text(text, reply_markup=keyboard)

    elif call.data == "verify_human":
        text = (
            "🎉 <b>Подтверждение пройдено!</b>\n\n"
            f"Вот ссылка на чат РП: {CHAT_LINK}\n\n"
            "Присоединяйся и начинай игру!"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu")]
        ])
        await call.message.edit_text(text, reply_markup=keyboard)

    elif call.data == "mechanics":
        text = (
            "⚙️ <b>Механика игры</b>\n\n"
            "🚫 <b>Сезон не начался</b>\n\n"
            "Информация о механике появится позже. Следи за обновлениями!"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
        await call.message.edit_text(text, reply_markup=keyboard)

    elif call.data == "world_desc":
        text = (
            "📖 <b>Описание мира</b>\n\n"
            "🚫 <b>Сезон не начался</b>\n\n"
            "Описание мира будет доступно с началом сезона."
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
        await call.message.edit_text(text, reply_markup=keyboard)

    elif call.data == "create_country":
        text = (
            "🏛 <b>Создать страну</b>\n\n"
            "🚫 <b>Сезон не начался</b>\n\n"
            "Создание стран откроется, когда начнётся сезон."
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
        await call.message.edit_text(text, reply_markup=keyboard)

    elif call.data == "start_conditions":
        text = (
            "📋 <b>Стартовые условия</b>\n\n"
            "🚫 <b>Сезон не начался</b>\n\n"
            "Стартовые условия будут объявлены перед началом сезона."
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
        await call.message.edit_text(text, reply_markup=keyboard)

    elif call.data == "support":
        text = (
            "📞 <b>Поддержка</b>\n\n"
            "Если хочешь что-то предложить или есть вопросы — обратись к <b>ИМПЕРАТОРУ</b> этого РП.\n\n"
            f"Связь с ИМПЕРАТОРОМ: {SUPPORT_USERNAME}"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
        await call.message.edit_text(text, reply_markup=keyboard)

    elif call.data == "back_to_menu":
        text = (
            "🍎 <b>Яблочное РП</b>\n\n"
            "Выбери действие:"
        )
        await call.message.edit_text(text, reply_markup=main_menu())

    await call.answer()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
