from telegram import Update

from bot.db.connection import wrap_with_db_connection
from bot.handlers.utils import build_start_inline_keyboard
from bot.services.companies import get_companies
from bot import texts


@wrap_with_db_connection
async def to_start_handler(update: Update, _):
    query = update.callback_query
    companies = await get_companies()
    
    await query.answer()

    await query.edit_message_text(
        text=texts.MESSAGE_WITH_COMPANY_LIST_TEXT,
        reply_markup=build_start_inline_keyboard(companies)
    )