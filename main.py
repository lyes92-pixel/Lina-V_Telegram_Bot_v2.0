from telethon import TelegramClient
from Sheets.config import API_ID, API_HASH, BOT_TOKEN
from bot.welcome import register_welcome_handlers
from bot.registration import register_registration_handlers
from bot.loops import start_check_loop
from bot.group_tracking import register_group_tracking
from bot.utils import user_state

import asyncio

# ⚙️ إنشاء العميل
bot = TelegramClient("Expert_X", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 🔗 تسجيل الأحداث
register_welcome_handlers(bot, user_state)
register_registration_handlers(bot, user_state)
register_group_tracking(bot)
bot.loop.create_task(start_check_loop(bot))

print("🚀 Expert_X bot (MMG) est en ligne... 💎")
bot.run_until_disconnected()
