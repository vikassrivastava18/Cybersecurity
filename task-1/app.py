from flask import Flask, redirect, render_template, request, url_for

from database import close_db, get_db, init_db

app = Flask(__name__)

app.teardown_appcontext(close_db)


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

    if username and email:
        db = get_db()
        db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, ""),
        )
        db.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
