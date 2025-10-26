
from datetime import datetime
from .connexion import connect_sheet

def add_to_membres(user_id, nom, prenom, link, numero):
    sheet = connect_sheet("membres")
    users = sheet.col_values(1)
    str_id = str(user_id)

    if str_id not in users:
        sheet.append_row([
            str_id, nom, prenom, link, numero, "", "Niveau 1", "", "", "",
            datetime.now().strftime("%Y-%m-%d %H:%M"), 0, 0, "", 0,
            *["" for _ in range(35)]
        ])
