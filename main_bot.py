from telethon import TelegramClient, events
from config import DB, API_ID, API_HASH, BOT_TOKEN
import random

bot = TelegramClient("main_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# استقبال أسئلة المتربصين
@bot.on(events.NewMessage(pattern=r"\?$"))
async def handle_question(event):
    user = await event.get_sender()
    question = event.text.strip()

    cur = DB.cursor()
    cur.execute("SELECT id, channel_id FROM assistants ORDER BY random() LIMIT 1")
    assistant = cur.fetchone()

    if not assistant:
        await event.reply("⚠️ لا يوجد مساعدون متصلون حالياً.")
        return

    assistant_id, channel_id = assistant
    cur.execute("INSERT INTO questions (user_id, assistant_id, question, status) VALUES (%s, %s, %s, 'pending')",
                (user.id, assistant_id, question))
    DB.commit()
    cur.close()

    await bot.send_message(channel_id, f"🟢 سؤال جديد من @{user.username or user.first_name}:\n\n{question}")
    await event.reply("✅ تم إرسال سؤالك إلى المساعد.")

# استقبال تقييم المتربص
@bot.on(events.NewMessage(pattern=r"^/rate\s+(\d+)$"))
async def rate_handler(event):
    rating = int(event.pattern_match.group(1))
    user = await event.get_sender()

    cur = DB.cursor()
    cur.execute("""
        SELECT q.id, a.id FROM questions q
        JOIN assistants a ON q.assistant_id = a.id
        WHERE q.user_id=%s AND q.status='answered' AND q.rating IS NULL
        ORDER BY q.id DESC LIMIT 1
    """, (user.id,))
    record = cur.fetchone()

    if not record:
        await event.reply("⚠️ لا يوجد رد لتقييمه.")
        return

    qid, assistant_id = record
    cur.execute("UPDATE questions SET rating=%s WHERE id=%s", (rating, qid))

    cur.execute("SELECT rating, answers FROM assistants WHERE id=%s", (assistant_id,))
    old_rating, answers = cur.fetchone() or (0, 0)
    new_rating = (old_rating * answers + rating) / (answers + 1)
    cur.execute("UPDATE assistants SET rating=%s, answers=answers+1 WHERE id=%s", (new_rating, assistant_id))
    DB.commit()
    cur.close()

    await event.reply(f"⭐ شكراً لتقييمك! ({rating}/5)")

with bot:
    print("🎯 Main bot running...")
    bot.run_until_disconnected()
