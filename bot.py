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

TOKEN = "8694643746:AAF5fmxZNN1JZ2nq3WT4l1O9qJ5wiRUZsA8"
CHAT_LINK = "https://t.me/+75xD5Z_btvliOGJi"  https://t.me/+75xD5Z_btvliOGJi
SUPPORT_USERNAME = "@mix_929"
ADMIN_ID = 6901387556
REVIEW_CHAT_ID = -1003644060282
BOOST_LINK = "https://t.me/boost/popa0193"
INVITE_LINK = "https://t.me/+75xD5Z_btvliOGJi"

# Состояния
NAME, SPAWN, FLAG, CONFIRM, CHANGE_MENU, CHANGE_NAME, CHANGE_SPAWN, CHANGE_FLAG = range(8)
REVIEW_WRITE, REVIEW_RATING = 99, 100

# Счётчики
season_number = 1
country_counter = {}
countries = {}  # {user_id: {"name": str, "number": int, "username": str, "date": str}}

# Отзывы
REVIEWS_FILE = "reviews.json"
COUNTRIES_FILE = "countries.json"

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

# Восстанавливаем счётчик стран из файла
if countries:
    max_num = max(c.get("number", 0) for c in countries.values())
    country_counter[season_number] = max_num
else:
    country_counter[season_number] = 0

# ========== КЛАВИАТУРЫ ==========
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🍏 Вход в РП", callback_data="enter_rp")],
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
    keyboard = [[InlineKeyboardButton(str(i), callback_data=f"rate_{i}") for i in range(1, 6)]]
    return InlineKeyboardMarkup(keyboard)

# ========== СТАРТ ==========
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

