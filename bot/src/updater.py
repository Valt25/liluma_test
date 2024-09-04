import asyncio
from telegram import Bot
import gspread
from bot import settings
from bot.db.connection import wrap_with_db_connection
from bot.services.bot import delete_messages_with_stale_companies, update_all_presented_graphics
from bot.services.companies import delete_companies_by_sheet_ids, get_companies, update_companies, update_data

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

gc = gspread.api_key(settings.GOOGLE_API_KEY)
sh = gc.open_by_key(settings.SPREADSHEET_ID)

@wrap_with_db_connection
async def get_updates():
	sheets = sh.worksheets()
	companies = []
	companies_data = {}
	for sheet in sheets:
		company_name = sheet.title
		sheet_id = str(sheet.id)
		companies.append((company_name, sheet_id))
		row_count = sheet.row_count
		data = sheet.get(f"A2:E{row_count}")
		companies_data[sheet_id] = data
	
	current_companies = await get_companies()
	sheet_ids_to_delete = set(c.sheet_id for c in current_companies) - set(c[1] for c in companies)
	await delete_messages_with_stale_companies(sheet_ids_to_delete)
	await delete_companies_by_sheet_ids(sheet_ids_to_delete)
	await update_companies(companies)
	await update_data(companies_data)
	await update_all_presented_graphics()

async def main():
	while True:
		async with Bot(settings.TOKEN) as bot:
			await get_updates()
			await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())