from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "ТВОЙ_ТОКЕН_СЮДА"

RP_LINK = "https://t.me/popa0193"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
keyboard = [
[InlineKeyboardButton("🚪 Войти в RP", callback_data="check_human")],
[InlineKeyboardButton("📝 Регистрация", callback_data="register")],
[InlineKeyboardButton("📜 Правила", callback_data="rules")],
[InlineKeyboardButton("📖 Описание мира", callback_data="world")],
[InlineKeyboardButton("🏆 Сезоны", callback_data="seasons")]
]

text = (
    "🍏 Добро пожаловать в Яблочное RP!\n\n"
    "Мир только готовится к открытию.\n"
    "Собирайте информацию, следите за новостями и готовьтесь к старту первого сезона.\n\n"
    "Выберите нужный раздел ниже."
)

await update.message.reply_text(
    text,
    reply_markup=InlineKeyboardMarkup(keyboard)
)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

if query.data == "check_human":
    keyboard = [
        [InlineKeyboardButton("✅ Я человек", callback_data="human_ok")]
    ]

    await query.message.reply_text(
        "Проверка перед входом.\n\nНажмите кнопку ниже.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

elif query.data == "human_ok":
    keyboard = [
        [InlineKeyboardButton("🚪 Перейти в RP", url=RP_LINK)]
    ]

    await query.message.reply_text(
        "Проверка пройдена.\n\nТеперь можете войти в RP.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

elif query.data == "register":
    await query.message.reply_text(
        "📝 Регистрация временно недоступна.\n\nПервый сезон ещё не начался."
    )

elif query.data == "rules":
    await query.message.reply_text(
        "📜 Правила пока находятся в разработке."
    )

elif query.data == "world":
    await query.message.reply_text(
        "📖 Описание мира скоро появится."
    )

elif query.data == "seasons":
    await query.message.reply_text(
        "🏆 Первый сезон ещё не начался."
    )

def main():
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Бот запущен")
app.run_polling()

if name == "main":
main()
