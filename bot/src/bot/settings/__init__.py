from bot.settings.utils import get_setting


TOKEN = get_setting("TOKEN", required=True)

DB_USER = get_setting("DB_USER", required=True)
DB_PASSWORD = get_setting("DB_PASSWORD", required=True)
DB_HOST = get_setting("DB_HOST", required=True)
DB_PORT = get_setting("DB_PORT", required=True)
DB_NAME = get_setting("DB_NAME", required=True)

SPREADSHEET_ID = get_setting("SAMPLE_SPREADSHEET_ID", default="1w5MAeMSZZJ6_3_s2res3hJPcw2NJxNIaFV4lV0j7ePI")
GOOGLE_API_KEY = get_setting("GOOGLE_API_KEY", required=True)