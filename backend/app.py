from flask import Flask, request, jsonify
import logging
import sqlite3

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  value1 TEXT NOT NULL,
                  value2 TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.json
        value1 = data['value1']
        value2 = data['value2']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO data (value1, value2) VALUES (?, ?)", (value1, value2))
        conn.commit()
        conn.close()
        logging.info(f"Inserted values: {value1}, {value2}")
        return jsonify({'message': 'Data inserted successfully!'}), 201
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': f'Failed to insert data: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
