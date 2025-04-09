#!/bin/bash

SIG_RESULT=$(python3 -c 'from unlock_guard_v2 import verify_sig; print(verify_sig()[1])')

zenity --info \
  --title="Unlock Signature Check" \
  --text="$SIG_RESULT"
