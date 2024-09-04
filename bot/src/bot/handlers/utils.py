from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.services.companies import Company


def build_start_inline_keyboard(companies: List[Company]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(company.title, callback_data=f"company_selection:{company.title}")] for company in companies
    ])