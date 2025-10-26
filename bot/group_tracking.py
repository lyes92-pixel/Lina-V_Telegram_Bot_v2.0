from telethon import events
from Sheets.membres import log_first_entry

def register_group_tracking(bot):

    @bot.on(events.ChatAction)
    async def handle_group_entry(event):
        if event.user_joined or event.user_added:
            user = await event.get_user()
            chat = await event.get_chat()
            try:
                log_first_entry(user.id, chat.title)
                print(f"🕒 تم تسجيل دخول {user.first_name} إلى {chat.title}")
            except Exception as e:
                print(f"⚠️ خطأ أثناء تسجيل دخول {user.id}: {e}")
