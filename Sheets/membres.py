
from datetime import datetime
from .connexion import connect_sheet

def add_to_membres(user_id, nom, prenom, link, numero):
    sheet = connect_sheet("membres")
    users = sheet.col_values(1)
    str_id = str(user_id)

    if str_id not in users:
        sheet.append_row([
            str_id,
            nom, 
            prenom, 
            link, 
            numero,
            "", 
            "Niveau 1", 
            "", 
            "", 
            "",
            datetime.now().strftime("%Y-%m-%d %H:%M"), 
            0, 
            0, 
            "", 
            0,
            *["" for _ in range(35)]
        ])

def update_member_activity(user_id, name, messages_count, stars):
    """
    تحدّث بيانات العضو في Google Sheets مع عدد الرسائل والتفاعل
    """
    sheet = connect_sheet("membres")
    all_data = sheet.get_all_records()

    for i, row in enumerate(all_data, start=2):  # الصف 2 لأن الصف 1 هو العناوين
        if str(row.get("ID")) == str(user_id):
            sheet.update(f"E{i}", messages_count)  # عمود عدد الرسائل
            sheet.update(f"F{i}", stars)           # عمود التفاعل
            return

    # إذا لم يكن العضو موجودًا، أضفه
    sheet.append_row([user_id, name, messages_count, stars])