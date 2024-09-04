from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from bot.common.enums import CompanyOptions
from bot import texts


def _build_keyboard(company_name: str) -> List[InlineKeyboardMarkup]:
    return InlineKeyboardMarkup([
        *[[InlineKeyboardButton(texts.COMPANY_OPTION_ENUM_TO_TEXT[option], callback_data=f"company_option_selection:{option.value}:{company_name}")] for option in CompanyOptions],
        [InlineKeyboardButton(texts.BACK_BUTTON_TEXT, callback_data='to_start')]
    ])


async def company_selected_handler(update: Update, _):
    query = update.callback_query
    print(f"{query=}")
    data = query.data
    company_name = data.split(":", 1)[-1]
    await query.answer()

    await query.edit_message_text(text=texts.MESSAGE_WITH_COMPANY_OPTIONS_TEXT, reply_markup=_build_keyboard(company_name))
