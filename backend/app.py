import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# Cho phép mọi nơi (bao gồm Netlify của bạn) gọi vào API này
CORS(app)

# Tên file database
DB_NAME = "notes.db"

# Hàm khởi tạo DB nếu chưa có
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Chạy tạo bảng ngay khi khởi động
init_db()

@app.route('/')
def home():
    return "Backend is running!"

# API lấy danh sách ghi chú
@app.route('/api/notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    # Chuyển đổi dữ liệu sang JSON
    notes = [{'id': row[0], 'content': row[1]} for row in rows]
    return jsonify(notes)

# API thêm ghi chú mới
@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({"error": "No content"}), 400
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Added successfully"}), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)