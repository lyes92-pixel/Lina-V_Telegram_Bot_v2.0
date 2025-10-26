import asyncio
from collections import Counter
from telethon import Button
from Sheets.portail import get_all_portail, mark_as_notified
from Sheets.membres import add_to_membres, update_member_activity
from Sheets.config import LEVEL1_LINK

# --------------------------------------------------------
# دالة إرسال الإشعار للمقبولين الجدد
# --------------------------------------------------------
async def check_new_users(bot):
    all_users = get_all_portail()
    accepted_today = 0

    for user in all_users:
        statut = user.get("Statut", "").strip()
        notified = user.get("notified", "").strip()

        if not notified and statut == "Inscrit":
            try:
                add_to_membres(user["ID"], user["Nom"], user["Prénom"], user["Lien"], user["Numero"])
                await bot.send_message(
                    user["ID"],
                    f"🎉 مرحبًا {user['Prénom']} {user['Nom']}!\n✅ تم قبولك في الدورة.\n\n"
                    f"اضغط أدناه للانتقال إلى المستوى 1 👇",
                    buttons=[[Button.url("🎓 Niveau 1", LEVEL1_LINK)]],
                )
                mark_as_notified(user["ID"])
                accepted_today += 1
                print(f"✅ إشعار أُرسل إلى {user['Nom']} {user['Prénom']}")
            except Exception as e:
                print(f"⚠️ خطأ أثناء الإشعار {user['ID']}: {e}")

    print(f"📊 عدد المقبولين الذين تم إشعارهم: {accepted_today}")

# --------------------------------------------------------
# دالة حساب التفاعل في مجموعة المستوى 1
# --------------------------------------------------------
async def count_activity(bot):
    level1 = await bot.get_entity(LEVEL1_LINK)
    print("📥 تحميل آخر الرسائل من مجموعة المستوى 1...")
    messages = await bot.get_messages(level1, limit=1000)  # يمكن تعديل الحد حسب الحاجة

    senders = [msg.sender_id for msg in messages if msg.sender_id]
    stats = Counter(senders)

    print("📊 إحصائيات التفاعل:")
    for user_id, count in stats.most_common():
        try:
            user = await bot.get_entity(user_id)
            name = f"{user.first_name or ''} {user.last_name or ''}".strip()

            # 🧮 تحديد التقييم حسب عدد الرسائل
            if count <= 10:
                stars = "⭐"
            elif count <= 30:
                stars = "⭐⭐"
            else:
                stars = "⭐⭐⭐"

            # تحديث Google Sheets
            update_member_activity(user_id, name, count, stars)
            print(f"👤 {name}: {count} رسالة → {stars}")

        except Exception as e:
            print(f"⚠️ خطأ أثناء معالجة المستخدم {user_id}: {e}")

# --------------------------------------------------------
# الحلقة الرئيسية
# --------------------------------------------------------
async def start_check_loop(bot):
    await bot.connect()
    print("🕒 تشغيل حلقة التحقق والتفاعل...")

    while True:
        await check_new_users(bot)
        await count_activity(bot)
        print("✅ تم تحديث الإحصائيات بنجاح. الانتظار 5 دقيقة قبل الدورة التالية...")
        await asyncio.sleep(300)  # كل ساعة