from telethon import events
from Sheets.portail import add_to_portail
from Sheets.activity import update_activity
from Sheets.templates import get_template

def register_registration_handlers(bot, user_state):

    @bot.on(events.CallbackQuery(data=b"start_registration"))
    async def start_registration(event):
        sender_id = event.sender_id
        lang = user_state.get(sender_id, {}).get("lang", "Ar")
        user_state[sender_id]["step"] = "nom"
        await event.answer()
        await event.edit(get_template("ask_name", lang))

    @bot.on(events.NewMessage)
    async def main_handler(event):
        sender_id = event.sender_id
        if sender_id not in user_state:
            if event.is_private or event.is_group:
                sender = await event.get_sender()
                update_activity(sender.id, "Niveau 1", live=False)
            return

        state = user_state[sender_id]
        step = state.get("step")
        lang = state.get("lang", "Ar")
        text = event.text.strip()

        if step == "lang_select":
            return

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
            add_to_portail(sender_id, state["nom"], state["prenom"], state["numero"], username)
            await event.respond(get_template("waiting_validation", lang))
            del user_state[sender_id]
