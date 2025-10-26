from datetime import datetime
from .connexion import connect_sheet

def update_activity(user_id, group_name, live=False):
    sheet = connect_sheet("membres")
    users = sheet.col_values(1)
    str_id = str(user_id)
    if str_id not in users:
        return

    row = users.index(str_id) + 1
    headers = sheet.row_values(1)

    # تحديد المستوى
    level = None
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

    if not level:
        return

    def col(name): return headers.index(name) + 1 if name in headers else None

    msg_col = col(f"{level} - Nbr messages")
    live_col = col(f"{level} - Live")
    last_col = col(f"{level} - Dernier Message")
    inter_col = col(f"{level} - Interaction")

    # تحديث الرسائل
    if msg_col:
        count = int(sheet.cell(row, msg_col).value or 0) + 1
        sheet.update_cell(row, msg_col, count)

    # آخر رسالة
    if last_col:
        sheet.update_cell(row, last_col, datetime.now().strftime("%Y-%m-%d %H:%M"))

    # التفاعل
    if inter_col:
        inter = int(sheet.cell(row, inter_col).value or 0) + 2
        sheet.update_cell(row, inter_col, inter)

    # حضور Live
    if live and live_col:
        live_count = int(sheet.cell(row, live_col).value or 0) + 1
        sheet.update_cell(row, live_col, live_count)
