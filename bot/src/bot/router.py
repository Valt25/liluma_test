from telegram.ext._application import Application 
from telegram.ext import CommandHandler, CallbackQueryHandler

from bot.handlers.company_option_selected import company_option_selected
from bot.handlers.company_selected_handler import company_selected_handler
from bot.handlers.start_handler import start_handler
from bot.handlers.to_start_handler import to_start_handler



def setup_routes(application: Application) -> None:
    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(CallbackQueryHandler(company_selected_handler, pattern="^company_selection:.*$"))
    application.add_handler(CallbackQueryHandler(company_option_selected, pattern="^company_option_selection:.*:.*$"))
    application.add_handler(CallbackQueryHandler(to_start_handler, pattern="^to_start$"))

