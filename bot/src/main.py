from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes

from bot.router import setup_routes
from bot import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.TOKEN).build()
    
    setup_routes(application)
    
    application.run_polling()