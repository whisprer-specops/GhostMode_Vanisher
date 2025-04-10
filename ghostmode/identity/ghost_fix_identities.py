    #!/usr/bin/env python3
    import os
    import json

    from pathlib import Path

    IDENTITY_DIR = Path.home() / ".ghost_identities"
    REQUIRED_FILES = ["metadata.json", "gpg-key.asc"]
    REQUIRED_DIRS = ["firefox-profile"]

    def validate_identity_folder(folder):
        issues = []
        for f in REQUIRED_FILES:
            if not (folder / f).exists():
                issues.append(f"❌ Missing required file: {f}")
        for d in REQUIRED_DIRS:
            if not (folder / d).exists():
                issues.append(f"❌ Missing required directory: {d}")
        return issues

    def scan_identities():
        print(f"🔍 Scanning identities in: {IDENTITY_DIR}")
        if not IDENTITY_DIR.exists():
            print("❌ Identity folder missing entirely.")
            return

        identities = [d for d in IDENTITY_DIR.iterdir() if d.is_dir()]
        if not identities:
            print("⚠️ No identity subfolders found.")
            return

        for ident in identities:
            print(f"
📂 Checking: {ident.name}")
            issues = validate_identity_folder(ident)
            if not issues:
                print("✅ OK")
            else:
                for issue in issues:
                    print(issue)

    if __name__ == "__main__":
        scan_identities()
