import asyncio
import logging
import time
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, ConversationHandler, filters

logging.basicConfig(level=logging.INFO)

TOKEN = "8694643746:AAF5fmxZNN1JZ2nq3WT4l1O9qJ5wiRUZsA8"
CHAT_LINK = "https://t.me/popa0193"
SUPPORT_USERNAME = "@mix_929"
ADMIN_ID = 6901387556
REVIEW_CHAT_ID = Nonе 

# Состояния
NAME, SPAWN, FLAG, CONFIRM, CHANGE_MENU, CHANGE_NAME, CHANGE_SPAWN, CHANGE_FLAG = range(8)
REVIEW_WRITE = 99

# Счётчики
season_number = 1
country_counter = {}
reviews = {}  # {user_id: {"username": str, "review": str, "date": str}}

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🍏 Вход в РП", callback_data="enter_rp")],
        [InlineKeyboardButton("⚙️ Механика", callback_data="mechanics")],
        [InlineKeyboardButton("📖 Описание мира", callback_data="world_desc")],
        [InlineKeyboardButton("🏛 Основать страну", callback_data="create_country")],
        [InlineKeyboardButton("📋 Стартовые условия", callback_data="start_conditions")],
        [InlineKeyboardButton("⭐ Отзывы", callback_data="reviews_menu")],
        [InlineKeyboardButton("📞 Поддержка", callback_data="support")]
    ]
    return InlineKeyboardMarkup(keyboard)

def reviews_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("✍️ Написать отзыв", callback_data="write_review")],
        [InlineKeyboardButton("📋 Читать отзывы", callback_data="read_reviews")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== СТАРТ ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🍎 <b>Добро пожаловать в Яблочное РП!</b>\n\n"
        "Это уникальная ролевая игра, где ты можешь основать свою страну, "
        "развивать её и участвовать в мировых событиях.\n\n"
        "Нажми <b>«Меню»</b> ниже, чтобы увидеть все доступные действия."
    )
    await update.message.reply_html(text, reply_markup=main_menu())

