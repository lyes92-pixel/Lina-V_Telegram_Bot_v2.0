import asyncio
from Sheets.portail import get_all_portail, mark_as_notified
from Sheets.membres import add_to_membres
from Sheets.config import LEVEL1_LINK
from telethon import Button

async def start_check_loop(bot):
    await bot.connect()
    print("🕒 التحقق من الحالات كل 1 دقائق...")

    while True:
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
        await asyncio.sleep(60)
