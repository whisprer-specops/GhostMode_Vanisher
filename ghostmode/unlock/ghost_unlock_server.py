#!/usr/bin/env python3
from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import time
import smtplib
from email.message import EmailMessage
import secrets

app = Flask(__name__)
db = TinyDB("users.json")
User = Query()

API_KEY = "your-shared-secret"
EMAIL_NOTIFY = "you@example.com"
SMTP_SERVER = "localhost"
SMTP_PORT = 25

def send_unlock_email(user_id, ip):
    msg = EmailMessage()
    msg["Subject"] = f"✅ GhostMode Unlocked (Server): {user_id} [IP: {ip}]"
    msg["From"] = "ghostserver@localhost"
    msg["To"] = EMAIL_NOTIFY
    msg.set_content(f"User {user_id} unlocked GhostMode at {time.ctime()} from IP: {ip}")
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.send_message(msg)
    except Exception as e:
        print("📭 Email failed:", e)

@app.before_request
def verify_api_key():
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

@app.route("/unlock", methods=["POST"])
def unlock():
    data = request.json
    user_id = data.get("user_id")
    token = data.get("token")
    ip = request.remote_addr

    if not user_id:
        return jsonify({"status": "error", "message": "Missing user_id"}), 400

    record = db.get(User.user_id == user_id)
    if not record:
        return jsonify({"status": "error", "message": "User not found"}), 404

    if record.get("locked"):
        return jsonify({"status": "error", "message": "Account locked"}), 403

    if "token" in record and record["token"] and record["token"] != token:
        return jsonify({"status": "error", "message": "Invalid token"}), 403

    new_token = secrets.token_urlsafe(24)

    db.update({
        "last_access": time.time(),
        "last_ip": ip,
        "activated": True,
        "token": new_token
    }, User.user_id == user_id)

    send_unlock_email(user_id, ip)

return jsonify({
    "status": "ok",
    "password": record["password"],
    "new_token": new_token,
    "last_access": time.time(),
    "last_ip": ip,
    "message": "Unlock granted. New token issued."
})

@app.route("/status/<user_id>", methods=["GET"])
def status(user_id):
    record = db.get(User.user_id == user_id)
    if not record:
        return jsonify({"status": "error", "message": "User not found"}), 404
    return jsonify({
        "user_id": user_id,
        "activated": record.get("activated", False),
        "last_access": record.get("last_access"),
        "last_ip": record.get("last_ip"),
        "locked": record.get("locked", False)
    })

@app.route("/unlock_and_delete", methods=["POST"])
def unlock_and_delete():
    response = unlock()
    if response[1] == 200:
        try:
            if os.path.exists("ghostmode.7z"):
                os.remove("ghostmode.7z")
                return jsonify({"status": "ok", "message": "Unlocked and archive deleted."})
            else:
                return jsonify({"status": "ok", "message": "Unlocked. No archive to delete."})
        except Exception as e:
            return jsonify({"status": "error", "message": f"Unlock OK but delete failed: {e}"}), 500
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
