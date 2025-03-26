import os
import json
from flask import Flask, jsonify
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# --- Инициализация Flask
app = Flask(__name__)

# --- Получение переменных окружения
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# --- Запись JSON-файла с ключами (если нужно сохранить локально)
if GOOGLE_CREDENTIALS_JSON:
    with open("credentials.json", "w") as f:
        f.write(GOOGLE_CREDENTIALS_JSON)

# --- Настройка Google API
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

def get_messages():
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    data = sheet.get_all_records()
    return [row['Сообщение'] for row in data if 'Сообщение' in row]

@app.route('/messages')
def messages():
    return jsonify(get_messages())

if __name__ == '__main__':
    app.run(debug=True)
