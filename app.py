
import os
from flask import Flask, render_template_string, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import mysql.connector
import os
from flask import abort

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_TO_A_RANDOM_SECRET_KEY"

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

from flask import Flask, render_template_string, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get("MYSQL_PASSWORD"),
        database="book_management"
    )
import os
from flask import abort

ADMIN_USER = os.environ.get("BOOK_ADMIN_USER")
ADMIN_PASSWORD_HASH = os.environ.get("BOOK_ADMIN_PASSWORD_HASH")
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #eef2ff, #ddd6fe);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }
        .login-card {
            background: white;
            padding: 32px;
            border-radius: 16px;
            width: 320px;
            max-width: calc(100% - 80px);
            box-shadow: 0 8px 30px #00000015;
        }
        h1 { color: #4338ca; }
        input, button {
            box-sizing: border-box;
            width: 100%;
            padding: 12px;
            margin-top: 12px;
            border-radius: 8px;
        }
        input { border: 1px solid #cbd5e1; }
        button {
            background: #4f46e5;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        .error { color: #dc2626; }
    </style>
</head>
<body>
    <div class="login-card">
        <h1>Admin Login</h1>
        <p>Login to manage your books.</p>
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
        <form method="post">
            <input type="text" name="username"
                   placeholder="Admin username" required>
            <input type="password" name="password"
                   placeholder="Admin password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""
@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if (
            ADMIN_USER
            and ADMIN_PASSWORD_HASH
            and username == ADMIN_USER
            and check_password_hash(ADMIN_PASSWORD_HASH, password)
        ):
            session["admin_logged_in"] = True
            return redirect("/")

        error = "Invalid username or password"

    return render_template_string(LOGIN_PAGE, error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Book Management System</title>
       <style>
    * {
        box-sizing: border-box;
    }

    body {
        font-family: 'Segoe UI', Arial, sans-serif;
        max-width: 850px;
        margin: 0 auto;
        padding: 30px 20px;
        background: linear-gradient(135deg, #eef2ff, #f5f3ff);
        color: #1e293b;
        min-height: 100vh;
    }

    h1 {
        color: #4338ca;
        font-size: 32px;
        margin-bottom: 25px;
    }

    h2 {
        color: #312e81;
        margin-top: 0;
        font-size: 21px;
    }

    section {
        background: white;
        padding: 25px;
        margin: 20px 0;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(30, 41, 59, 0.08);
        border: 1px solid #e0e7ff;
    }

    input {
        padding: 12px 14px;
        margin: 6px 4px 6px 0;
        border: 1px solid #cbd5e1;
        border-radius: 9px;
        font-size: 15px;
        max-width: 100%;
    }

    input:focus {
        outline: 2px solid #818cf8;
        border-color: #6366f1;
    }

    button {
        padding: 11px 17px;
        border: none;
        border-radius: 9px;
        background: #4f46e5;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: 0.2s;
    }

    button:hover {
        background: #3730a3;
        transform: translateY(-1px);
    }

    a {
        color: #4f46e5;
        margin-left: 8px;
        text-decoration: none;
        font-weight: 600;
    }

    a:hover {
        text-decoration: underline;
    }

    ul {
        list-style: none;
        padding: 0;
        margin-bottom: 0;
    }

    li {
        padding: 14px;
        margin: 10px 0;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        flex-wrap: wrap;
    }

    li form {
        margin-left: auto;
    }

    li button {
        background: #dc2626;
        padding: 8px 12px;
    }

    li button:hover {
        background: #991b1b;
    }

    @media (max-width: 600px) {
        body {
            padding: 18px 12px;
        }

        h1 {
            font-size: 26px;
        }

        section {
            padding: 18px;
        }

        input {
            width: 100%;
            margin: 6px 0;
        }
    }
</style>
    
</head>
<body>
    <h1>📚 Book Management System</h1>
    <section>
        <h2>Add Book</h2>
        <form method="post" action="/add">
            <input type="number" name="id" placeholder="Book ID" required>
            <input type="text" name="name" placeholder="Book Name" required>
            <button type="submit">Add Book</button>
        </form>
    </section>
    <section>
        <h2>Book List</h2>
        <form method="get" action="/">
    <input
        type="search"
        name="q"
        placeholder="Search by Book ID or Name"
        value="{{ query }}"
    >
    <button type="submit">Search</button>
    <a href="/">Clear</a>
</form>
        <ul>
        {% for book in books %}
           <li>
    <span>{{ book[0] }} — {{ book[1] }}</span>

<form method="post"
      action="/upload_notes/{{ book[0] }}"
      enctype="multipart/form-data"
      style="display: inline;">
    <input type="file" name="pdf" accept=".pdf,application/pdf" required>
    <button type="submit">Upload Notes</button>
</form>

    <form method="post"
          action="/delete/{{ book[0] }}"
          style="display: inline;">
        <button type="submit"
                onclick="return confirm('Are you sure you want to delete this book?')">
            Delete
        </button>
    </form>
</li>
        {% else %}
            <li>No books yet. Add your first book!</li>
        {% endfor %}
        </ul>
    </section>
</body>
</html>
"""
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def home():
    search = request.args.get("q", "").strip()

    db = get_db()
    cursor = db.cursor()

    if search:
        cursor.execute(
            """
            SELECT id, name FROM books
            WHERE CAST(id AS CHAR) = %s
            OR name LIKE %s
            ORDER BY id
            """,
            (search, "%" + search + "%")
        )
    else:
        cursor.execute("SELECT id, name FROM books ORDER BY id")

    books = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template_string(
        PAGE, books=books, query=search
    )


@app.route("/add", methods=["POST"])
@login_required
def add_book():
    book_id = int(request.form["id"])
    name = request.form["name"].strip()

    if book_id <= 0 or not name:
        return "Valid Book ID aur name enter karo.", 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO books (id, name) VALUES (%s, %s)",
            (book_id, name)
        )
        db.commit()
    except mysql.connector.IntegrityError:
        db.rollback()
        cursor.close()
        db.close()
        return "Ye Book ID pehle se hai. Doosri ID try karo.", 400

    cursor.close()
    db.close()
    return redirect("/")
@app.route("/delete/<int:book_id>", methods=["POST"])
@login_required 
def delete_book(book_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM books WHERE id = %s",
        (book_id,)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect("/")

@app.route("/upload_notes/<int:book_id>", methods=["POST"])
@login_required
def upload_notes(book_id):
    pdf = request.files.get("pdf")

    if not pdf or not pdf.filename:
        return "Pehle PDF file select karo.", 400

    if not pdf.filename.lower().endswith(".pdf"):
        return "Sirf PDF files allowed hain.", 400

    filename = secure_filename(pdf.filename)

    # File ke andar PDF signature check karo
    pdf.stream.seek(0)
    if not pdf.stream.read(5).startswith(b"%PDF-"):
        return "Valid PDF file select karo.", 400
    pdf.stream.seek(0)

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id FROM books WHERE id = %s",
        (book_id,)
    )

    if not cursor.fetchone():
        cursor.close()
        db.close()
        return "Book nahi mili.", 404

    saved_filename = f"book_{book_id}.pdf"
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        saved_filename
    )

    pdf.save(file_path)

    cursor.execute(
        "UPDATE books SET notes_pdf = %s WHERE id = %s",
        (saved_filename, book_id)
    )
    db.commit()

    cursor.close()
    db.close()

    return redirect("/")

@app.route("/notes/<int:book_id>")
@login_required
def view_notes(book_id):
    from flask import send_from_directory

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT notes_pdf FROM books WHERE id = %s",
        (book_id,)
    )
    result = cursor.fetchone()

    cursor.close()
    db.close()

    if not result or not result[0]:
        return "Is book ke notes abhi upload nahi hue hain.", 404

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        result[0],
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
