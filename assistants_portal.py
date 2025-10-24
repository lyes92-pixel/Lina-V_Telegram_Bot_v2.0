from telethon import TelegramClient, events, types
from telethon.tl.functions.channels import CreateChannelRequest, EditAdminRequest
from config import DB, API_ID, API_HASH, BOT_TOKEN

bot = TelegramClient("assist_portal", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    user = await event.get_sender()
    cur = DB.cursor()
    cur.execute("SELECT channel_id FROM assistants WHERE user_id=%s", (user.id,))
    row = cur.fetchone()

    if row:
        await event.respond("✅ لديك بالفعل قناة خاصة.")
        return

    result = await bot(CreateChannelRequest(
        title=f"🎯 لوحة {user.first_name}",
        about="قناة خاصة بالمساعد.",
        megagroup=False
    ))
    channel = result.chats[0]
    await bot(EditAdminRequest(
        channel=channel,
        user_id=user.id,
        admin_rights=types.ChatAdminRights(post_messages=True),
        rank="Assistant"
    ))

    cur.execute("INSERT INTO assistants (user_id, username, channel_id) VALUES (%s, %s, %s)",
                (user.id, user.username or "بدون_اسم", channel.id))
    DB.commit()
    cur.close()
    await event.respond("🚀 تم إنشاء قناتك الخاصة!")

# استقبال الإجابات من القناة الخاصة
@bot.on(events.NewMessage())
async def handle_answer(event):
    chat = await event.get_chat()
    cur = DB.cursor()
    cur.execute("SELECT id FROM assistants WHERE channel_id=%s", (chat.id,))
    assistant = cur.fetchone()
    if not assistant:
        return

    assistant_id = assistant[0]
    text = event.text.strip()

    cur.execute("""
        SELECT id, user_id FROM questions
        WHERE assistant_id=%s AND status='pending'
        ORDER BY id ASC LIMIT 1
    """, (assistant_id,))
    q = cur.fetchone()

    if not q:
        return

    qid, user_id = q
    cur.execute("UPDATE questions SET answer=%s, status='answered' WHERE id=%s", (text, qid))
    DB.commit()
    cur.close()

    await bot.send_message(user_id, f"💬 المساعد أجاب:\n\n{text}\n\n🌟 قيّم الإجابة بالأمر:\n`/rate 1` إلى `/rate 5`")

    await event.respond("✅ تم إرسال الإجابة للمتربص.")

with bot:
    print("🤖 Assistants Portal running...")
    bot.run_until_disconnected()
