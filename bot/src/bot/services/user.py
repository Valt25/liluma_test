from ast import Str
from bot.common.enums import CompanyOptions
from bot.db.connection import ConnectionCache
from bot.services.companies import Company


async def update_latest_message_id(user_id: int, message_id: int):
    conn = ConnectionCache.get_connection()

    await conn.execute(
	    f'''INSERT INTO chats (user_id, graphic_message_id) VALUES ($1, $2) 
	    	ON CONFLICT(user_id) DO UPDATE SET graphic_message_id=EXCLUDED.graphic_message_id;''',
	    str(user_id),
	    str(message_id),
	)

async def update_latest_message(user_id: int, message_id: int, company_name: str, company_option: CompanyOptions):
    conn = ConnectionCache.get_connection()
    res = await conn.fetchrow("SELECT * FROM companies WHERE title=$1", company_name)
    await conn.execute(
	    f'''INSERT INTO chats (user_id, graphic_message_id, selected_company_id, selected_company_option) VALUES ($1, $2, $3, $4) 
	    	ON CONFLICT(user_id) DO UPDATE SET graphic_message_id=EXCLUDED.graphic_message_id, selected_company_id=EXCLUDED.selected_company_id, selected_company_option=EXCLUDED.selected_company_option;''',
	    str(user_id),
	    str(message_id),
        res['sheet_id'],
        company_option.value
	)

async def get_latest_message_id(user_id):
    conn = ConnectionCache.get_connection()
    res = await conn.fetchrow(
        '''SELECT * FROM chats WHERE user_id=$1''',
        str(user_id)
    )
    if res is None:
        return None
    return int(res['graphic_message_id'])

async def set_last_message_to_null(user_id):
    conn = ConnectionCache.get_connection()
    await conn.execute("UPDATE chats SET graphic_message_id=NULL, selected_company_id=NULL,selected_company_option=NULL WHERE user_id=user_id")