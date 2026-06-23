import asyncio
import logging
import time
import random
import threading
import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, ConversationHandler, filters

logging.basicConfig(level=logging.INFO)

TOKEN = "8694643746:AAGv6pju1GKvnQmY878Qf4Hyf1wzz0l4z-k"
CHAT_LINK = "https://t.me/joinchat/75xD5Z_btvliOGJi"
SUPPORT_USERNAME = "@mix_929"
ADMIN_ID = 6901387556
REVIEW_CHAT_ID = -1003644060282
BOOST_LINK = "https://t.me/boost/popa0193"
INVITE_LINK = "https://t.me/joinchat/75xD5Z_btvliOGJi"

NAME, SPAWN, FLAG, CONFIRM, CHANGE_MENU, CHANGE_NAME, CHANGE_SPAWN, CHANGE_FLAG = range(8)
REVIEW_WRITE, REVIEW_RATING = 99, 100

season_number = 1
country_counter = {}
countries = {}
pending_countries = {}

REVIEWS_FILE = "reviews.json"
COUNTRIES_FILE = "countries.json"
PENDING_FILE = "pending.json"

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

reviews = load_json(REVIEWS_FILE)
countries = load_json(COUNTRIES_FILE)
pending_countries = load_json(PENDING_FILE)

if countries:
    max_num = max(c.get("number", 0) for c in countries.values())
    country_counter[season_number] = max_num
else:
    country_counter[season_number] = 0

