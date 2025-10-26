<<<<<<< HEAD
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
<<<<<<< HEAD
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

<<<<<<< HEAD


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
<<<<<<< HEAD

        row = users.index(str_id) + 1
        sheet.update_cell(row, 2, nom)
        sheet.update_cell(row, 3, prenom)
        sheet.update_cell(row, 4, username)
        sheet.update_cell(row, 5, numero)

<<<<<<< HEAD
-fix
# ----------------------------
# التحقق من حالة المتربص في portail
# ----------------------------
def check_status_portail(user_id):
    sheet = connect_sheet("portail")
<<<<<<< HEAD
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
<<<<<<< HEAD

    for row in records:
        if "status" not in row:
=======
    
    # تأكد من وجود العمود 'status'
    for row in records:
        if "status" not in row:
            # حاول البحث عن العمود الموجود بالاسم الآخر، مثلا "Statut"
>>>>>>> temp-fix
            if "Statut" in row:
                row["status"] = row["Statut"]
            else:
                row["status"] = "En attente"
<<<<<<< HEAD

        if "notified" not in row:
            row["notified"] = False

    if "notified" not in headers:
        sheet.update_cell(1, len(headers) + 1, "notified")
        for row_idx in range(2, len(records) + 2):
            sheet.update_cell(row_idx, len(headers) + 1, "FALSE")

    return records


# ----------------------------
# تحديث علامة notified
=======
                
        if "notified" not in row:
            row["notified"] = False
            
    # إضافة العمود notified إذا لم يكن موجود
    if "notified" not in headers:
        sheet.update_cell(1, len(headers)+1, "notified")
        for row_idx in range(2, len(records)+2):
            sheet.update_cell(row_idx, len(headers)+1, "FALSE")
            
    return records

# ----------------------------
# تحديث علامة notified لمنع إعادة إرسال الرابط
>>>>>>> temp-fix
# ----------------------------
def mark_as_notified(user_id):
    sheet = connect_sheet("portail")
    records = sheet.get_all_records()
    headers = sheet.row_values(1)
    if "notified" not in headers:
<<<<<<< HEAD
        sheet.update_cell(1, len(headers) + 1, "notified")
=======
        sheet.update_cell(1, len(headers)+1, "notified")
>>>>>>> temp-fix
        headers.append("notified")

    for idx, row in enumerate(records, start=2):
        if row["ID"] == user_id:
            col_idx = headers.index("notified") + 1
            sheet.update_cell(idx, col_idx, "TRUE")
            break
<<<<<<< HEAD


# ----------------------------
# إضافة المتربص إلى membres
# ----------------------------
def add_to_membres(user_id, nom, prenom, username):
=======
# ----------------------------
# إضافة المتربص إلى membres بعد الضغط على الرابط
# ----------------------------
def add_to_membres(user_id, nom, prenom, Link,numero):
>>>>>>> temp-fix
    sheet = connect_sheet("membres")
    users = sheet.col_values(1)
    str_id = str(user_id)

<<<<<<< HEAD
    if str_id not in users:
        sheet.append_row([
            str_id, nom, prenom, username, "", "Niveau 1", datetime.now().strftime("%Y-%m-%d"),
            0, 0, "", 0, *["" for _ in range(35)]
        ])


# ----------------------------
# تحديث النشاط
=======
    # إذا لم يكن موجود مسبقًا
    if str_id not in users:
        sheet.append_row([
            str_id, nom, prenom, Link, numero, "", "Niveau 1","","","", datetime.now().strftime("%Y-%m-%d %H:%M"),
            0, 0, "", 0,  # Nbr messages, Live, Dernier message, Interaction
            *["" for _ in range(35)]  # أعمدة للمستويات الأخرى
        ])
    # إذا موجود مسبقًا يمكن تحديث بيانات الدخول إلى المستوى الجديد لاحقًا

