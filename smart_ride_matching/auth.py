import json
import hashlib
import os
import secrets

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "users.json")


def _load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_users(users):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def _hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return salt, hashed.hex()


def signup(username, password):
    username = username.strip()
    if not username or not password:
        return False, "Username and password are required."
    if len(password) < 4:
        return False, "Password must be at least 4 characters."
    users = _load_users()
    if username in users:
        return False, "Username already exists."
    salt, hashed = _hash_password(password)
    users[username] = {"salt": salt, "password": hashed}
    _save_users(users)
    return True, "Account created successfully!"


def login(username, password):
    username = username.strip()
    users = _load_users()
    if username not in users:
        return False, "Invalid username or password."
    user = users[username]
    _, hashed = _hash_password(password, user["salt"])
    if hashed == user["password"]:
        return True, "Login successful!"
    return False, "Invalid username or password."
