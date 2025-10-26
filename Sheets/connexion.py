import gspread
from oauth2client.service_account import ServiceAccountCredentials
from Sheets.config import SHEET_ID, GOOGLE_CREDENTIALS_FILE

def connect_sheet(sheet_name: str):
    """
    🔗 الاتصال بملف Google Sheet
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(sheet_name)
