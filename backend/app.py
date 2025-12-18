import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Lấy đường dẫn DB từ biến môi trường trên Render
DB_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Tạo bảng theo cú pháp PostgreSQL
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Khởi tạo bảng ngay khi server chạy
try:
    init_db()
    print("Database connected and initialized!")
except Exception as e:
    print(f"Error connecting to DB: {e}")

@app.route('/')
def home():
    return "Backend with PostgreSQL is running!"

@app.route('/api/notes', methods=['GET'])
def get_notes():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM notes ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        notes = [{'id': row[0], 'content': row[1]} for row in rows]
        return jsonify(notes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({"error": "No content"}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Postgres dùng %s thay vì ?
        cur.execute("INSERT INTO notes (content) VALUES (%s)", (content,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)