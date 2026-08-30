import hashlib
import random, string
from database import get_db
import sqlite3


def md5_hash(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def get_random_accounts():

    first_names = [
        "Aarav",
        "Ananya",
        "Rohan",
        "Priya",
        "Arjun",
        "Neha",
        "Vikram",
        "Sneha",
        "Rahul",
        "Kavya",
    ]

    last_names = [
        "Sharma",
        "Patel",
        "Verma",
        "Singh",
        "Gupta",
        "Kumar",
        "Mehta",
        "Joshi",
        "Malhotra",
        "Shah",
    ]

    patterns = [
        lambda f, l: f"{f}123",
        lambda f, l: f"{f}@123",
        lambda f, l: f"{f}2026",
        lambda f, l: f"{f}{l}",
        lambda f, l: f"{f}{l}123",
        lambda f, l: f"{f.lower()}123",
        lambda f, l: f"{f.lower()}@123",
        lambda f, l: f"{f}#2026",
        lambda f, l: f"{l}123",
        lambda f, l: f"{l}@123",
    ]

    accounts = []
    for i in range(10):
        first = first_names[i]
        for j in range(10):
            last = last_names[j]
            username = f"{first} {last}"
            email = f"{first.lower()}.{last.lower()}@example.com"
            pattern = random.choice(patterns)
            password = pattern(first, last)
            accounts.append({"username": username, "email": email, "password": password})
    return accounts


def insert_accounts() -> None:
    """Helper function to add"""
    accounts = get_random_accounts()

    for account in accounts:
        db = get_db()
        username, email, pwd_md5 = account["username"], account["email"], md5_hash(account["password"])
        db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, pwd_md5),
        )
        db.commit()


def insert_bad_accounts(file_name: str) -> None:
    """Helper function to add"""

    with open(file_name, "r", encoding="utf-8") as file:
        content = file.read()
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file.readlines()[:20]:
                content = line.strip()                
                random_string = "".join(
                    random.choices(string.ascii_letters + string.digits, k=5)
                )
                username, email, pwd_md5 = f"{content} {random_string}", f"{content}@gmail.com", md5_hash(content)
                db = get_db()
                try:
                    db.execute(
                                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                                (username, email, pwd_md5),
                                )
                    db.commit()
                except sqlite3.IntegrityError:
                    db.rollback()
                    print("Email already exists.")
    
            

