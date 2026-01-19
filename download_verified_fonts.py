import requests
import os
import io
import zipfile

# Stable source for DejaVu Sans
ZIP_URL = "https://www.fontsquirrel.com/fonts/download/dejavu-sans"

TARGET_DIR = os.path.join("utils", "fonts")
os.makedirs(TARGET_DIR, exist_ok=True)

def check_ttf_header(content):
    if len(content) < 4:
        return False
    header = content[:4]
    return header == b'\x00\x01\x00\x00' or header == b'OTTO'

def download_and_extract():
    print(f"Downloading ZIP from {ZIP_URL}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(ZIP_URL, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Failed to download zip. Status: {response.status_code}")
        else:
            print(f"  Downloaded {len(response.content)} bytes.")
            try:
                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    # List files to debug
                    print("  Zip contents:")
                    for info in z.infolist():
                        print(f"    - {info.filename}")
                        
                        target_name = None
                        # Check filename ignoring path
                        fname = os.path.basename(info.filename)
                        
                        if fname == "DejaVuSans.ttf":
                            target_name = "DejaVuSans.ttf"
                        elif fname == "DejaVuSans-Bold.ttf":
                            target_name = "DejaVuSans-Bold.ttf"
                        
                        if target_name:
                            print(f"  Found target: {fname}")
                            with z.open(info.filename) as source, open(os.path.join(TARGET_DIR, target_name), 'wb') as target:
                                content = source.read()
                                if check_ttf_header(content):
                                    target.write(content)
                                    print(f"  ✅ Extracted and valid: {target_name} ({len(content)} bytes)")
                                else:
                                    print(f"  ⚠️ Extracted file {target_name} invalid header")
            except zipfile.BadZipFile:
                print("❌ Downloaded content is not a valid zip file")

    except Exception as e:
        print(f"❌ Error during zip handling: {e}")

def try_raw_fallback():
    print("Trying raw GitHub fallback with verify=False...")
    urls = {
        "DejaVuSans.ttf": "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans.ttf",
        "DejaVuSans-Bold.ttf": "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans-Bold.ttf"
    }
    
    for name, url in urls.items():
        if os.path.exists(os.path.join(TARGET_DIR, name)):
            continue
            
        print(f"Downloading {name} from {url}...")
        try:
            r = requests.get(url, verify=False, timeout=20)
            if r.status_code == 200 and check_ttf_header(r.content):
                with open(os.path.join(TARGET_DIR, name), 'wb') as f:
                    f.write(r.content)
                print(f"  ✅ SUCCESS RAW: {name}")
            else:
                print(f"  ❌ Failed RAW: {r.status_code}")
        except Exception as e:
            print(f"  ❌ Error RAW: {e}")


if __name__ == "__main__":
    download_and_extract()
    try_raw_fallback()
    
    # Check if files exist
    files = ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]
    missing = [f for f in files if not os.path.exists(os.path.join(TARGET_DIR, f))]
    
    if not missing:
        print("All fonts ready.")
    else:
        print(f"Missing fonts: {missing}")
        # Copy regular to bold if just bold missing
        if "DejaVuSans-Bold.ttf" in missing and "DejaVuSans.ttf" not in missing:
             src = os.path.join(TARGET_DIR, "DejaVuSans.ttf")
             dst = os.path.join(TARGET_DIR, "DejaVuSans-Bold.ttf")
             with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
                 fdst.write(fsrc.read())
             print("Created fallback for Bold.")