def main_menu():
    keyboard = [
        [InlineKeyboardButton("⚙️ Механика", callback_data="mechanics")],
        [InlineKeyboardButton("🏛 Основать страну", callback_data="create_country")],
        [InlineKeyboardButton("📋 Стартовые условия", callback_data="start_conditions")],
        [InlineKeyboardButton("🌍 Страны", callback_data="countries_list")],
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

def rating_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton(str(i), callback_data=f"rate_{i}") for i in range(1, 6)]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🍎 <b>Добро пожаловать в Яблочное РП!</b>\n\n"
        "🌍 Это уникальная ролевая игра, где ты можешь основать свою страну, "
        "развивать её и вершить судьбу целого мира.\n\n"
        "⚔️ Войны, дипломатия, экономика — всё в твоих руках.\n\n"
        "<i>Готов войти в историю?</i>"
    )
    keyboard = [
        [InlineKeyboardButton("📋 Перейти в меню", callback_data="back_to_menu")],
        [InlineKeyboardButton("🍏 Вход в РП", callback_data="enter_rp")],
        [InlineKeyboardButton("📖 О игре", callback_data="about_game")]
    ]
    await update.message.reply_html(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "enter_rp":
        text = (
            "🤖 <b>Проверка на бота</b>\n\n"
            "Нажми кнопку ниже чтобы подтвердить что ты человек."
        )
        keyboard = [
            [InlineKeyboardButton("✅ Я не бот", callback_data="verify_human")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_start")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "verify_human":
        text = "🎉 <b>Готово!</b>\n\nНажми кнопку ниже чтобы перейти в чат РП."
        keyboard = [
            [InlineKeyboardButton("🍏 Перейти в чат РП", url=CHAT_LINK)],
            [InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "back_to_start":
        await start(update, context)

    elif query.data == "about_game":
        text = (
            "🍎 <b>Яблочное РП — лучшее РП!</b>\n\n"
            "🏆 Уникальная система создания государств\n"
            "⚔️ Войны, дипломатия, экономика\n"
            "🌍 Активное сообщество игроков\n\n"
            "👑 ИМПЕРАТОР создал этот мир для тебя.\n"
            "🔥 Присоединяйся и стань частью истории!"
        )
        keyboard = [
            [InlineKeyboardButton("🍏 Войти в РП", callback_data="enter_rp")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_start")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "mechanics":
        text = (
            "🌍 <b>ЯБЛОЧНОЕ РП — ЕДИНАЯ СИСТЕМА МИРА</b>\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "<b>1. СУТЬ ИГРЫ</b>\n\n"
            "Геополитическая стратегия. Каждый управляет государством.\n"
            "Цель: развить страну, решить проблемы, выжить в кризисах.\n"
            "1 день = 1 игровой год.\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "<b>2. СОЗДАНИЕ ГОСУДАРСТВА</b>\n\n"
            "Игрок указывает: название, флаг, точку спавна.\n"
            "Экономика и армия НЕ выбираются.\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "<b>3. СИСТЕМА СПАВНА</b>\n\n"
            "Спавн = кризисная зона. Игрок получает проблемы:\n"
            "нестабильность, слабую армию, угрозы, нехватку ресурсов.\n"
            "👉 Игрок начинает проблемным.\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "<b>4. ЭПОХИ</b>\n\n"
            "Древние эпохи — племена, конфликты\n"
            "Средние века — феодалы, локальные войны\n"
            "Индустриальная — заводы, армии с техникой\n"
            "Современная — экономика, регулярные армии\n"
            "Новейшая — наука, технологии\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "<b>5. РОЛЬ ИГРОКА</b>\n\n"
            "Стабилизация, реформы, развитие, войны, дипломатия.\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "<b>6. ЗАПРЕТ НА ИМБУ</b>\n\n"
            "❌ Мгновенное развитие\n"
            "❌ Армия с нуля\n"
            "❌ Захват мира за день\n"
            "❌ Игнор экономики\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🏆 <b>ИТОГ:</b> Игра про выживание и долгий рост."
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "create_country":
        text = "🏛 <b>Основать страну</b>\n\nОзнакомься со стартовыми условиями в меню.\n\nГотов?"
        keyboard = [
            [InlineKeyboardButton("🏁 Начать основывать страну", callback_data="start_create")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "start_conditions":
        text = (
            "📋 <b>СТАРТОВЫЕ УСЛОВИЯ — ГОД 1200</b>\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "👥 Население до 100 000 чел, деревни, города формируются\n"
            "🏰 Власть феодалов, регионы независимы\n"
            "💰 Воровство бюджета, программы не работают\n"
            "🛤 Слабая связь, страна «разорвана»\n"
            "📦 Нет единой экономики между областями\n"
            "🔨 Ремесленничество, нет промышленности\n"
            "⚔️ Армия слабая или отсутствует\n"
            "🛠 Низкие технологии, ручной труд\n"
            "📉 Дефицит товаров, рынок нестабилен\n"
            "💸 Слабая экономика, нет бюджета\n"
            "⚠️ Риск распада при кризисе\n"
            "🏚 Политическая нестабильность\n"
            "🚫 Нет центрального контроля\n"
            "💀 Риск коллапса при войне или голоде"
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "countries_list":
        if not countries:
            text = "🌍 <b>Список стран пуст</b>\n\nБудь первым!"
        else:
            text = "🌍 <b>ОСНОВАННЫЕ СТРАНЫ:</b>\n\n"
            for uid, data in countries.items():
                text += f"🏛 {data['name']}\n👤 @{data['username']}\n🔢 №{data['number']}\n📅 {data['date']}\n{'─'*20}\n"
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "support":
        text = f"📞 <b>Поддержка</b>\n\nОбратись к ИМПЕРАТОРУ: {SUPPORT_USERNAME}"
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "reviews_menu":
        if reviews:
            ratings = [r["rating"] for r in reviews.values() if "rating" in r]
            avg = sum(ratings) / len(ratings) if ratings else 0
            rating_text = f"\n⭐ Средняя оценка: <b>{avg:.2f}</b> ({len(ratings)} отзывов)"
        else:
            rating_text = ""
        text = f"⭐ <b>Отзывы</b>{rating_text}\n\nВыбери действие:"
        await query.edit_message_text(text, reply_markup=reviews_menu_keyboard(), parse_mode="HTML")

    elif query.data == "read_reviews":
        if not reviews:
            text = "📋 <b>Отзывы</b>\n\nПока нет отзывов. Будь первым! 🌟"
        else:
            ratings = [r["rating"] for r in reviews.values() if "rating" in r]
            avg = sum(ratings) / len(ratings) if ratings else 0
            text = f"📋 <b>Отзывы:</b>\n⭐ Средняя оценка: <b>{avg:.2f}</b>\n\n"
            for uid, data in reviews.items():
                stars = "⭐" * data.get("rating", 0)
                text += f"👤 @{data['username']} {stars}\n💬 {data['review']}\n📅 {data['date']}\n{'─'*20}\n"
        keyboard = [
            [InlineKeyboardButton("✍️ Написать отзыв", callback_data="write_review")],
            [InlineKeyboardButton("🔙 Назад", callback_data="reviews_menu")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "back_to_menu":
        text = "🍎 <b>Яблочное РП</b>\n\nВыбери действие:"
        await query.edit_message_text(text, reply_markup=main_menu(), parse_mode="HTML")

async def write_review_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "✍️ <b>Написать отзыв</b>\n\nНапиши одним сообщением:"
    keyboard = [[InlineKeyboardButton("🔙 Отмена", callback_data="reviews_menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return REVIEW_WRITE

async def review_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["review_text"] = update.message.text
    text = "⭐ <b>Оцени от 1 до 5:</b>"
    await update.message.reply_html(text, reply_markup=rating_keyboard())
    return REVIEW_RATING

async def review_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    rating = int(query.data.split("_")[1])
    user = query.from_user
    review_text = context.user_data.get("review_text", "")
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    reviews[str(user.id)] = {
        "username": user.username or f"user_{user.id}",
        "review": review_text,
        "rating": rating,
        "date": now
    }
    save_json(REVIEWS_FILE, reviews)

    stars = "⭐" * rating
    text = f"🌟 <b>Спасибо за отзыв!</b>\n\nОценка: {stars}"
    keyboard = [
        [InlineKeyboardButton("📋 Читать отзывы", callback_data="read_reviews")],
        [InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    if REVIEW_CHAT_ID:
        try:
            await context.bot.send_message(
                chat_id=REVIEW_CHAT_ID,
                text=f"📢 Новый отзыв!\n👤 @{user.username}\n⭐ {rating}/5\n💬 {review_text}",
                parse_mode="HTML"
            )
        except:
            pass

    context.user_data.clear()
    return ConversationHandler.END

async def cancel_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "⭐ <b>Отзывы</b>\n\nВыбери действие:"
    await query.edit_message_text(text, reply_markup=reviews_menu_keyboard(), parse_mode="HTML")
    return ConversationHandler.END

async def periodic_message(context: ContextTypes.DEFAULT_TYPE):
    if not REVIEW_CHAT_ID:
        return
    delay = random.randint(0, 840)
    await asyncio.sleep(delay)

    messages = [
        (["🌟 Оставьте отзыв!", "💭 Ваше мнение важно!", "📝 Напиши отзыв!", "🍎 Расскажи о РП!", "✨ Помоги стать лучше!"],
         [[InlineKeyboardButton("✍️ Написать отзыв", url=f"https://t.me/{context.bot.username}?start=review")]]),
        (["👥 Пригласи друзей!", "🚀 Играйте вместе!", "🔥 Больше игроков!", "🎯 Собери команду!", "💎 Вместе веселее!"],
         [[InlineKeyboardButton("🔗 Присоединиться", url=INVITE_LINK)]]),
        (["⭐ Проголосуй за РП!", "🏆 Подними в рейтинге!", "📊 Твой голос важен!", "🔝 В топ вместе!", "💪 Сила сообщества!"],
         [[InlineKeyboardButton("⭐ Проголосовать", url=BOOST_LINK)]]),
        (["👑 Поддержи ИМПЕРАТОРА!", "🎁 Отправь подарок!", "💝 ИМПЕРАТОР старается!", "🏅 Скажи спасибо!", "🌟 Поддержи развитие!"],
         [[InlineKeyboardButton("🎁 Отправить подарок", url=f"https://t.me/{SUPPORT_USERNAME.replace('@', '')}")]])
    ]

    category = random.randint(0, 3)
    text = random.choice(messages[category][0])
    kb = messages[category][1]

    try:
        await context.bot.send_message(chat_id=REVIEW_CHAT_ID, text=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
    except:
        pass

async def start_create_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "🏛 <b>Шаг 1/3:</b> Напиши <b>название</b> страны:"
    await query.edit_message_text(text, parse_mode="HTML")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["country_name"] = update.message.text
    text = "🗺 <b>Шаг 2/3:</b> Скинь <b>место спавна</b> (описание или скрин):"
    await update.message.reply_html(text)
    return SPAWN

async def get_spawn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["spawn_photo"] = update.message.photo[-1].file_id
        context.user_data["spawn_text"] = "(фото)"
    elif update.message.text:
        context.user_data["spawn_text"] = update.message.text
        context.user_data["spawn_photo"] = None
    else:
        await update.message.reply_html("❌ Отправь текст или фото!")
        return SPAWN

    text = "🏴 <b>Шаг 3/3:</b> Скинь <b>флаг</b> страны <b>(ОБЯЗАТЕЛЬНО)</b>:"
    await update.message.reply_html(text)
    return FLAG

async def get_flag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["flag_photo"] = update.message.photo[-1].file_id
    elif update.message.document:
        context.user_data["flag_photo"] = update.message.document.file_id
    else:
        await update.message.reply_html("❌ Флаг <b>обязателен!</b> Отправь фото или документ.")
        return FLAG

    name = context.user_data.get("country_name", "Не указано")
    spawn = "✅ Есть" if context.user_data.get("spawn_photo") or context.user_data.get("spawn_text") else "❌ Нет"
    flag = "✅ Есть"

    text = f"📋 <b>Проверь данные:</b>\n\n🏛 Название: <b>{name}</b>\n🗺 Спавн: {spawn}\n🏴 Флаг: {flag}\n\nВсё верно?"
    keyboard = [
        [InlineKeyboardButton("✏️ Исправить", callback_data="change_something")],
        [InlineKeyboardButton("📨 Отправить на проверку", callback_data="submit_to_admin")]
    ]
    await update.message.reply_html(text, reply_markup=InlineKeyboardMarkup(keyboard))
    return CONFIRM

async def change_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "✏️ Что хочешь исправить?"
    keyboard = [
        [InlineKeyboardButton("🏛 Название", callback_data="change_name")],
        [InlineKeyboardButton("🗺 Спавн", callback_data="change_spawn")],
        [InlineKeyboardButton("🏴 Флаг", callback_data="change_flag")],
        [InlineKeyboardButton("✅ ОК, всё верно", callback_data="submit_to_admin")]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    return CHANGE_MENU

async def change_name_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🏛 Напиши новое <b>название</b>:", parse_mode="HTML")
    return CHANGE_NAME

async def change_name_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["country_name"] = update.message.text
    return await show_summary_msg(update, context)

async def change_spawn_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🗺 Скинь новое <b>место спавна</b>:", parse_mode="HTML")
    return CHANGE_SPAWN

async def change_spawn_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["spawn_photo"] = update.message.photo[-1].file_id
        context.user_data["spawn_text"] = "(фото)"
    elif update.message.text:
        context.user_data["spawn_text"] = update.message.text
        context.user_data["spawn_photo"] = None
    return await show_summary_msg(update, context)

async def change_flag_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🏴 Скинь новый <b>флаг</b> (обязательно):", parse_mode="HTML")
    return CHANGE_FLAG

async def change_flag_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["flag_photo"] = update.message.photo[-1].file_id
    elif update.message.document:
        context.user_data["flag_photo"] = update.message.document.file_id
    else:
        await update.message.reply_html("❌ Отправь фото или документ!")
        return CHANGE_FLAG
    return await show_summary_msg(update, context)

async def show_summary_msg(update, context):
    name = context.user_data.get("country_name", "Не указано")
    spawn = "✅ Есть" if context.user_data.get("spawn_photo") or context.user_data.get("spawn_text") else "❌ Нет"
    flag = "✅ Есть" if context.user_data.get("flag_photo") else "❌ Нет"

    text = f"📋 <b>Проверь данные:</b>\n\n🏛 Название: <b>{name}</b>\n🗺 Спавн: {spawn}\n🏴 Флаг: {flag}\n\nВсё верно?"
    keyboard = [
        [InlineKeyboardButton("✏️ Исправить", callback_data="change_something")],
        [InlineKeyboardButton("📨 Отправить на проверку", callback_data="submit_to_admin")]
    ]
    await update.message.reply_html(text, reply_markup=InlineKeyboardMarkup(keyboard))
    return CONFIRM

async def submit_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    name = context.user_data.get("country_name", "Не указано")
    spawn_text = context.user_data.get("spawn_text", "")
    spawn_photo = context.user_data.get("spawn_photo")
    flag_photo = context.user_data.get("flag_photo")

    pending_countries[str(user.id)] = {
        "username": user.username or f"user_{user.id}",
        "name": name,
        "spawn_text": spawn_text,
        "spawn_photo": spawn_photo,
        "flag_photo": flag_photo,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M")
    }
    save_json(PENDING_FILE, pending_countries)

    await query.edit_message_text("📨 <b>Анкета отправлена на проверку!</b>\n\nОжидай решения ИМПЕРАТОРА.", parse_mode="HTML")

    if ADMIN_ID:
        admin_text = f"📢 <b>НОВАЯ ЗАЯВКА</b>\n\n👤 @{user.username or 'нет'}\n🏛 Название: <b>{name}</b>"
        keyboard = [
            [InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_{user.id}"),
             InlineKeyboardButton("❌ Отказать", callback_data=f"reject_menu_{user.id}")]
        ]
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
            if spawn_photo:
                await context.bot.send_photo(chat_id=ADMIN_ID, photo=spawn_photo, caption="🗺 Спавн")
            elif spawn_text:
                await context.bot.send_message(chat_id=ADMIN_ID, text=f"🗺 Спавн: {spawn_text}")
            if flag_photo:
                await context.bot.send_photo(chat_id=ADMIN_ID, photo=flag_photo, caption="🏴 Флаг")
        except:
            pass

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

async def admin_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID:
        return

    user_id = query.data.split("_")[1]
    if user_id not in pending_countries:
        await query.edit_message_text("❌ Заявка не найдена.")
        return

    data = pending_countries.pop(user_id)
    save_json(PENDING_FILE, pending_countries)

    global country_counter
    if season_number not in country_counter:
        country_counter[season_number] = 0
    country_counter[season_number] += 1
    country_num = country_counter[season_number]
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    countries[user_id] = {
        "name": data["name"],
        "number": country_num,
        "username": data["username"],
        "date": now
    }
    save_json(COUNTRIES_FILE, countries)

    await query.edit_message_text(f"✅ Страна <b>{data['name']}</b> одобрена! (#{country_num})", parse_mode="HTML")

    try:
        await context.bot.send_message(
            chat_id=int(user_id),
            text=f"🎉 <b>Поздравляем!</b>\n\nТвоя страна <b>{data['name']}</b> создана!\n🔢 Номер: <b>{country_num}</b>",
            parse_mode="HTML"
        )
    except:
        pass

async def admin_reject_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID:
        return

    user_id = query.data.split("_")[2]
    keyboard = [
        [InlineKeyboardButton("📏 Спавн не подходит", callback_data=f"reject_{user_id}_1")],
        [InlineKeyboardButton("📛 Название не подходит", callback_data=f"reject_{user_id}_2")],
        [InlineKeyboardButton("🔙 Отмена", callback_data=f"cancel_reject_{user_id}")]
    ]
    await query.edit_message_text("❌ <b>Выбери причину отказа:</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def admin_reject_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID:
        return

    parts = query.data.split("_")
    user_id = parts[1]
    reason_code = parts[2]

    reasons = {
        "1": "📏 Спавн не подходит. Уточни место спавна.",
        "2": "📛 Название не подходит. Выбери другое название."
    }

    if user_id in pending_countries:
        pending_countries.pop(user_id)
        save_json(PENDING_FILE, pending_countries)

    reason_text = reasons.get(reason_code, "Неизвестная причина")
    await query.edit_message_text(f"❌ Отказано.\n{reason_text}", parse_mode="HTML")

    try:
        await context.bot.send_message(
            chat_id=int(user_id),
            text=f"❌ <b>В создании страны отказано.</b>\n\nПричина: {reason_text}",
            parse_mode="HTML"
        )
    except:
        pass

async def admin_cancel_reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.data.split("_")[2]
    if user_id in pending_countries:
        data = pending_countries[user_id]
        keyboard = [
            [InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_{user_id}"),
             InlineKeyboardButton("❌ Отказать", callback_data=f"reject_menu_{user_id}")]
        ]
        await query.edit_message_text(f"📢 Заявка от @{data['username']}\n🏛 {data['name']}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        pass

def run_http():
    try:
        server = HTTPServer(('0.0.0.0', 10000), Handler)
        server.serve_forever()
    except:
        pass

def main():
    http_thread = threading.Thread(target=run_http, daemon=True)
    http_thread.start()
    time.sleep(2)

    while True:
        try:
            app = Application.builder().token(TOKEN).build()

            conv_handler = ConversationHandler(
                entry_points=[CallbackQueryHandler(start_create_country, pattern="^start_create$")],
                states={
                    NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
                    SPAWN: [MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, get_spawn)],
                    FLAG: [MessageHandler(filters.PHOTO | filters.Document.ALL, get_flag)],
                    CONFIRM: [
                        CallbackQueryHandler(change_menu, pattern="^change_something$"),
                        CallbackQueryHandler(submit_to_admin, pattern="^submit_to_admin$")
                    ],
                    CHANGE_MENU: [
                        CallbackQueryHandler(change_name_start, pattern="^change_name$"),
                        CallbackQueryHandler(change_spawn_start, pattern="^change_spawn$"),
                        CallbackQueryHandler(change_flag_start, pattern="^change_flag$"),
                        CallbackQueryHandler(submit_to_admin, pattern="^submit_to_admin$")
                    ],
                    CHANGE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_name_done)],
                    CHANGE_SPAWN: [MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, change_spawn_done)],
                    CHANGE_FLAG: [MessageHandler(filters.PHOTO | filters.Document.ALL, change_flag_done)],
                },
                fallbacks=[CallbackQueryHandler(cancel_create, pattern="^back_to_menu$")],
            )

            review_handler = ConversationHandler(
                entry_points=[CallbackQueryHandler(write_review_start, pattern="^write_review$")],
                states={
                    REVIEW_WRITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, review_received)],
                    REVIEW_RATING: [CallbackQueryHandler(review_rating, pattern="^rate_")]
                },
                fallbacks=[CallbackQueryHandler(cancel_review, pattern="^reviews_menu$")],
            )

            app.add_handler(CommandHandler("start", start))
            app.add_handler(conv_handler)
            app.add_handler(review_handler)
            app.add_handler(CallbackQueryHandler(admin_approve, pattern="^approve_"))
            app.add_handler(CallbackQueryHandler(admin_reject_menu, pattern="^reject_menu_"))
            app.add_handler(CallbackQueryHandler(admin_reject_confirm, pattern="^reject_"))
            app.add_handler(CallbackQueryHandler(admin_cancel_reject, pattern="^cancel_reject_"))
            app.add_handler(CallbackQueryHandler(button_handler))

            try:
                app.job_queue.run_repeating(periodic_message, interval=14400, first=10)
            except:
                pass

            print("Бот запущен!")
            app.run_polling(drop_pending_updates=True)

        except Exception as e:
            print(f"Ошибка: {e}. Перезапуск через 10 сек...")
            time.sleep(10)

if __name__ == "__main__":
    main()
