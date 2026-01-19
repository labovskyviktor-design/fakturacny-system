#!/usr/bin/env python3
"""
Startup diagnostic script for PDF generation environment.
Run this on Railway to verify all dependencies are correctly configured.
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 70)
    print("PDF GENERATION ENVIRONMENT DIAGNOSTIC")
    print("=" * 70)
    print()
    
    # Import and run diagnostics
    try:
        from utils.pdf_diagnostics import log_diagnostics
        success, diagnostics = log_diagnostics()
        
        print()
        if success:
            print("[OK] All checks passed! PDF generation should work.")
            return 0
        else:
            print("[FAIL] Some checks failed. Review errors above.")
            print()
            print("Common fixes:")
            print("  1. Ensure nixpacks.toml includes all required packages")
            print("  2. Check that LD_LIBRARY_PATH is set correctly")
            print("  3. Verify fonts are installed (dejavu_fonts, liberation_ttf)")
            return 1
            
    except Exception as e:
        print(f"[ERROR] Diagnostic script failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
