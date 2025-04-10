#!/usr/bin/env python3
from tinydb import TinyDB, Query
import getpass
import time
import os

db_path = "users.json"
db = TinyDB(db_path)
User = Query()

def user_exists(user_id):
    return db.contains(User.user_id == user_id)

def add_user():
    print("🧙‍♂️ GhostAdmin: Add New User")
    user_id = input("👤 User ID: ").strip()

    if user_exists(user_id):
        print("⚠️ User already exists!")
        return

    password = getpass.getpass("🔐 Password: ").strip()
    confirm = getpass.getpass("🔐 Confirm Password: ").strip()
    if password != confirm:
        print("❌ Passwords do not match.")
        return

    token = input("🔑 Optional token (press enter to skip): ").strip()
    locked = input("🚫 Lock user immediately? [y/N]: ").strip().lower() == "y"

    record = {
        "user_id": user_id,
        "password": password,
        "token": token if token else None,
        "locked": locked,
        "activated": False,
        "last_access": None,
        "last_ip": None
    }

    db.insert(record)
    print(f"✅ User '{user_id}' created successfully.")

if __name__ == "__main__":
    add_user()
