from .connexion import connect_sheet

def get_template(msg_type, lang="Ar"):
    sheet = connect_sheet("Templates")
    records = sheet.get_all_records()

    lang = lang.capitalize()
    for row in records:
        if row["type"].strip().lower() == msg_type.lower():
            return row.get(lang, row.get("Fr", "❌ Message introuvable")).strip()
    return f"❌ Template '{msg_type}' non trouvé"
