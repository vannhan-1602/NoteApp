from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app) # Cho phép Frontend gọi vào

DB_FILE = 'notes.db'

# Hàm khởi tạo Database nếu chưa có
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Tạo bảng notes
    c.execute('''CREATE TABLE IF NOT EXISTS notes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  title TEXT, 
                  content TEXT)''')
    # Thêm dữ liệu mẫu (nếu bảng rỗng)
    c.execute('SELECT count(*) FROM notes')
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", ('Project 2', 'Code Python Flask'))
        c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", ('Deadline', 'Nop bai thi DevOps'))
        conn.commit()
    conn.close()

# Chạy hàm tạo DB ngay khi App khởi động
init_db()

# API lấy danh sách ghi chú
@app.route('/api/notes', methods=['GET'])
def get_notes():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row # Để lấy dữ liệu dạng từ điển
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes")
        rows = cursor.fetchall()
        conn.close()
        
        # Chuyển đổi sang JSON
        result = []
        for row in rows:
            result.append({"id": row["id"], "title": row["title"], "content": row["content"]})
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)