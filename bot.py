from telethon import TelegramClient, events
from config import API_ID, API_HASH, BOT_TOKEN
from sheets import get_template, add_or_update_user, update_activity

bot = TelegramClient("Expert_X", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 📥 عند دخول عضو جديد
@bot.on(events.ChatAction)
async def new_member(event):
    if event.user_joined or event.user_added:
        user = await event.get_user()
        group_name = event.chat.title

        nom = user.first_name or ""
        prenom = user.last_name or ""
        username = f"https://t.me/{user.username}" if user.username else "—"

        add_or_update_user(user.id, nom, prenom, username, group_name)

        welcome_msg = get_template("welcome")
        try:
            await bot.send_message(user.id, welcome_msg)
        except:
            await event.reply("⚠️ Impossible d’envoyer le message privé (DM fermé).")

# 💬 عند إرسال رسالة في مجموعة
@bot.on(events.NewMessage)
async def on_message(event):
    if event.is_group:
        sender = await event.get_sender()
        group_name = event.chat.title
        update_activity(sender.id, group_name)

print("🚀 Expert_X bot (MMG) is running... 💎")
bot.run_until_disconnected()
