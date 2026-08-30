"""Flask app entry point for user registration and database setup."""
import logging

from flask import Flask, redirect, render_template, request, url_for

from database import close_db, get_db, init_db
from utils import salted_hash

# Create the Flask application instance.
app = Flask(__name__)

# Close any database connection at the end of each request.
app.teardown_appcontext(close_db)

# Configure logging for password warnings and security-related events.
logging.basicConfig(
    filename="bad_passwords.log",
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(message)s",
)


@app.route("/")
def index():
    """Display the list of registered users."""
    db = get_db()
    users = db.execute(
        "SELECT id, username, email FROM users ORDER BY id"
    ).fetchall()
    return render_template("index.html", users=users)


@app.route("/add", methods=["POST"])
def add_user():
    """Register a new user with a securely hashed password."""
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password")

    if username and email and password:
        password_hash = salted_hash(password)
        db = get_db()
        db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password_hash),
        )
        db.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    # Ensure the database schema exists before the app starts.
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
