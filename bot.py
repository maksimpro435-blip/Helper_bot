from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "ТУТ_ТВОЙ_ТОКЕН"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚪 Войти в RP", url="https://t.me/popa0193")],
        [InlineKeyboardButton("📜 Правила", callback_data="rules")],
        [InlineKeyboardButton("📖 Описание мира", callback_data="world")],
        [InlineKeyboardButton("🏆 Сезоны", callback_data="seasons")]
    ]

    await update.message.reply_text(
        "👋 Добро пожаловать в наше RP!\n\nВыберите нужный раздел:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "rules":
        await query.message.reply_text("📜 Правила пока находятся в разработке.")

    elif query.data == "world":
        await query.message.reply_text("📖 Описание мира скоро появится.")

    elif query.data == "seasons":
        await query.message.reply_text("🏆 Первый сезон ещё не начался.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
