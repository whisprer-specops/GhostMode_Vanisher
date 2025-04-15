# Honeypots, Traps, and Tamper Detection

13. Audit Logging & GhostCloud

Audit logs (e.g., `ghost_audit.log`) record:
- Logins
- Unlocks
- Admin actions

Can sync to remote encrypted repo:
```bash
rclone copy ghost_audit.log remote:ghost_logs
```

Logs are optionally GPG-signed and auto-encrypted.