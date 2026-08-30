from flask import Flask, redirect, render_template, request, url_for
import logging

from database import (close_db, 
                      get_db, 
                      init_db)
from utils import (md5_hash, 
                   insert_bad_accounts, 
                   insert_accounts, 
                   find_bad_accounts)

app = Flask(__name__)

app.teardown_appcontext(close_db)

logging.basicConfig(
    filename="bad_passwords.log",
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(message)s",
)


@app.route("/")
def index():
    db = get_db()
    users = db.execute(
        "SELECT id, username, email FROM users ORDER BY id"
    ).fetchall()
    return render_template("index.html", users=users)


@app.route("/add", methods=["POST"])
def add_user():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password")

    if username and email and password:
        pwd_md5 = md5_hash(password)
        db = get_db()
        db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, pwd_md5),
        )
        db.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    with app.app_context():
        # insert_accounts()
        find_bad_accounts("static/common.txt")
        find_bad_accounts("static/weak.txt")
    app.run(debug=True, host="127.0.0.1", port=5000)
