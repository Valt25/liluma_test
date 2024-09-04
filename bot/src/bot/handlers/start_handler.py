from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.db.connection import wrap_with_db_connection
from bot.handlers.utils import build_start_inline_keyboard
from bot.services.companies import get_companies
from bot import texts


@wrap_with_db_connection
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    companies = await get_companies()
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=texts.MESSAGE_WITH_COMPANY_LIST_TEXT,
        reply_markup=build_start_inline_keyboard(companies)
    )
