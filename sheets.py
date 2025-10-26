import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config import SHEET_ID, GOOGLE_CREDENTIALS_FILE

# ----------------------------
# الاتصال بـ Google Sheet
# ----------------------------
def connect_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # ✅ استخدام المتغير البيئي في حالة Pella أو Render
    if os.getenv("GOOGLE_CREDENTIALS_JSON"):
        try:
            creds_json = json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON"))
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        except Exception as e:
            raise Exception(f"❌ خطأ في تحميل GOOGLE_CREDENTIALS_JSON: {e}")
    else:
        # 💻 استخدام الملف المحلي في حالة التطوير المحلي
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)

    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(sheet_name)


# ----------------------------
# جلب قالب رسالة من Templates
# ----------------------------
def get_template(template_type):
    sheet = connect_sheet("Templates")
    records = sheet.get_all_records()
    for row in records:
        if row["type"] == template_type:
            return row["message"]
    return f"❌ Template '{template_type}' not found."


# ----------------------------
# إضافة متربص جديد في portail
# ----------------------------
def add_to_portail(user_id, nom, prenom, numero, username):
    sheet = connect_sheet("portail")
    users = sheet.col_values(1)
    str_id = str(user_id)

    if str_id not in users:
        sheet.append_row([
            str_id, nom, prenom, username, numero, "En attente", datetime.now().strftime("%Y-%m-%d")
        ])
    else:
        row = users.index(str_id) + 1
        sheet.update_cell(row, 2, nom)
        sheet.update_cell(row, 3, prenom)
        sheet.update_cell(row, 4, username)
        sheet.update_cell(row, 5, numero)


# ----------------------------
# التحقق من حالة المتربص في portail
# ----------------------------
def check_status_portail(user_id):
    sheet = connect_sheet("portail")
    users = sheet.col_values(1)
    str_id = str(user_id)
    if str_id in users:
        row = users.index(str_id) + 1
        status = sheet.cell(row, 6).value
        return status
    return None


# ----------------------------
# جلب جميع المتربصين من portail
# ----------------------------
def get_all_portail():
    sheet = connect_sheet("portail")
    headers = [h.strip() for h in sheet.row_values(1) if h.strip() != ""]
    records = sheet.get_all_records(empty2zero=False, head=1)

    for row in records:
        if "status" not in row:
            if "Statut" in row:
                row["status"] = row["Statut"]
            else:
                row["status"] = "En attente"

        if "notified" not in row:
            row["notified"] = False

    if "notified" not in headers:
        sheet.update_cell(1, len(headers) + 1, "notified")
        for row_idx in range(2, len(records) + 2):
            sheet.update_cell(row_idx, len(headers) + 1, "FALSE")

    return records


# ----------------------------
# تحديث علامة notified
# ----------------------------
def mark_as_notified(user_id):
    sheet = connect_sheet("portail")
    records = sheet.get_all_records()
    headers = sheet.row_values(1)
    if "notified" not in headers:
        sheet.update_cell(1, len(headers) + 1, "notified")
        headers.append("notified")

    for idx, row in enumerate(records, start=2):
        if row["ID"] == user_id:
            col_idx = headers.index("notified") + 1
            sheet.update_cell(idx, col_idx, "TRUE")
            break


# ----------------------------
# إضافة المتربص إلى membres
# ----------------------------
def add_to_membres(user_id, nom, prenom, username):
    sheet = connect_sheet("membres")
    users = sheet.col_values(1)
    str_id = str(user_id)

    if str_id not in users:
        sheet.append_row([
            str_id, nom, prenom, username, "", "Niveau 1", datetime.now().strftime("%Y-%m-%d"),
            0, 0, "", 0, *["" for _ in range(35)]
        ])


# ----------------------------
# تحديث النشاط
# ----------------------------
def update_activity(user_id, group_name, live=False):
    sheet = connect_sheet("membres")
    users = sheet.col_values(1)
    str_id = str(user_id)

    if str_id not in users:
        return

    row = users.index(str_id) + 1
    headers = sheet.row_values(1)

    if "1" in group_name:
        level = "Niveau 1"
    elif "2" in group_name:
        level = "Niveau 2"
    elif "3" in group_name:
        level = "Niveau 3"
    elif "4" in group_name:
        level = "Niveau 4"
    elif "VIP" in group_name.upper():
        level = "VIP"
    else:
        return

    def col(name):
        return headers.index(name) + 1 if name in headers else None

    msg_col = col(f"{level} - Nbr messages")
    live_col = col(f"{level} - Live")
    last_col = col(f"{level} - Dernier Message")
    inter_col = col(f"{level} - Interaction")

    if msg_col:
        count = int(sheet.cell(row, msg_col).value or 0) + 1
        sheet.update_cell(row, msg_col, count)

    if last_col:
        sheet.update_cell(row, last_col, datetime.now().strftime("%Y-%m-%d %H:%M"))

    if inter_col:
        inter = int(sheet.cell(row, inter_col).value or 0) + 2
        sheet.update_cell(row, inter_col, inter)

    if live and live_col:
        live_count = int(sheet.cell(row, live_col).value or 0) + 1
        sheet.update_cell(row, live_col, live_count)


# ----------------------------
# 🧠 جلب رسالة من Template حسب اللغة
# ----------------------------
def get_template(msg_type, lang="Ar"):
    sheet = connect_sheet("Templates")
    records = sheet.get_all_records()

    lang = lang.capitalize()

    for row in records:
        if row["type"].strip().lower() == msg_type.lower():
            return row.get(lang, row.get("Fr", "❌ Message introuvable")).strip()

    return f"❌ Template '{msg_type}' non trouvé"
