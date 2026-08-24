from flask import Flask, session, render_template, request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQLAlchemy(app)


# Registration 
@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("registration.html")
        
    # Registration entities  
    else:
        user_name = request.form.get("name")
        user_username = request.form.get("username")

        user_pwd = request.form.get("password")

        # Error for missing fields
        if not user_name or not user_username  or not user_pwd:
            return render_template("registration.html", message = "Please fill all the fields")

        # Error for same username selection
        reader = db.execute("SELECT username FROM reader WHERE username = :user_username", {"user_username":user_username}).fetchone()
        if reader:
            return render_template("registration.html", message = "Username already exists, choose another") 

        # Insert the data for new user
        else:    
            db.execute("INSERT INTO reader (name, username, age, password) VALUES (:name, :username, :age, :password)",
                       {"name": user_name, "username": user_username, "password": user_pwd})
        db.commit()
        session['username'] = user_username
        return render_template("index.html",error_message="Welcome, you are registered!!")




    

