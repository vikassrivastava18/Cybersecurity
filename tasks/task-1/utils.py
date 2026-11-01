"""Utility helpers for password hashing and account management."""

import hashlib
import logging
import random
import sqlite3
import string

from werkzeug.security import generate_password_hash
from zxcvbn import zxcvbn

from database import get_db

logger = logging.getLogger(__name__)


def md5_hash(password: str) -> str:
    """Return the MD5 hash for a plaintext password."""
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def salted_hash(password: str) -> str:
    """Return a salted password hash using Werkzeug."""
    return generate_password_hash(password)


def get_random_accounts():
    """Generate sample user accounts with common password patterns."""
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
        lambda first, last: f"{first}123",
        lambda first, last: f"{first}@123",
        lambda first, last: f"{first}2026",
        lambda first, last: f"{first}{last}",
        lambda first, last: f"{first}{last}123",
        lambda first, last: f"{first.lower()}123",
        lambda first, last: f"{first.lower()}@123",
        lambda first, last: f"{first}#2026",
        lambda first, last: f"{last}123",
        lambda first, last: f"{last}@123",
    ]

    accounts = []
    for first in first_names:
        for last in last_names:
            username = f"{first} {last}"
            email = f"{first.lower()}.{last.lower()}@example.com"
            pattern = random.choice(patterns)
            password = pattern(first, last)
            accounts.append(
                {
                    "username": username,
                    "email": email,
                    "password": password,
                }
            )
    return accounts


def insert_accounts() -> None:
    """Insert a set of demo accounts using MD5-hashed passwords."""
    accounts = get_random_accounts()

    for account in accounts:
        db = get_db()
        username = account["username"]
        email = account["email"]
        pwd_md5 = md5_hash(account["password"])

        db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, pwd_md5),
        )
        db.commit()


def insert_bad_accounts(file_name: str) -> None:
    """Insert weak sample accounts from a text file."""
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file.readlines()[:20]:
            content = line.strip()
            if not content:
                continue

            random_string = "".join(
                random.choices(string.ascii_letters + string.digits, k=5)
            )
            username = f"{content} {random_string}"
            email = f"{content}@gmail.com"
            password_hash = md5_hash(content)

            db = get_db()
            try:
                db.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, password_hash),
                )
                db.commit()
            except sqlite3.IntegrityError:
                db.rollback()
                logger.warning("Email already exists for %s", email)


def find_bad_accounts(file_name: str) -> list:
    """Return user records whose password hash matches a weak-password list."""
    bad_accounts = []

    with open(file_name, "r", encoding="utf-8") as file:
        bad_passwords = {line.strip() for line in file if line.strip()}

    bad_hashes = {md5_hash(password): password for password in bad_passwords}

    db = get_db()
    users = db.execute(
        "SELECT id, username, email, password FROM users"
    ).fetchall()

    for user in users:
        password_hash = user["password"]

        if password_hash in bad_hashes:
            bad_accounts.append(
                {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                }
            )

            logger.warning(
                "Bad password detected for account: id=%s username=%s email=%s",
                user["id"],
                user["username"],
                user["email"],
            )

    return bad_accounts


def validate_password(password, user_inputs=None, MIN_LENGTH=12, MAX_LENGTH=128):
    """Validate password strength using a minimum length and zxcvbn scoring."""
    if not isinstance(password, str):
        return False, ["Invalid password."]

    if len(password) < MIN_LENGTH:
        return False, [
            f"Password must be at least {MIN_LENGTH} characters long."
        ]

    if len(password) > MAX_LENGTH:
        return False, [
            f"Password must not exceed {MAX_LENGTH} characters."
        ]

    result = zxcvbn(password, user_inputs=user_inputs or [])

    if result["score"] < 3:
        feedback = result.get("feedback", {})
        errors = []

        if feedback.get("warning"):
            errors.append(feedback["warning"])

        errors.extend(feedback.get("suggestions", []))

        if not errors:
            errors.append("Password is too easy to guess.")

        return False, errors

    return True, []

