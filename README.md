# Cybersecurity

<p>Notes on cybersecurity with demonstrable code snippets for building secure applications</p>


## Securing Accounts
<p> Forcing a user to keep strong password makes their account more secure to cyberattacks.</p>

```
pip install Flask-WTF email-validator

from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError

class RegisterForm(FlaskForm):
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(message="Password is required."),
            Length(min=8, message="Password must be at least 8 characters long.")
        ]
    )
    submit = SubmitField('Submit')

    # Custom validator for extra security complexity
    def validate_password(self, field):
        password = field.data
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one number.')
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least one lowercase letter.')

```

<p><b> Limitation:</b> The password still lacks sophistication. Check some common RegEX patterns that makes it harder to guess.</p>


## Securing Data
<p> Storing plain passwords is severe security risks, saving hashed password is a must for applications</p>
<p>Flask implementation:</p>

> ```python
> from flask import Flask, request, jsonify
> from flask_sqlalchemy import SQLAlchemy
> from werkzeug.security import generate_password_hash, check_password_hash
>
> app = Flask(__name__)
> app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
> db = SQLAlchemy(app)
>
> # User Database Model
> class User(db.Model):
>     id = db.Column(db.Integer, primary_key=True)
>     username = db.Column(db.String(80), unique=True, nullable=False)
>     password_hash = db.Column(db.String(256), nullable=False) # Stores the secure hash
>
>     def set_password(self, password):
>         """Hashes the password and saves it to the model."""
>         self.password_hash = generate_password_hash(password)
>
>     def check_password(self, password):
>         """Checks the provided password against the stored hash."""
>         return check_password_hash(self.password_hash, password)
>
> # User Registration Route
> @app.route('/register', methods=['POST'])
> def register():
>     data = request.get_json()
>     if User.query.filter_by(username=data['username']).first():
>         return jsonify({"error": "User already exists"}), 400
>         
>     new_user = User(username=data['username'])
>     new_user.set_password(data['password']) # Hash before saving
>     db.session.add(new_user)
>     db.session.commit()
>     return jsonify({"message": "User registered successfully!"}), 201
>
> # User Login Route
> @app.route('/login', methods=['POST'])
> def login():
>     data = request.get_json()
>     user = User.query.filter_by(username=data['username']).first()
>     
>     if user and user.check_password(data['password']): # Verify hash
>         return jsonify({"message": "Login successful!"}), 200
>         
>     return jsonify({"error": "Invalid credentials"}), 401
>
> if __name__ == '__main__':
>     with app.app_context():
>         db.create_all()
>     app.run(debug=True)
>
> ```


<p><b>Limitations</b>: If an attacker gets your database, they can calculate SHA-256 for millions/billions of candidate passwords and compare the results.

That's why password storage uses algorithms such as Argon2id, which are deliberately expensive to compute and include a salt.</p>


## Securing systems
<p><b>Use HTTPS</b> protocol for encrypted traffic between parties.</p>

<p>If one gives users ability to connect to a remote server via say SSH, one should have some guardrails to keep the system secure.</p>

- Don't expose SSH directly to the whole Internet
- Use SSH keys, not passwords.
- Give developers individual accounts
- Log everything important
- Alert on suspicious behavior

## Securing software
<b>Major bug, can you tell?</b>
```
import os
import logging

from flask import (
    Flask,
    request,
    redirect,
    jsonify,
    render_template,
)

app = Flask(__name__)
logger = logging.getLogger(__name__)

logged_in = False


def verify_login():
    """Check the global login status."""

    if not logged_in:
        logger.warning("Unauthorized access attempt - user not logged in")
        return redirect("/login?error=not_logged_in", code=307)

    return None


@app.get("/login")
def login_page():
    logger.info("Login page accessed")
    return render_template("login.html")


@app.post("/login/")
def login():
    global logged_in

    try:
        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == os.getenv("user")
            and password == os.getenv("password")
        ):
            logged_in = True
            logger.info("Successful login for user: %s", username)
            return jsonify({"message": "Logged"})

        else:
            logger.warning(
                "Failed login attempt with username: %s",
                username
            )
            return redirect(
                "/?error=invalid_credentials",
                code=303
            )

    except Exception as e:
        logger.error(
            "Error during login process: %s",
            e,
            exc_info=True
        )
        return redirect(
            "/?error=login_error",
            code=303
        )
```


## Authorization

```
class Post(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

class IsAuthorForUpdate(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ("PUT", "PATCH"):
            return obj.author == request.user

        return True

class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorForUpdate]
```

