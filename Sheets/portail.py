from datetime import datetime
from .connexion import connect_sheet

def add_to_portail(user_id, nom, prenom, numero, username):
    sheet = connect_sheet("portail")
    users = sheet.col_values(1)
    str_id = str(user_id)

    if str_id not in users:
        sheet.append_row([
            str_id, nom, prenom, username, numero, "En attente", datetime.now().strftime("%Y-%m-%d %H:%M")
        ])
    else:
        row = users.index(str_id) + 1
        sheet.update_cell(row, 2, nom)
        sheet.update_cell(row, 3, prenom)
        sheet.update_cell(row, 4, username)
        sheet.update_cell(row, 5, numero)

def check_status_portail(user_id):
    sheet = connect_sheet("portail")
    users = sheet.col_values(1)
    str_id = str(user_id)
    if str_id in users:
        row = users.index(str_id) + 1
        return sheet.cell(row, 6).value
    return None

def mark_as_notified(user_id):
    sheet = connect_sheet("portail")
    records = sheet.get_all_records()
    headers = sheet.row_values(1)

    if "notified" not in headers:
        sheet.update_cell(1, len(headers)+1, "notified")
        headers.append("notified")

    for idx, row in enumerate(records, start=2):
        if str(row.get("ID", "")) == str(user_id):
            col_idx = headers.index("notified") + 1
            sheet.update_cell(idx, col_idx, "TRUE")
            break