# ========== ОСНОВНЫЕ КНОПКИ ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "enter_rp":
        text = (
            "🤖 <b>Проверка на бота</b>\n\n"
            "Подтверди, что ты не бот, нажав кнопку ниже.\n"
            "После подтверждения ты получишь доступ к чату РП."
        )
        keyboard = [
            [InlineKeyboardButton("✅ Я не бот", callback_data="verify_human")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "verify_human":
        text = (
            "🎉 <b>Подтверждение пройдено!</b>\n\n"
            "Нажми кнопку ниже, чтобы перейти в чат РП."
        )
        keyboard = [
            [InlineKeyboardButton("🍏 Перейти в чат РП", url=CHAT_LINK)],
            [InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "mechanics":
        text = (
            "⚙️ <b>Механика игры</b>\n\n"
            "🚫 <b>Сезон не начался</b>\n\n"
            "Информация о механике появится позже. Следи за обновлениями!"
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "world_desc":
        text = (
            "📖 <b>Описание мира</b>\n\n"
            "🚫 <b>Сезон не начался</b>\n\n"
            "Описание мира будет доступно с началом сезона."
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "create_country":
        text = (
            "🏛 <b>Основать страну</b>\n\n"
            "Создай свою страну, но обязательно ознакомься со <b>стартовыми условиями</b> в меню!\n\n"
            "Готов начать?"
        )
        keyboard = [
            [InlineKeyboardButton("🏁 Начать основывать страну", callback_data="start_create")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "start_conditions":
        text = (
            "📋 <b>Стартовые условия</b>\n\n"
            "🚫 <b>Сезон не начался</b>\n\n"
            "Стартовые условия будут объявлены перед началом сезона."
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "support":
        text = (
            "📞 <b>Поддержка</b>\n\n"
            "Если хочешь что-то предложить или есть вопросы — обратись к <b>ИМПЕРАТОРУ</b> этого РП.\n\n"
            f"Связь с ИМПЕРАТОРОМ: {SUPPORT_USERNAME}"
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "reviews_menu":
        text = "⭐ <b>Отзывы</b>\n\nХочешь почитать отзывы или оставить свой?"
        await query.edit_message_text(text, reply_markup=reviews_menu_keyboard(), parse_mode="HTML")

    elif query.data == "read_reviews":
        if not reviews:
            text = "📋 <b>Отзывы</b>\n\nПока нет ни одного отзыва. Будь первым! 🌟"
        else:
            text = "📋 <b>Отзывы наших игроков:</b>\n\n"
            for uid, data in reviews.items():
                text += f"👤 @{data['username']}\n💬 {data['review']}\n📅 {data['date']}\n{'─'*20}\n"
        keyboard = [[InlineKeyboardButton("✍️ Написать отзыв", callback_data="write_review")],
                    [InlineKeyboardButton("🔙 Назад", callback_data="reviews_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "back_to_menu":
        text = "🍎 <b>Яблочное РП</b>\n\nВыбери действие:"
        await query.edit_message_text(text, reply_markup=main_menu(), parse_mode="HTML")

# ========== НАПИСАНИЕ ОТЗЫВА ==========
async def write_review_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "✍️ <b>Написать отзыв</b>\n\n"
        "Поделись своим мнением о нашем РП! Что нравится? Что хотелось бы улучшить?\n\n"
        "<i>Просто напиши свой отзыв одним сообщением.</i>"
    )
    keyboard = [[InlineKeyboardButton("🔙 Отмена", callback_data="reviews_menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return REVIEW_WRITE

async def review_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    review_text = update.message.text
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    reviews[user.id] = {
        "username": user.username or f"user_{user.id}",
        "review": review_text,
        "date": now
    }

    text = (
        "🌟 <b>Спасибо за отзыв!</b>\n\n"
        "Твоё мнение очень важно для нас. Оно поможет сделать Яблочное РП ещё лучше!"
    )
    keyboard = [[InlineKeyboardButton("📋 Читать отзывы", callback_data="read_reviews")],
                [InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")]]
    await update.message.reply_html(text, reply_markup=InlineKeyboardMarkup(keyboard))

    # Отправка в чат если указан
    if REVIEW_CHAT_ID:
        chat_text = (
            "📢 <b>Новый отзыв!</b>\n\n"
            f"👤 @{user.username or f'user_{user.id}'}\n"
            f"💬 {review_text}\n"
            f"📅 {now}"
        )
        try:
            await context.bot.send_message(chat_id=REVIEW_CHAT_ID, text=chat_text, parse_mode="HTML")
        except Exception as e:
            logging.error(f"Ошибка отправки отзыва в чат: {e}")

    return ConversationHandler.END

async def cancel_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "⭐ <b>Отзывы</b>\n\nХочешь почитать отзывы или оставить свой?"
    await query.edit_message_text(text, reply_markup=reviews_menu_keyboard(), parse_mode="HTML")
    return ConversationHandler.END

# ========== ЕЖЕНЕДЕЛЬНАЯ РАССЫЛКА ==========
async def weekly_review_request(context: ContextTypes.DEFAULT_TYPE):
    if REVIEW_CHAT_ID:
        text = (
            "🌟 <b>Дорогие игроки Яблочного РП!</b>\n\n"
            "Вам нравится наше РП? Мы хотим стать ещё лучше!\n\n"
            "Пожалуйста, оставьте свой отзыв — нам важно ваше мнение."
        )
        keyboard = [[InlineKeyboardButton("✍️ Написать отзыв", url=f"https://t.me/{context.bot.username}?start=review")]]
        try:
            await context.bot.send_message(chat_id=REVIEW_CHAT_ID, text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        except Exception as e:
            logging.error(f"Ошибка еженедельной рассылки: {e}")

# ========== СОЗДАНИЕ СТРАНЫ ==========
async def start_create_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "🏛 <b>Шаг 1:</b> Напиши <b>название</b> своей страны:"
    await query.edit_message_text(text, parse_mode="HTML")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["country_name"] = update.message.text
    text = "🗺 <b>Шаг 2:</b> Скинь <b>место спавна</b> твоей страны (опиши или скинь карту/скрин):"
    await update.message.reply_html(text)
    return SPAWN

async def get_spawn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["spawn_photo"] = update.message.photo[-1].file_id
        context.user_data["spawn_text"] = ""
    else:
        context.user_data["spawn_text"] = update.message.text
        context.user_data["spawn_photo"] = None

    keyboard = [[InlineKeyboardButton("⏭ Пропустить", callback_data="skip_flag")]]
    text = "🏴 <b>Шаг 3:</b> Скинь <b>флаг</b> твоей страны <i>(необязательно)</i>:"
    await update.message.reply_html(text, reply_markup=InlineKeyboardMarkup(keyboard))
    return FLAG

async def get_flag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["flag_photo"] = update.message.photo[-1].file_id
    else:
        context.user_data["flag_photo"] = None
    return await show_summary(update, context)

async def skip_flag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["flag_photo"] = None
    return await show_summary_callback(query, context)

async def show_summary(update, context):
    name = context.user_data.get("country_name", "Не указано")
    spawn = "✅ Есть" if context.user_data.get("spawn_photo") or context.user_data.get("spawn_text") else "❌ Нет"
    flag = "✅ Есть" if context.user_data.get("flag_photo") else "❌ Пропущено"

    text = (
        "📋 <b>Итог создания страны:</b>\n\n"
        f"🏛 Название: <b>{name}</b>\n"
        f"🗺 Спавн: {spawn}\n"
        f"🏴 Флаг: {flag}\n\n"
        "Хочешь что-то изменить?"
    )
    keyboard = [
        [InlineKeyboardButton("✏️ Поменять", callback_data="change_something")],
        [InlineKeyboardButton("✅ Подтвердить", callback_data="confirm_country")]
    ]
    if hasattr(update, 'callback_query'):
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    else:
        await update.message.reply_html(text, reply_markup=InlineKeyboardMarkup(keyboard))
    return CONFIRM

async def show_summary_callback(query, context):
    name = context.user_data.get("country_name", "Не указано")
    spawn = "✅ Есть" if context.user_data.get("spawn_photo") or context.user_data.get("spawn_text") else "❌ Нет"
    flag = "✅ Есть" if context.user_data.get("flag_photo") else "❌ Пропущено"

    text = (
        "📋 <b>Итог создания страны:</b>\n\n"
        f"🏛 Название: <b>{name}</b>\n"
        f"🗺 Спавн: {spawn}\n"
        f"🏴 Флаг: {flag}\n\n"
        "Хочешь что-то изменить?"
    )
    keyboard = [
        [InlineKeyboardButton("✏️ Поменять", callback_data="change_something")],
        [InlineKeyboardButton("✅ Подтвердить", callback_data="confirm_country")]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return CONFIRM

async def change_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "✏️ Что хочешь поменять?"
    keyboard = [
        [InlineKeyboardButton("🏛 Название", callback_data="change_name")],
        [InlineKeyboardButton("🗺 Спавн", callback_data="change_spawn")],
        [InlineKeyboardButton("🏴 Флаг", callback_data="change_flag")],
        [InlineKeyboardButton("✅ ОК, подтвердить", callback_data="confirm_country")]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return CHANGE_MENU

async def change_name_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🏛 Напиши новое <b>название</b> страны:", parse_mode="HTML")
    return CHANGE_NAME

async def change_name_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["country_name"] = update.message.text
    return await show_summary(update, context)

async def change_spawn_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🗺 Скинь новое <b>место спавна</b>:", parse_mode="HTML")
    return CHANGE_SPAWN

async def change_spawn_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["spawn_photo"] = update.message.photo[-1].file_id
        context.user_data["spawn_text"] = ""
    else:
        context.user_data["spawn_text"] = update.message.text
        context.user_data["spawn_photo"] = None
    return await show_summary(update, context)

async def change_flag_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("⏭ Пропустить", callback_data="skip_flag_change")]]
    await query.edit_message_text("🏴 Скинь новый <b>флаг</b>:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return CHANGE_FLAG

async def change_flag_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["flag_photo"] = update.message.photo[-1].file_id
    return await show_summary(update, context)

async def skip_flag_change(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["flag_photo"] = None
    return await show_summary_callback(query, context)

async def confirm_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    global season_number, country_counter
    if season_number not in country_counter:
        country_counter[season_number] = 0
    country_counter[season_number] += 1
    country_num = country_counter[season_number]

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    name = context.user_data.get("country_name", "Не указано")
    spawn_photo = context.user_data.get("spawn_photo")
    spawn_text = context.user_data.get("spawn_text")
    flag_photo = context.user_data.get("flag_photo")

    text = (
        "✅ <b>Страна успешно основана!</b>\n\n"
        f"🏛 Название: <b>{name}</b>\n"
        f"📅 Сезон: <b>{season_number}</b>\n"
        f"🔢 Твоя страна: <b>{country_num}-я</b> в этом сезоне\n"
        f"🕒 Время создания: {now}\n\n"
        "Ожидай начала сезона!"
    )
    keyboard = [[InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    if ADMIN_ID:
        admin_text = (
            "📢 <b>Новая страна основана!</b>\n\n"
            f"👤 Юзер: @{user.username or 'нет юзернейма'} (ID: {user.id})\n"
            f"🏛 Название: <b>{name}</b>\n"
            f"📅 Сезон: <b>{season_number}</b>\n"
            f"🔢 Страна №: <b>{country_num}</b>\n"
            f"🕒 Время: {now}"
        )
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="HTML")
            if spawn_photo:
                await context.bot.send_photo(chat_id=ADMIN_ID, photo=spawn_photo, caption="🗺 Спавн страны")
            elif spawn_text:
                await context.bot.send_message(chat_id=ADMIN_ID, text=f"🗺 Спавн: {spawn_text}")
            if flag_photo:
                await context.bot.send_photo(chat_id=ADMIN_ID, photo=flag_photo, caption="🏴 Флаг страны")
        except Exception as e:
            logging.error(f"Ошибка отправки админу: {e}")

    context.user_data.clear()
    return ConversationHandler.END

async def cancel_create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "❌ Создание страны отменено."
    if update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode="HTML")
    else:
        await update.message.reply_html(text)
    context.user_data.clear()
    return ConversationHandler.END

# ========== ЗАПУСК ==========
def run_bot():
    app = Application.builder().token(TOKEN).build()

    # ConversationHandler для создания страны
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_create_country, pattern="^start_create$")],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            SPAWN: [
                MessageHandler(filters.PHOTO, get_spawn),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_spawn)
            ],
            FLAG: [
                MessageHandler(filters.PHOTO, get_flag),
                CallbackQueryHandler(skip_flag, pattern="^skip_flag$")
            ],
            CONFIRM: [
                CallbackQueryHandler(change_menu, pattern="^change_something$"),
                CallbackQueryHandler(confirm_country, pattern="^confirm_country$")
            ],
            CHANGE_MENU: [
                CallbackQueryHandler(change_name_start, pattern="^change_name$"),
                CallbackQueryHandler(change_spawn_start, pattern="^change_spawn$"),
                CallbackQueryHandler(change_flag_start, pattern="^change_flag$"),
                CallbackQueryHandler(confirm_country, pattern="^confirm_country$")
            ],
            CHANGE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_name_done)],
            CHANGE_SPAWN: [
                MessageHandler(filters.PHOTO, change_spawn_done),
                MessageHandler(filters.TEXT & ~filters.COMMAND, change_spawn_done)
            ],
            CHANGE_FLAG: [
                MessageHandler(filters.PHOTO, change_flag_done),
                CallbackQueryHandler(skip_flag_change, pattern="^skip_flag_change$")
            ],
        },
        fallbacks=[CallbackQueryHandler(cancel_create, pattern="^back_to_menu$")],
    )

    # ConversationHandler для отзывов
    review_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(write_review_start, pattern="^write_review$")],
        states={
            REVIEW_WRITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, review_received)]
        },
        fallbacks=[CallbackQueryHandler(cancel_review, pattern="^reviews_menu$")],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(review_handler)
    app.add_handler(CallbackQueryHandler(button_handler))

    # Еженедельная рассылка (раз в 7 дней)
    app.job_queue.run_repeating(weekly_review_request, interval=604800, first=10)

    print("Бот запущен!")
    app.run_polling()

def main():
    while True:
        try:
            run_bot()
        except Exception as e:
            print(f"Ошибка: {e}. Перезапуск через 5 сек...")
            time.sleep(5)

if __name__ == "__main__":
    main()
