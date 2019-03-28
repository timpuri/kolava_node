import sys

print("Running installer...")

try:
    import uasyncio
except ImportError:
    print("asyncio package not installed, installing")
    import upip
    upip.install(['micropython-uasyncio'])

print("Installer ready")