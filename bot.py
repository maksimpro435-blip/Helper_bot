telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update из telegram.ext import Application, CommandHandler, CallbackQueryHandler, contextTypes
RP_LINK = "https://t.me/popa0193�"
start def async(update: Update, context: ContextTypes.DEFAULT_TYPE): keyboard = [ [InlineKeyboardButton("🚪 Войти в RP", callback_data="join")], [InlineKeyboardButton("📜 Правила", callback_data="rules")], [InlineKeyboardButton("📖 Описание мира", callback_data="world")], [InlineKeyboardButton("🏆 Сезоны", callback_data="seasons")] ]
ожидание обновления.сообщение.текст ответа(
    "👋 Добро пожаловать в наше RP!\n\nВыберите нужный раздел:",
    InlineKeyboardMarkup=reply_markup(клавиатура)
)
button def async(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer()
query if.data == "join":
    query await.message.reply_text(f"🚪 Ссылка на RP:\n{RP_LINK}")

query elif.data == "rules":
    query await.message.reply_text("📜 Правила пока находятся в разработке.")

query elif.data == "world":
    query await.message.reply_text("📖 Описание мира скоро появится.")

query elif.data == "seasons":
    query await.message.reply_text("🏆 Первый сезон ещё не начался.")
main def(): app = Application.builder().токен(8721151214:AAEQFF012KV1ZViqxoiLp523XRV4ZhyG2Bs).build()
app.add_handler(CommandHandler("пуск", начать))
app.add_handler(CallbackQueryHandler(кнопка))

приложение.run_polling()
"main" == имя if: main() :::
