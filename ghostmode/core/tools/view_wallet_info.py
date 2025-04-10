#!/usr/bin/env python3
import requests
import json
import os
import sys

RPC_URL = "http://127.0.0.1:18082/json_rpc"
HEADERS = {"Content-Type": "application/json"}

def rpc_request(method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": method
    }
    if params:
        payload["params"] = params

    try:
        response = requests.post(RPC_URL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()["result"]
    except Exception as e:
        print(f"[!] RPC error: {e}")
        return None

def get_wallet_info():
    print("🔍 Fetching wallet info...\n")
    info = rpc_request("get_balance")
    addr = rpc_request("get_address")
    status = rpc_request("get_height")

    if info and addr and status:
        print(f"📍 Address: {addr['address']}")
        print(f"💰 Balance: {info['balance'] / 1e12:.12f} XMR")
        print(f"🕒 Unlocked: {info['unlocked_balance'] / 1e12:.12f} XMR")
        print(f"📈 Blockchain height: {status['height']}")
    else:
        print("[!] Could not fetch all wallet details. Is monero-wallet-rpc running and wallet open?")

def main():
    print("GhostMode 🪙 Wallet Info Panel\n")
    if not shutil.which("monero-wallet-rpc"):
        print("[!] monero-wallet-rpc not found in PATH.")
        return
    get_wallet_info()

if __name__ == "__main__":
    import shutil
    main()
