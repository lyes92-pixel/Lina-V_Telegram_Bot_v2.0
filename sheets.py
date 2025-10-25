import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config import SHEET_ID, GOOGLE_CREDENTIALS_FILE

# 🔹 الاتصال بـ Google Sheet
def connect_sheet(sheet_name="Members"):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(sheet_name)

# 🔹 قراءة Template من ورقة Templates
def get_template(template_type):
    sheet = connect_sheet("Templates")
    records = sheet.get_all_records()
    for row in records:
        if row["type"] == template_type:
            return row["message"]
    return f"❌ Template '{template_type}' not found."

# 🔹 تحديد اسم العمود المناسب حسب المجموعة
def get_level_columns(group_name):
    if "1" in group_name:
        return "Niveau 1"
    elif "2" in group_name:
        return "Niveau 2"
    elif "3" in group_name:
        return "Niveau 3"
    elif "4" in group_name:
        return "Niveau 4"
    elif "VIP" in group_name.upper():
        return "VIP"
    else:
        return None

# 🔹 إضافة أو تحديث مستخدم عند دخوله مجموعة
def add_or_update_user(user_id, nom, prenom, username, group_name):
    sheet = connect_sheet("Members")
    users = sheet.col_values(1)
    str_id = str(user_id)

    level = get_level_columns(group_name)
    if not level:
        return f"⚠️ Groupe {group_name} non reconnu."

    if str_id in users:
        row = users.index(str_id) + 1
    else:
        sheet.append_row([
            str_id, nom, prenom, username, "", "", group_name,
            "Actif", 0, "",  # Rappel vide
            # Niveaux 1 → VIP (كلها فارغة عند البداية)
            *["" for _ in range(30)]
        ])
        row = len(users) + 1

    # 🔹 تحديث بيانات المستوى الحالي
    headers = sheet.row_values(1)
    def find_col(title): return headers.index(title) + 1 if title in headers else None

    date_col = find_col(f"{level} - Date d’entrée")
    msg_col = find_col(f"{level} - Nbr messages")
    last_col = find_col(f"{level} - Dernier Message")
    inter_col = find_col(f"{level} - Interaction")

    if date_col:
        sheet.update_cell(row, date_col, datetime.now().strftime("%Y-%m-%d"))
    if msg_col:
        sheet.update_cell(row, msg_col, 0)
    if last_col:
        sheet.update_cell(row, last_col, "")
    if inter_col:
        sheet.update_cell(row, inter_col, 0)

# 🔹 تحديث النشاط (عدد الرسائل والتفاعل)
def update_activity(user_id, group_name):
    sheet = connect_sheet("Members")
    users = sheet.col_values(1)
    str_id = str(user_id)

    level = get_level_columns(group_name)
    if not level:
        return

    if str_id in users:
        row = users.index(str_id) + 1
        headers = sheet.row_values(1)

        def find_col(title): return headers.index(title) + 1 if title in headers else None
        msg_col = find_col(f"{level} - Nbr messages")
        last_col = find_col(f"{level} - Dernier Message")
        inter_col = find_col(f"{level} - Interaction")

        # 🔹 تحديث القيم
        if msg_col:
            count = int(sheet.cell(row, msg_col).value or 0) + 1
            sheet.update_cell(row, msg_col, count)

        if last_col:
            sheet.update_cell(row, last_col, datetime.now().strftime("%Y-%m-%d %H:%M"))

        if inter_col:
            inter = int(sheet.cell(row, inter_col).value or 0) + 2  # مثال: +2 نقطة تفاعل
            sheet.update_cell(row, inter_col, inter)
