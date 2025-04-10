#!/bin/bash
# Randomize MAC address on Linux

IFACE="eth0"  # Change to correct interface

echo "[*] Current MAC: $(cat /sys/class/net/$IFACE/address)"
sudo ip link set dev "$IFACE" down
sudo macchanger -r "$IFACE"
sudo ip link set dev "$IFACE" up
echo "[+] MAC address randomized for $IFACE"
