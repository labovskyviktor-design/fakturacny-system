import os
import binascii

files = [
    r"utils/fonts/DejaVuSans.ttf",
    r"utils/fonts/DejaVuSans-Bold.ttf"
]

for f in files:
    if os.path.exists(f):
        try:
            with open(f, "rb") as file:
                header = file.read(4)
                print(f"File: {f}")
                print(f"  Size: {os.path.getsize(f)} bytes")
                print(f"  Header (hex): {binascii.hexlify(header)}")
                print(f"  Header (raw): {header}")
                if header == b'\x00\x01\x00\x00' or header == b'OTTO':
                    print("  ✅ VALID TTF/OTF HEADER")
                else:
                    print("  ❌ INVALID HEADER")
        except Exception as e:
            print(f"Error reading {f}: {e}")
    else:
        print(f"File not found: {f}")