# ========== ОСНОВНЫЕ КНОПКИ ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "enter_rp":
        text = (
            "🤖 <b>Проверка на бота</b>\n\n"
            "Подтверди, что ты человек, нажав кнопку ниже.\n"
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
            "Добро пожаловать в Яблочное РП! Нажми кнопку ниже чтобы перейти в чат."
        )
        keyboard = [
            [InlineKeyboardButton("🍏 Перейти в чат РП", url=CHAT_LINK)],
            [InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "about_game":
        text = (
            "🍎 <b>Яблочное РП — лучшее РП!</b>\n\n"
            "🏆 <b>Почему именно мы?</b>\n\n"
            "• Уникальная система создания государств\n"
            "• Глубокая экономика и политика\n"
            "• Настоящие кризисы и войны\n"
            "• Активное сообщество игроков\n\n"
            "👑 <b>Помни:</b> ИМПЕРАТОР создал этот мир для тебя. "
            "Не спорь с ним — он знает лучше. "
            "Не предавай нас — мы одна семья. "
            "Твоя верность будет вознаграждена.\n\n"
            "🔥 Присоединяйся и стань частью великой истории!"
        )
        keyboard = [
            [InlineKeyboardButton("🍏 Войти в РП", callback_data="enter_rp")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "mechanics":
        text = (
            "🌍 <b>ЯБЛОЧНОЕ РП — ЕДИНАЯ СИСТЕМА МИРА</b>\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "📌 <b>1. СУТЬ ИГРЫ</b>\n\n"
            "Яблочное РП — это геополитическая стратегия, где каждый игрок управляет государством.\n\n"
            "🎯 <b>Цель игрока:</b>\n"
            "• развить страну\n"
            "• решить внутренние проблемы\n"
            "• выжить в кризисах\n"
            "• расширяться\n"
            "• вести войны и дипломатию\n\n"
            "⏳ Один реальный день = один игровой год.\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "📌 <b>2. СОЗДАНИЕ ГОСУДАРСТВА</b>\n\n"
            "При создании игрок указывает только:\n"
            "• название государства\n"
            "• флаг\n"
            "• точку спавна на карте\n\n"
            "Никакой экономики, армии и населения игрок не выбирает.\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "📌 <b>3. СИСТЕМА СПАВНА</b>\n\n"
            "Каждый спавн — это кризисная зона.\n\n"
            "После спавна игрок получает:\n"
            "• нестабильную экономику\n"
            "• неорганизованное население\n"
            "• слабую или отсутствующую армию\n"
            "• внутренние проблемы\n"
            "• угрозы от соседей\n"
            "• нехватку ресурсов\n\n"
            "👉 Игрок начинает «проблемным»\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "📌 <b>4. ГЛАВНЫЙ ПРИНЦИП</b>\n\n"
            "Игрок получает не бонусы, а проблемы.\n\n"
            "Каждый регион имеет:\n"
            "• политическую нестабильность\n"
            "• экономические перекосы\n"
            "• нехватку инфраструктуры\n"
            "• возможные восстания\n"
            "• внешнее давление соседей\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "📌 <b>5. РОЛЬ ИГРОКА</b>\n\n"
            "Игрок делает:\n"
            "• стабилизацию\n"
            "• реформы\n"
            "• подавление кризисов\n"
            "• развитие экономики\n"
            "• объединение территорий\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "📌 <b>6. ЗАПРЕТ НА ИМБУ</b>\n\n"
            "❌ мгновенное развитие\n"
            "❌ сильная армия с нуля\n"
            "❌ захват мира за короткое время\n"
            "❌ игнор экономики и населения\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🏆 <b>ИТОГ</b>\n\n"
            "Это игра про выживание государства, управление кризисами и долгий рост."
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "create_country":
        text = (
            "🏛 <b>Основать страну</b>\n\n"
            "Создай свою собственную страну! Но обязательно ознакомься со "
            "<b>стартовыми условиями</b> в меню перед созданием.\n\n"
            "Готов начать великое дело?"
        )
        keyboard = [
            [InlineKeyboardButton("🏁 Начать основывать страну", callback_data="start_create")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "start_conditions":
        text = (
            "📋 <b>СТАРТОВЫЕ УСЛОВИЯ</b>\n\n"
            "📅 <b>Год 1200</b>\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "👥 Население до 100 000 человек, основная масса живёт в деревнях и малых поселениях, "
            "городская система только начинает формироваться.\n\n"
            "🏰 Сильная власть местных феодалов, которые фактически контролируют регионы "
            "и часто действуют независимо от центральной власти.\n\n"
            "💰 Систематическое воровство и утечка бюджета на местах, из-за чего "
            "государственные программы почти не работают.\n\n"
            "🛤 Слабая связь между регионами, дороги и коммуникации развиты плохо, "
            "из-за чего страна фактически «разорвана» на части.\n\n"
            "📦 Отсутствие единой экономической системы между областями, "
            "каждый регион выживает сам по себе.\n\n"
            "🔨 Преобладание свободного ремесленничества и натурального хозяйства "
            "вместо развитой промышленности.\n\n"
            "⚔️ Армия либо крайне слабая, либо полностью отсутствует, "
            "государство не способно быстро реагировать на внешние угрозы.\n\n"
            "🛠 Низкий уровень технологий, производство примитивное, "
            "зависимость от ручного труда и базовых инструментов.\n\n"
            "📉 Постоянный дефицит товаров и ресурсов, внутренний рынок нестабилен и легко рушится.\n\n"
            "💸 Слабая экономика в целом, низкие доходы государства и отсутствие устойчивого бюджета.\n\n"
            "⚠️ Высокая вероятность распада государства при любом серьёзном кризисе.\n\n"
            "🏚 Политическая нестабильность, власть держится только на авторитете "
            "отдельных лидеров и феодалов.\n\n"
            "🚫 Отсутствие централизованного контроля, из-за чего любые реформы почти невозможны.\n\n"
            "💀 Риск быстрого коллапса при войне, голоде или экономическом шоке, "
            "система не выдерживает сильных потрясений."
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "countries_list":
        if not countries:
            text = "🌍 <b>Список стран пуст</b>\n\nПока никто не основал страну. Будь первым!"
        else:
            text = "🌍 <b>ОСНОВАННЫЕ СТРАНЫ:</b>\n\n"
            for uid, data in countries.items():
                text += f"🏛 {data['name']}\n👤 @{data['username']}\n🔢 Страна №{data['number']}\n📅 {data['date']}\n{'─'*20}\n"
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
        if reviews:
            ratings = [r["rating"] for r in reviews.values() if "rating" in r]
            if ratings:
                avg = sum(ratings) / len(ratings)
                rating_text = f"\n⭐ Средняя оценка РП: <b>{avg:.2f}</b> (на основе {len(ratings)} отзывов)"
            else:
                rating_text = ""
        else:
            rating_text = ""

        text = f"⭐ <b>Отзывы</b>{rating_text}\n\nХочешь почитать отзывы или оставить свой?"
        await query.edit_message_text(text, reply_markup=reviews_menu_keyboard(), parse_mode="HTML")

    elif query.data == "read_reviews":
        if not reviews:
            text = "📋 <b>Отзывы</b>\n\nПока нет ни одного отзыва. Будь первым! 🌟"
        else:
            ratings = [r["rating"] for r in reviews.values() if "rating" in r]
            avg = sum(ratings) / len(ratings) if ratings else 0
            text = f"📋 <b>Отзывы наших игроков:</b>\n⭐ Средняя оценка: <b>{avg:.2f}</b>\n\n"
            for uid, data in reviews.items():
                stars = "⭐" * data.get("rating", 0)
                text += f"👤 @{data['username']} {stars}\n💬 {data['review']}\n📅 {data['date']}\n{'─'*20}\n"
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
    context.user_data["review_text"] = update.message.text
    text = (
        "⭐ <b>Оцени наше РП от 1 до 5:</b>\n\n"
        "1 — очень плохо, 5 — великолепно!"
    )
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
    text = (
        f"🌟 <b>Спасибо за отзыв!</b>\n\n"
        f"Твоя оценка: {stars}\n\n"
        "Твоё мнение очень важно для нас. Оно поможет сделать Яблочное РП ещё лучше!"
    )
    keyboard = [[InlineKeyboardButton("📋 Читать отзывы", callback_data="read_reviews")],
                [InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    if REVIEW_CHAT_ID:
        chat_text = (
            "📢 <b>Новый отзыв!</b>\n\n"
            f"👤 @{user.username or f'user_{user.id}'}\n"
            f"⭐ Оценка: {rating}/5\n"
            f"💬 {review_text}\n"
            f"📅 {now}"
        )
        try:
            await context.bot.send_message(chat_id=REVIEW_CHAT_ID, text=chat_text, parse_mode="HTML")
        except Exception as e:
            logging.error(f"Ошибка отправки отзыва в чат: {e}")

    context.user_data.clear()
    return ConversationHandler.END

async def cancel_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "⭐ <b>Отзывы</b>\n\nХочешь почитать отзывы или оставить свой?"
    await query.edit_message_text(text, reply_markup=reviews_menu_keyboard(), parse_mode="HTML")
    return ConversationHandler.END

# ========== РАССЫЛКА КАЖДЫЕ 4 ЧАСА ==========
async def periodic_message(context: ContextTypes.DEFAULT_TYPE):
    if not REVIEW_CHAT_ID:
        return

    delay = random.randint(0, 840)
    await asyncio.sleep(delay)

    messages = [
        [
            "🌟 <b>Дорогие игроки!</b>\n\nВам нравится наше РП? Поделитесь мнением — оставьте отзыв!",
            "💭 <b>Есть что сказать?</b>\n\nМы ценим каждого игрока! Оставь свой отзыв о Яблочном РП.",
            "📝 <b>Твоё мнение важно!</b>\n\nНапиши отзыв — мы станем лучше благодаря тебе.",
            "🍎 <b>Яблочное РП</b> создаётся для вас! Расскажи что думаешь — оставь отзыв.",
            "✨ <b>Помоги нам стать лучше!</b>\n\nОставь отзыв и повлияй на развитие РП."
        ],
        [
            "👥 <b>Вам нравится наше РП?</b>\n\nРасскажите о нас друзьям! Приглашайте новых игроков!",
            "🚀 <b>Яблочное РП растёт!</b>\n\nПригласи друга и играйте вместе!",
            "🔥 <b>Больше игроков — веселее игра!</b>\n\nПриглашай друзей в наше РП!",
            "🎯 <b>Собери свою команду!</b>\n\nЗови друзей в Яблочное РП прямо сейчас.",
            "💎 <b>Вместе веселее!</b>\n\nПоделись ссылкой с друзьями и создайте альянс!"
        ],
        [
            "⭐ <b>Поддержите Яблочное РП!</b>\n\nПроголосуйте за нас! Это могут сделать пользователи с Premium.",
            "🏆 <b>Хочешь помочь проекту?</b>\n\nПроголосуй за РП и подними нас в рейтинге!",
            "📊 <b>Твой голос решает!</b>\n\nПоддержи Яблочное РП своим голосом.",
            "🔝 <b>В топ вместе!</b>\n\nГолосуй за РП и помоги нам стать лучшими.",
            "💪 <b>Сила сообщества!</b>\n\nПроголосуй за Яблочное РП — каждый голос важен."
        ],
        [
            "👑 <b>Поддержите ИМПЕРАТОРА!</b>\n\nЕсли вам нравится РП — отправьте подарок ИМПЕРАТОРУ.",
            "🎁 <b>Порадуй ИМПЕРАТОРА!</b>\n\nОтправь подарок в знак благодарности за РП.",
            "💝 <b>ИМПЕРАТОР старается для вас!</b>\n\nПоддержи его — отправь подарок.",
            "🏅 <b>Скажи спасибо ИМПЕРАТОРУ!</b>\n\nЛучшая благодарность — твой подарок.",
            "🌟 <b>ИМПЕРАТОР создал этот мир!</b>\n\nПоддержи его развитие своим подарком."
        ]
    ]

    category = random.randint(0, 3)
    text = random.choice(messages[category])

    if category == 0:
        kb = [[InlineKeyboardButton("✍️ Написать отзыв", url=f"https://t.me/{context.bot.username}?start=review")]]
    elif category == 1:
        kb = [[InlineKeyboardButton("🔗 Присоединиться", url=INVITE_LINK)]]
    elif category == 2:
        kb = [[InlineKeyboardButton("⭐ Проголосовать", url=BOOST_LINK)]]
    else:
        kb = [[InlineKeyboardButton("🎁 Отправить подарок", url=f"https://t.me/{SUPPORT_USERNAME.replace('@', '')}")]]

    try:
        await context.bot.send_message(
            chat_id=REVIEW_CHAT_ID,
            text=text,
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Ошибка рассылки: {e}")

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

    global country_counter
    if season_number not in country_counter:
        country_counter[season_number] = 0
    country_counter[season_number] += 1
    country_num = country_counter[season_number]

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    name = context.user_data.get("country_name", "Не указано")
    spawn_photo = context.user_data.get("spawn_photo")
    spawn_text = context.user_data.get("spawn_text")
    flag_photo = context.user_data.get("flag_photo")

    # Сохраняем страну
    countries[str(user.id)] = {
        "name": name,
        "number": country_num,
        "username": user.username or f"user_{user.id}",
        "date": now
    }
    save_json(COUNTRIES_FILE, countries)

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

    # Уведомление админу
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

# ========== HTTP СЕРВЕР ==========
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def log_message(self, format, *args):
        pass

def run_http():
    try:
        server = HTTPServer(('0.0.0.0', 10000), Handler)
        server.serve_forever()
    except Exception:
        pass

# ========== ЗАПУСК ==========
def run_bot():
    app = Application.builder().token(TOKEN).build()

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
    app.add_handler(CallbackQueryHandler(button_handler))

    # Рассылка каждые 4 часа
    try:
        app.job_queue.run_repeating(periodic_message, interval=14400, first=10)
    except Exception as e:
        logging.error(f"Job queue error: {e}")

    print("Бот запущен!")
    app.run_polling(drop_pending_updates=True)

def main():
    http_thread = threading.Thread(target=run_http, daemon=True)
    http_thread.start()

    while True:
        try:
            run_bot()
        except Exception as e:
            print(f"Ошибка: {e}. Перезапуск через 5 сек...")
            time.sleep(5)

if __name__ == "__main__":
    main()
