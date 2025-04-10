# tools/qr_generator.py

import qrcode
import sys

def generate_qr(data, output="qr_output.png"):
    img = qrcode.make(data)
    img.save(output)
    print(f"[QR] Saved to: {output}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qr_generator.py 'your data here'")
    else:
        generate_qr(sys.argv[1])
