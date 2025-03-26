import os
import json
from flask import Flask, jsonify
from oauth2client.service_account import ServiceAccountCredentials
from flask_cors import CORS
import gspread

# --- Инициализация Flask
app = Flask(__name__)
CORS(app)

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
if not SPREADSHEET_ID:
    raise ValueError("❌ Ошибка: SPREADSHEET_ID не найдено!")

CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
if not CREDENTIALS_JSON:
    raise ValueError("❌ Ошибка: GOOGLE_CREDENTIALS_JSON не найдено!")

# --- Авторизация и подключение к Google Sheets
try:
    creds_dict = json.loads(CREDENTIALS_JSON)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n").strip()
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
    client = gspread.authorize(creds)
except Exception as e:
    raise ValueError(f"❌ Ошибка подключения к Google Sheets: {e}")

# --- Получение сообщений
def get_messages():
    try:
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        data = sheet.get_all_records()
        messages = []

        for row in data:
            text = row.get("Input")
            name = row.get("Name")
            if text and name:
                messages.append({"name": name, "text": text})

        return messages
    except Exception as e:
        return [{"error": f"❌ Ошибка чтения данных: {str(e)}"}]

# --- Роут для API
@app.route('/messages')
def messages():
    return jsonify(get_messages())

# --- Запуск сервера
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
