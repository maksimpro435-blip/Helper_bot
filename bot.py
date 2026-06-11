:::writing{variant="document" id="52841"} from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
RP_LINK = "https://t.me/popa0193⁠�"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): keyboard = [ [InlineKeyboardButton("🚪 Войти в RP", callback_data="join")], [InlineKeyboardButton("📜 Правила", callback_data="rules")], [InlineKeyboardButton("📖 Описание мира", callback_data="world")], [InlineKeyboardButton("🏆 Сезоны", callback_data="seasons")] ]
await update.message.reply_text(
    "👋 Добро пожаловать в наше RP!\n\nВыберите нужный раздел:",
    reply_markup=InlineKeyboardMarkup(keyboard)
)
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer()
if query.data == "join":
    await query.message.reply_text(f"🚪 Ссылка на RP:\n{RP_LINK}")

elif query.data == "rules":
    await query.message.reply_text("📜 Правила пока находятся в разработке.")

elif query.data == "world":
    await query.message.reply_text("📖 Описание мира скоро появится.")

elif query.data == "seasons":
    await query.message.reply_text("🏆 Первый сезон ещё не начался.")
def main(): app = Application.builder().token(8721151214:AAEQFF012KV1ZViqxoiLp523XRV4ZhyG2Bs).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
if name == "main": main() :::
