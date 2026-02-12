import socket
import sys

regions = [
    "aws-0-eu-central-1.pooler.supabase.com",
    "aws-0-us-east-1.pooler.supabase.com",
    "aws-0-us-west-1.pooler.supabase.com",
    "aws-0-ap-southeast-1.pooler.supabase.com",
    "aws-0-sa-east-1.pooler.supabase.com",
]

print("Testing Supabase pooler resolution:")
found = False
for r in regions:
    try:
        ipv4 = socket.gethostbyname(r)
        print(f"[OK] {r} -> {ipv4}")
        found = True
    except Exception as e:
        print(f"[FAIL] {r} -> {e}")

if not found:
    sys.exit(1)
