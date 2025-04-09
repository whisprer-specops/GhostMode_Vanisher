Requires: sudo apt install qrencode

📸 Then you can:

View the QR code fullscreen (feh, eog, or Qt image viewer)

---

Scan with webcam from hot machine using zbarcam or your smartOn the hot (online) machine:
Use webcam to decode the QR:

bash
Copy
Edit
sudo apt install zbar-tools
zbarcam
It’ll show you the scanned token like:

ruby
Copy
Edit
QR-Code:token-abc123xyz-unlock
Then you paste that token into your unlocker.phone