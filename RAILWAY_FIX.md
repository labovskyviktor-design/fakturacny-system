# Critical Fix for Railway PDF Generation

## Problem
Railway still cannot find `libgobject-2.0-0` even with previous fixes.

## Root Cause
Missing `gobject-introspection` and `pkg-config` packages in nixpacks.toml.

## Solution Applied

### 1. Added Missing Packages to nixpacks.toml
- `pkg-config` - Helps find library paths
- `gobject-introspection` - Provides GObject library bindings

### 2. Enhanced Environment Variables
- Added `PKG_CONFIG_PATH` to help ctypes locate libraries
- Enhanced `LD_LIBRARY_PATH` with wildcard paths for Nix store

## Deploy Now

```bash
git add nixpacks.toml
git commit -m "Fix: Add gobject-introspection and pkg-config for Railway"
git push origin main
```

## Why This Works

WeasyPrint uses `ctypes.util.find_library()` to locate system libraries. In Nix environments, this requires:
1. **pkg-config** - To query library locations
2. **gobject-introspection** - To provide GObject library metadata
3. **PKG_CONFIG_PATH** - Environment variable pointing to .pc files

Without these, Python's ctypes cannot find libgobject-2.0-0 even though it's installed.

## Expected Result

After deployment, PDF generation should work without the "cannot load library" error.
