from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database configuration
DB_NAME = 'users.db'
TABLE_NAME = 'users'


# Create database table if it doesn't exist
def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)")
    conn.commit()
    conn.close()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {TABLE_NAME} (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()

        return redirect('/users')

    return render_template('register.html')


@app.route('/users')
def users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    user_data = cursor.fetchall()
    conn.close()

    return render_template('users.html', users=user_data)


if __name__ == '__main__':
    create_table()
    app.run(debug=True)
