#!/usr/bin/env python3
from tinydb import TinyDB, Query
import os
import time

db_path = "users.json"
db = TinyDB(db_path)
User = Query()

def view_users():
    print("\n👁️ All Users:")
    users = db.all()
    if not users:
        print("  (none)")
        return
    for u in users:
        print(f"- {u['user_id']} | Locked: {u.get('locked', False)} | Activated: {u.get('activated', False)} | Last IP: {u.get('last_ip', 'n/a')} | Last Access: {time.ctime(u['last_access']) if u.get('last_access') else 'n/a'}")

def delete_user():
    user_id = input("🗑️ User to delete: ").strip()
    if db.remove(User.user_id == user_id):
        print(f"✅ User '{user_id}' deleted.")
    else:
        print("❌ User not found.")

def lock_unlock_user(lock=True):
    action = "Lock" if lock else "Unlock"
    user_id = input(f"{action} user ID: ").strip()
    updated = db.update({"locked": lock}, User.user_id == user_id)
    print(f"✅ {action}ed '{user_id}'" if updated else "❌ User not found.")

def reset_user():
    user_id = input("♻️ Reset user state for: ").strip()
    updated = db.update({
        "activated": False,
        "last_access": None,
        "last_ip": None,
        "locked": False
    }, User.user_id == user_id)
    print(f"✅ User '{user_id}' reset." if updated else "❌ User not found.")

def main():
    actions = {
        "1": ("View users", view_users),
        "2": ("Delete user", delete_user),
        "3": ("Lock user", lambda: lock_unlock_user(True)),
        "4": ("Unlock user", lambda: lock_unlock_user(False)),
        "5": ("Reset user", reset_user),
        "0": ("Exit", lambda: print("👋 Bye!"))
    }

    while True:
        print("\n🧙‍♂️ GhostAdmin Dashboard")
        for k, (label, _) in actions.items():
            print(f"{k}. {label}")
        choice = input("Choose action: ").strip()
        if choice == "0":
            break
        action = actions.get(choice)
        if action:
            action[1]()
        else:
            print("❓ Invalid option.")

if __name__ == "__main__":
    main()
