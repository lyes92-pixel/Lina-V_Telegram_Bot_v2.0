from telethon import events, Button
from Sheets.templates import get_template

def register_welcome_handlers(bot, user_state):

    @bot.on(events.NewMessage(incoming=True))
    async def auto_welcome(event):
        sender_id = event.sender_id
        if sender_id not in user_state:
            user_state[sender_id] = {"step": "lang_select"}
            welcome_image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiD6ImSjQAFVJr3B6sagk6aHOzlx7e9pzgdw&s"

            await bot.send_file(
                sender_id,
                file=welcome_image,
                caption=(
                    "👋 **مرحبا بيك في MMG!** 💪\n\n"
                    "أنا هو **Expert X**، راح نكون معاك خطوة بخطوة باش تتعلم وتخدم مشروعك 🛍️💻\n"
                    "🌍 اختار اللغة اللي تحب تكمل بيها 👇"
                ),
                buttons=[
                    [Button.inline("🇩🇿 العربية", b"lang_ar"),
                     Button.inline("🇫🇷 Français", b"lang_fr"),
                     Button.inline("🇬🇧 English", b"lang_en")]
                ],
            )
            return

        if user_state[sender_id].get("step") == "lang_select":
            return

    @bot.on(events.CallbackQuery(pattern=b"lang_"))
    async def set_language(event):
        sender_id = event.sender_id
        lang_code = event.data.decode().split("_")[1].capitalize()
        user_state[sender_id] = {"lang": lang_code, "step": "start"}
        welcome_message = get_template("welcome", lang_code)
        await event.answer()
        await event.edit(
            welcome_message,
            buttons=[[Button.inline("📝 تسجيل / Register / Inscription", b"start_registration")]],
        )
