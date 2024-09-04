import asyncio
from typing import Set

from telegram import Bot

from bot import settings, texts
from bot.common.enums import CompanyOptions
from bot.db.connection import ConnectionCache
from bot.services.companies import get_company_data
from bot.services.plot import get_plot
from bot.services.user import get_latest_message_id, set_last_message_to_null, update_latest_message_id


async def delete_messages_with_stale_companies(sheet_ids: Set[str]):
    if len(sheet_ids) > 0:
        sheet_ids = [f"'{val}'" for val in sheet_ids]
        conn = ConnectionCache.get_connection()
        res = await conn.fetch(f'''SELECT user_id, graphic_message_id FROM chats WHERE selected_company_id IN ({','.join(sheet_ids)});''')
        async with Bot(settings.TOKEN) as bot:
            await asyncio.gather(*[bot.delete_message(int(r['user_id']), int(r['graphic_message_id'])) for r in res])
        await conn.execute(f'''UPDATE chats SET graphic_message_id=NULL, selected_company_id=NULL WHERE selected_company_id IN ({','.join(sheet_ids)});''')


async def update_message_with_latest_data(company_name, company_option, bot, chat_id):
    company_data = await get_company_data(company_name, company_option)
    in_memory_media =  await get_plot(company_data, company_name, company_option)
    return await bot.send_photo(
            chat_id=chat_id,
            photo=in_memory_media,
            caption=texts.COMPANY_DATA_PRESENTATION_TEXT,
    )


async def update_all_presented_graphics():
    conn = ConnectionCache.get_connection()
    res = await conn.fetch('''SELECT user_id, graphic_message_id, selected_company_option, title FROM chats JOIN companies ON chats.selected_company_id=companies.sheet_id WHERE graphic_message_id IS NOT NULL AND selected_company_option IS NOT NULL;''')
    await_list = []

    async with Bot(settings.TOKEN) as bot:
        for r in res:
            company_data = await get_company_data(r['title'], CompanyOptions(r['selected_company_option']))
            in_memory_media =  await get_plot(company_data, r['title'], CompanyOptions(r['selected_company_option']))
            try:
                await bot.delete_message(
                    chat_id=r['user_id'],
                    message_id=r['graphic_message_id'],
                )
            except:
                await set_last_message_to_null(r['user_id'])
            await_list.append(asyncio.create_task(bot.send_photo(
                chat_id=r['user_id'],
                photo=in_memory_media,
                caption=texts.COMPANY_DATA_PRESENTATION_TEXT,
            )))
            
        new_messages = await asyncio.gather(*await_list)
        for new_message in new_messages:
            await update_latest_message_id(new_message.from_user.id, new_message.message_id)