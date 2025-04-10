#!/usr/bin/env python3
import subprocess
import platform
import re
import random
import os
import sys

def generate_mac():
    return "02:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(*[random.randint(0x00, 0xff) for _ in range(5)])

def spoof_mac_linux(interface):
    new_mac = generate_mac()
    try:
        subprocess.run(["sudo", "ip", "link", "set", interface, "down"], check=True)
        subprocess.run(["sudo", "ip", "link", "set", interface, "address", new_mac], check=True)
        subprocess.run(["sudo", "ip", "link", "set", interface, "up"], check=True)
        print(f"[✓] MAC address for {interface} changed to {new_mac}")
    except subprocess.CalledProcessError:
        print(f"[!] Failed to spoof MAC address on {interface}")

def spoof_mac_windows(interface_name=None):
    try:
        import wmi
        c = wmi.WMI()
        adapters = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        for adapter in adapters:
            if interface_name is None or interface_name.lower() in adapter.Description.lower():
                new_mac = generate_mac().replace(':', '')
                adapter.SetMACAddress(new_mac)
                print(f"[✓] MAC address spoofed to {new_mac} on: {adapter.Description}")
                return
        print("[!] No matching network adapter found.")
    except ImportError:
        print("[!] 'wmi' module required. Install with: pip install wmi")

def main():
    if platform.system() == "Linux":
        iface = input("Enter network interface (e.g. eth0, wlan0): ")
        spoof_mac_linux(iface)
    elif platform.system() == "Windows":
        iface = input("Enter part of network adapter name (or press enter for first match): ")
        spoof_mac_windows(iface if iface else None)
    else:
        print("[!] Platform not supported")

if __name__ == "__main__":
    main()
