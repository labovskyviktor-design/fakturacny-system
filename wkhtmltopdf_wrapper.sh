#!/bin/bash
# Wrapper pre wkhtmltopdf na Railway/Headless server
# Spúšťa generátor cez virtuálnu obrazovku (Xvfb)

# Hľadanie binárky wkhtmltopdf
WK_BIN=$(command -v wkhtmltopdf)

if [ -z "$WK_BIN" ]; then
    # Skúsime bežné Nix a Linux cesty
    for p in "/usr/bin/wkhtmltopdf" "/usr/local/bin/wkhtmltopdf" "/opt/bin/wkhtmltopdf" "/usr/bin/wkhtmltopdf-pack"; do
        if [ -f "$p" ]; then
            WK_BIN="$p"
            break
        fi
    done
fi

# Ak stále nič, skúsime nájsť v /nix/store (pomalšie, ale záchrana)
if [ -z "$WK_BIN" ]; then
    WK_BIN=$(find /usr /opt /nix/store -name wkhtmltopdf -type f -executable 2>/dev/null | head -n 1)
fi

if [ -z "$WK_BIN" ]; then
    echo "Error: wkhtmltopdf not found in PATH or standard locations." >&2
    exit 127
fi

if command -v xvfb-run > /dev/null 2>&1; then
    xvfb-run --server-args="-screen 0 1024x768x24" "$WK_BIN" "$@"
else
    "$WK_BIN" "$@"
fi
