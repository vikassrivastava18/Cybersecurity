"""Flask authentication app for login and signup routes."""

from flask import Flask, redirect, render_template, request, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from models import User, db

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# Initialize the database with this app.
db.init_app(app)

# Configure Flask-Login to load users from the database.
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Return the user object for a logged-in session."""
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


# Limit repeated login attempts to prevent brute-force attempts.
limiter = Limiter(get_remote_address, app=app)


@app.route("/login")
def login():
    """Render the login page."""
    return render_template("login.html")


@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login_post():
    """Validate a user login request."""
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for("login"))

    login_user(user, remember=remember)
    return redirect(url_for("profile"))


@app.route("/signup")
def signup():
    """Render the signup page."""
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    """Create a new user account if the email is not already registered."""
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    # Reject duplicate email registrations.
    user = User.query.filter_by(email=email).first()
    if user:
        return redirect(url_for("signup"))

    # Hash the password before storing it in the database.
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password),
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    """Log the current user out and redirect to login."""
    logout_user()
    return redirect(url_for("login"))


@app.route("/profile")
@login_required
def profile():
    """Display the logged-in user's profile page."""
    return render_template("profile.html", name=current_user.name)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
