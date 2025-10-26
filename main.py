from telethon import TelegramClient, events, Button
from config import API_ID, API_HASH, BOT_TOKEN, LEVEL1_LINK
from sheets import (
    add_to_portail,
    add_to_membres,
    update_activity,
    get_all_portail,
    mark_as_notified,
    get_template
)
import asyncio

# ------------------------------
# ⚙️ إعداد البوت
# ------------------------------
bot = TelegramClient("Expert_X", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user_state = {}

# ------------------------------
# 📸 رسالة الترحيب + اختيار اللغة
# ------------------------------
@bot.on(events.NewMessage(incoming=True))
async def auto_welcome(event):
    sender_id = event.sender_id

    # المستخدم أول مرة فقط
    if sender_id not in user_state:
        user_state[sender_id] = {"step": "lang_select"}

        welcome_image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiD6ImSjQAFVJr3B6sagk6aHOzlx7e9pzgdw&s"  # 🔗 ضع رابط الصورة هنا

        await bot.send_file(
            sender_id,
            file=welcome_image,
            caption=(
                        "👋 **مرحبا بيك في MMG!** 💪\n\n"
                        "أنا هو **Expert X**، راح نكون معاك خطوة بخطوة باش تتعلم وتخدم مشروعك في التجارة الإلكترونية 🛍️💻\n"
                        "🔥 حضّر روحك للتحدي والنجاح!\n\n"
                        "🌍 اختار اللغة اللي تحب تكمل بيها 👇"

            ),
            buttons=[
                [
                    Button.inline("🇩🇿 العربية", b"lang_ar"),
                    Button.inline("🇫🇷 Français", b"lang_fr"),
                    Button.inline("🇬🇧 English", b"lang_en"),
                ]
            ],
        )
        return

    # تجاهل أي رسالة أثناء اختيار اللغة
    if user_state[sender_id].get("step") == "lang_select":
        return


# ------------------------------
# 🌐 اختيار اللغة
# ------------------------------
@bot.on(events.CallbackQuery(pattern=b"lang_"))
async def set_language(event):
    sender_id = event.sender_id
    lang_code = event.data.decode().split("_")[1].capitalize()  # Ar / Fr / En

    user_state[sender_id] = {"lang": lang_code, "step": "start"}
    welcome_message = get_template("welcome", lang_code)

    await event.answer()
    await event.edit(
        welcome_message,
        buttons=[[Button.inline("📝 تسجيل / Register / Inscription", b"start_registration")]],
    )


# ------------------------------
# 🧾 بدء التسجيل
# ------------------------------
@bot.on(events.CallbackQuery(data=b"start_registration"))
async def start_registration(event):
    sender_id = event.sender_id
    lang = user_state.get(sender_id, {}).get("lang", "Ar")

    user_state[sender_id]["step"] = "nom"
    await event.answer()
    await event.edit(get_template("ask_name", lang))


# ------------------------------
# ✏️ معالجة خطوات التسجيل
# ------------------------------
@bot.on(events.NewMessage)
async def main_handler(event):
    sender_id = event.sender_id
    if sender_id not in user_state:
        # تحديث النشاط لأي رسالة عادية
        if event.is_private or event.is_group:
            sender = await event.get_sender()
            update_activity(sender.id, "Niveau 1", live=False)
        return

    state = user_state[sender_id]
    step = state.get("step")
    lang = state.get("lang", "Ar")
    text = event.text.strip()

    # اختيار اللغة فقط
    if step == "lang_select":
        return

    # خطوات التسجيل
    if step == "nom":
        state["nom"] = text
        state["step"] = "prenom"
        await event.respond(get_template("ask_prenom", lang))

    elif step == "prenom":
        state["prenom"] = text
        state["step"] = "numero"
        await event.respond(get_template("ask_numero", lang))

    elif step == "numero":
        state["numero"] = text
        username = f"https://t.me/{event.sender.username}" if event.sender.username else "—"

        # حفظ البيانات في Google Sheets
        add_to_portail(
            user_id=sender_id,
            nom=state["nom"],
            prenom=state["prenom"],
            numero=state["numero"],
            username=username,
        )

        await event.respond(get_template("waiting_validation", lang))
        del user_state[sender_id]


# ------------------------------
# 🔄 التحقق الدوري من القبول
# ------------------------------
async def check_inscription_loop():
    await bot.connect()
    print("🕒 التحقق من الحالات كل 1 دقائق...")

    while True:
        all_users = get_all_portail()
        accepted_today = 0

        for user in all_users:
            statut = user.get("Statut", "").strip()
            notified = user.get("notified", "").strip()

            # ✅ تحقق من الشرطين: لم يتم الإشعار + مقبول
            if not notified and statut == "Inscrit":
                try:
                    add_to_membres(user["ID"], user["Nom"], user["Prénom"], user["Lien"],user["Numero"])
                    await bot.send_message(
                        user["ID"],
                        f"🎉 مرحبًا {user['Prénom']} {user['Nom']}!\n"
                        f"✅ تم قبولك في الدورة.\n\n"
                        f"اضغط أدناه للانتقال إلى المستوى 1 👇",
                        buttons=[[Button.url("🎓 Niveau 1", LEVEL1_LINK)]]
                    )
                    mark_as_notified(user["ID"])
                    accepted_today += 1
                    print(f"✅ إشعار أُرسل إلى {user['Nom']} {user['Prénom']}")
                except Exception as e:
                    print(f"⚠️ خطأ أثناء إرسال الإشعار إلى {user['ID']}: {e}")

        print(f"📊 عدد المقبولين الذين تم إشعارهم: {accepted_today}")
        await asyncio.sleep(30)  # تحقق كل 3 دقائق


# ------------------------------
# 🚀 تشغيل البوت
# ------------------------------
bot.loop.create_task(check_inscription_loop())
print("🚀 Expert_X bot (MMG) est en ligne... 💎")
bot.run_until_disconnected()
