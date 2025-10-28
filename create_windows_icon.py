#!/usr/bin/env python3
"""
Convert PNG icon to Windows .ico format
Run this on Windows after cloning the repo
"""

from PIL import Image

# Open the PNG icon
img = Image.open('SDOH_icon.png')

# Create ICO with multiple sizes
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save('SDOH_icon.ico', format='ICO', sizes=icon_sizes)

print("✓ Created SDOH_icon.ico")
