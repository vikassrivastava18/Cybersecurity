from flask import Flask, render_template, url_for, redirect, request
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash

from models import User, db

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()

@app.route('/login')
def login():
    return render_template('login.html')

limiter = Limiter(
    get_remote_address,
    app=app
)


@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('login'))

    login_user(user, remember=remember)
    print("Login successful")
    return redirect(url_for('profile'))


@app.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        return redirect(url_for('signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)