# ----------------------------
# تحديث النشاط (رسائل، تفاعل، حضور Live)
>>>>>>> temp-fix
# ----------------------------
def update_activity(user_id, group_name, live=False):
    sheet = connect_sheet("membres")
    users = sheet.col_values(1)
    str_id = str(user_id)

    if str_id not in users:
        return

    row = users.index(str_id) + 1
    headers = sheet.row_values(1)

<<<<<<< HEAD
=======
    # تحديد المستوى من اسم المجموعة
>>>>>>> temp-fix
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

<<<<<<< HEAD
=======
    # إيجاد الأعمدة لكل مستوى
>>>>>>> temp-fix
    def col(name):
        return headers.index(name) + 1 if name in headers else None

    msg_col = col(f"{level} - Nbr messages")
    live_col = col(f"{level} - Live")
    last_col = col(f"{level} - Dernier Message")
    inter_col = col(f"{level} - Interaction")

<<<<<<< HEAD
=======
    # تحديث عدد الرسائل
>>>>>>> temp-fix
    if msg_col:
        count = int(sheet.cell(row, msg_col).value or 0) + 1
        sheet.update_cell(row, msg_col, count)

<<<<<<< HEAD
    if last_col:
        sheet.update_cell(row, last_col, datetime.now().strftime("%Y-%m-%d %H:%M"))

=======
    # تحديث آخر رسالة
    if last_col:
        sheet.update_cell(row, last_col, datetime.now().strftime("%Y-%m-%d %H:%M"))

    # تحديث التفاعل
>>>>>>> temp-fix
    if inter_col:
        inter = int(sheet.cell(row, inter_col).value or 0) + 2
        sheet.update_cell(row, inter_col, inter)

<<<<<<< HEAD
=======
    # تحديث Live إذا كان True
>>>>>>> temp-fix
    if live and live_col:
        live_count = int(sheet.cell(row, live_col).value or 0) + 1
        sheet.update_cell(row, live_col, live_count)


<<<<<<< HEAD
=======
def log_first_entry(user_id, group_name):
    sheet = connect_sheet("membres")
    users = sheet.col_values(1)
    str_id = str(user_id)

    if str_id not in users:
        return

    row = users.index(str_id) + 1
    headers = sheet.row_values(1)

    # تحديد العمود حسب المجموعة
    if "1" in group_name:
        col_name = "Entrée Niveau 1"
    elif "2" in group_name:
        col_name = "Entrée Niveau 2"
    elif "3" in group_name:
        col_name = "Entrée Niveau 3"
    elif "VIP" in group_name.upper():
        col_name = "Entrée Niveau 4"
    elif "VIP" in group_name.upper():
        col_name = "Entrée VIP"
    else:
        return

    # إذا لم يوجد العمود، أضفه
    if col_name not in headers:
        sheet.update_cell(1, len(headers) + 1, col_name)
        headers.append(col_name)

    col_idx = headers.index(col_name) + 1
    cell_value = sheet.cell(row, col_idx).value

    # سجّل الوقت فقط إذا لم يكن موجودًا من قبل
    if not cell_value:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        sheet.update_cell(row, col_idx, now_str)


>>>>>>> temp-fix
# ----------------------------
# 🧠 جلب رسالة من Template حسب اللغة
# ----------------------------
def get_template(msg_type, lang="Ar"):
<<<<<<< HEAD
    sheet = connect_sheet("Templates")
    records = sheet.get_all_records()

    lang = lang.capitalize()

    for row in records:
        if row["type"].strip().lower() == msg_type.lower():
            return row.get(lang, row.get("Fr", "❌ Message introuvable")).strip()

    return f"❌ Template '{msg_type}' non trouvé"
=======
    sheet = connect_sheet("Templates")  # اسم الورقة في Google Sheets
    records = sheet.get_all_records()

    lang = lang.capitalize()  # لضمان التطابق (Ar, Fr, An)

    for row in records:
        if row["type"].strip().lower() == msg_type.lower():
            # نحاول جلب الرسالة باللغة المطلوبة
            return row.get(lang, row.get("Fr", "❌ Message introuvable")).strip()

    return f"❌ Template '{msg_type}' non trouvé"
>>>>>>> temp-fix
