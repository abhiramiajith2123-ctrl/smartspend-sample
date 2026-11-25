from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite Database Connection
def get_db_connection():
    conn = sqlite3.connect('smartspend_sample.db')
    conn.row_factory = sqlite3.Row
    return conn

# Table automatic aayi create cheyyan
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    transactions = conn.execute("SELECT * FROM transactions ORDER BY created_at DESC").fetchall()
    conn.close()
    
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense')
    balance = total_income - total_expense
    
    return render_template('index.html', 
                           transactions=transactions,
                           total_income=total_income,
                           total_expense=total_expense,
                           balance=balance)

@app.route('/add', methods=['POST'])
def add_transaction():
    t_type = request.form['type']
    description = request.form['description']
    category = request.form['category']
    amount = float(request.form['amount'])
    
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO transactions (type, description, category, amount) VALUES (?, ?, ?, ?)",
        (t_type, description, category, amount)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_transaction(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM transactions WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)