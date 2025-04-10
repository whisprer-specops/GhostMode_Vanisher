#!/bin/bash
echo "🛠️ Running GhostMode post-install hook..."

# Fix identities
if command -v python3 >/dev/null && [[ -f /usr/local/bin/ghost_fix_identities.py ]]; then
  python3 /usr/local/bin/ghost_fix_identities.py
fi

# Create default log entry
mkdir -p "$HOME/.ghostmode"
echo "GhostMode installed on $(date)" >> "$HOME/.ghostmode/ghost_audit.log"

# Optional first-use launch of wizard
if [[ ! -d $HOME/.ghost_identities ]] || [[ -z "$(ls -A $HOME/.ghost_identities)" ]]; then
  if [[ -f /usr/local/bin/tools/identity_wizard_gui.py ]]; then
    python3 /usr/local/bin/tools/identity_wizard_gui.py &
  fi
fi

echo "✅ Post-install complete."
