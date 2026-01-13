from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY_123"

# ==========================
# SQLITE DATABASE SETUP
# ==========================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "library.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# CREATE TABLE
with get_db_connection() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            publisher TEXT,
            genre TEXT,
            language TEXT
        )
    """)
    conn.commit()

# ==========================
# ROUTES
# ==========================
@app.route("/")
def index():
    return redirect(url_for("register_book"))

@app.route("/register", methods=["GET", "POST"])
def register_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        publisher = request.form["publisher"]
        genre = request.form["genre"]
        language = request.form["language"]

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO books (title, author, publisher, genre, language)
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, publisher, genre, language))
        conn.commit()
        conn.close()

        return redirect(url_for("success"))

    return render_template("register_book.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/books")
def book_list():
    search = request.args.get("search")

    conn = get_db_connection()
    if search:
        books = conn.execute(
            """
            SELECT * FROM books
            WHERE title LIKE ?
            OR author LIKE ?
            OR genre LIKE ?
            """,
            (f"%{search}%", f"%{search}%", f"%{search}%")
        ).fetchall()
    else:
        books = conn.execute("SELECT * FROM books").fetchall()

    conn.close()
    return render_template("book.html", books=books, search=search)

if __name__ == "__main__":
    app.run(debug=True)
