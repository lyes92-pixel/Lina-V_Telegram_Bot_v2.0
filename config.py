# config.py
import psycopg2

# إعدادات قاعدة البيانات من Railway
DB = psycopg2.connect(
    host="containers-us-west-56.railway.app",
    port="7460",
    database="railway",
    user="postgres",
    password="yourpassword"
)

# إعدادات API Telegram
API_ID = 1234567
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
ADMIN_ID = 987654321
