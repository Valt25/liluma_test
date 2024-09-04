import asyncio
from io import BytesIO
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputFile, InputMedia, Update
from telegram.constants import InputMediaType
from telegram.ext import ContextTypes

from bot.common.enums import CompanyOptions
from bot.db.connection import wrap_with_db_connection
from bot.services.companies import get_company_data
from bot.services.plot import get_plot
from bot import texts
from bot.services.user import get_latest_message_id, set_last_message_to_null, update_latest_message
    

async def conditional_delete_message(bot, chat_id):
    last_message_id = await get_latest_message_id(chat_id)
    if last_message_id is not None:
        await bot.delete_message(chat_id, last_message_id)

@wrap_with_db_connection
async def company_option_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data # type: ignore
    _, option_selected, company_name = data.split(":", 2) # type: ignore
    option_selected = CompanyOptions(option_selected)
    company_data = await get_company_data(company_name, option_selected)
    last_message_id = await get_latest_message_id(update.effective_chat.id)
    print(f"{last_message_id=}")
    in_memory_media =  await get_plot(company_data, company_name, option_selected)
    await_list = []
    await_list.append(context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=in_memory_media,
            caption=texts.COMPANY_DATA_PRESENTATION_TEXT,
    ))
    if last_message_id is not None:
        try:
            await context.bot.delete_message(update.effective_chat.id, last_message_id)
        except:
            await set_last_message_to_null(r['user_id'])
    await_list.append(query.answer())
    res = await asyncio.gather(*await_list)
    await update_latest_message(update.effective_chat.id, res[0].message_id, company_name, option_selected)
