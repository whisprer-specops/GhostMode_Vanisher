#!/usr/bin/env python3
from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import time

app = Flask(__name__)
db = TinyDB("users.json")
User = Query()

API_KEY = "your-shared-secret"

def auth_fail():
    return jsonify({"status": "error", "message": "Unauthorized"}), 403

@app.before_request
def check_api_key():
    if request.headers.get("X-API-Key") != API_KEY:
        return auth_fail()

@app.route("/admin/users", methods=["GET"])
def list_users():
    users = db.all()
    for u in users:
        u["last_access_str"] = time.ctime(u["last_access"]) if u.get("last_access") else "Never"
    return jsonify({"status": "ok", "users": users})

@app.route("/admin/add", methods=["POST"])
def add_user():
    data = request.json
    user_id = data.get("user_id")
    password = data.get("password")
    token = data.get("token", None)

    if db.contains(User.user_id == user_id):
        return jsonify({"status": "error", "message": "User exists"}), 409

    record = {
        "user_id": user_id,
        "password": password,
        "token": token,
        "locked": False,
        "activated": False,
        "last_ip": None,
        "last_access": None
    }
    db.insert(record)
    return jsonify({"status": "ok", "message": f"User {user_id} added."})

@app.route("/admin/lock", methods=["POST"])
def lock_user():
    data = request.json
    user_id = data.get("user_id")
    result = db.update({"locked": True}, User.user_id == user_id)
    return jsonify({"status": "ok" if result else "error", "message": "User locked" if result else "User not found"})

@app.route("/admin/unlock", methods=["POST"])
def unlock_user():
    data = request.json
    user_id = data.get("user_id")
    result = db.update({"locked": False}, User.user_id == user_id)
    return jsonify({"status": "ok" if result else "error", "message": "User unlocked" if result else "User not found"})

@app.route("/admin/reset", methods=["POST"])
def reset_user():
    data = request.json
    user_id = data.get("user_id")
    result = db.update({
        "activated": False,
        "last_ip": None,
        "last_access": None,
        "locked": False
    }, User.user_id == user_id)
    return jsonify({"status": "ok" if result else "error", "message": "User reset" if result else "User not found"})

@app.route("/admin/delete", methods=["DELETE"])
def delete_user():
    data = request.json
    user_id = data.get("user_id")
    result = db.remove(User.user_id == user_id)
    return jsonify({"status": "ok" if result else "error", "message": "User deleted" if result else "User not found"})

audit_patch_code = '''# == AUDIT LOGGING ==
from datetime import datetime
from flask import g
AUDIT_LOG_PATH = "audit_log.jsonl"

def log_audit_event(event_type, user_id, detail=None):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": event_type,
        "user_id": user_id,
        "ip": request.remote_addr,
        "detail": detail or {}
    }
    with open(AUDIT_LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\\n")

@app.route("/audit", methods=["POST"])
def receive_audit_log():
    try:
        log = request.get_json(force=True)
        log["received"] = datetime.utcnow().isoformat() + "Z"
        log["ip"] = request.remote_addr
        with open(AUDIT_LOG_PATH, "a") as f:
            f.write(json.dumps(log) + "\\n")
        return jsonify({"status": "ok", "logged": True})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
'''

# Append patch code to existing ghost_admin_server.py (if it exists)
admin_api_path = Path("/mnt/data/ghost_admin_server.py")
if admin_api_path.exists():
    existing_code = admin_api_path.read_text()
    if "# == AUDIT LOGGING ==" not in existing_code:
        updated_code = existing_code + "\n\n" + audit_patch_code
        admin_api_path.write_text(updated_code)
        result = "✅ Patched /audit into ghost_admin_server.py"
    else:
        result = "⚠️ Audit endpoint already exists in ghost_admin_server.py"
else:
    result = "❌ ghost_admin_server.py not found in /mnt/data"

result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
