# Cybersecurity

<p>Notes on cybersecurity with demonstrable code snippets for building secure applications</p>

## Securing Accounts
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



