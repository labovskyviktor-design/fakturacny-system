import requests
import os
import struct

FONTS = {
    "DejaVuSans.ttf": "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans.ttf",
    "DejaVuSans-Bold.ttf": "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans-Bold.ttf"
}

TARGET_DIR = os.path.join("utils", "fonts")
os.makedirs(TARGET_DIR, exist_ok=True)

def is_valid_ttf(path):
    try:
        with open(path, 'rb') as f:
            header = f.read(4)
            # TTF magic number is 0x00010000 or 'OTTO' for OpenType
            if header == b'\x00\x01\x00\x00' or header == b'OTTO':
                return True
            print(f"Invalid magic number: {header.hex()}")
            return False
    except Exception as e:
        print(f"Error checking file: {e}")
        return False

def download_font(name, url):
    print(f"Downloading {name} from {url}...")
    try:
        response = requests.get(url, allow_redirects=True, timeout=20)
        if response.status_code == 200:
            path = os.path.join(TARGET_DIR, name)
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"Saved to {path} ({len(response.content)} bytes)")
            
            if is_valid_ttf(path):
                print(f"✅ {name} verified as valid font.")
            else:
                print(f"❌ {name} is NOT a valid font file (likely HTML).")
                # Try raw.githubusercontent.com as backup
                return False
        else:
            print(f"Failed to download. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"Download error: {e}")
        return False
    return True

if __name__ == "__main__":
    for name, url in FONTS.items():
        if not download_font(name, url):
            # Backup URL check
            print(f"Retrying {name} with raw.githubusercontent.com...")
            backup_url = url.replace("github.com", "raw.githubusercontent.com").replace("/raw/", "/")
            download_font(name, backup_url)
