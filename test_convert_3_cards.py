#!/usr/bin/env python3
"""Test conversion of first 3 cards to data URLs"""

import json
import base64
import requests
from io import BytesIO
from PIL import Image
import time

def download_and_convert_to_data_url(url, max_width=660):
    """Download an image and convert it to a data URL"""
    try:
        print(f"  Downloading: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Open image
        img = Image.open(BytesIO(response.content))
        
        # Resize to reduce file size
        if max_width and img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"    Resized to {max_width}x{new_height}")
        
        # Convert to PNG and base64
        buffer = BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        img_bytes = buffer.getvalue()
        
        # Create data URL
        base64_str = base64.b64encode(img_bytes).decode('utf-8')
        data_url = f"data:image/png;base64,{base64_str}"
        
        size_kb = len(img_bytes) / 1024
        print(f"    ✓ Converted ({size_kb:.1f} KB)")
        
        return data_url
        
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return None

# Load cards
print("Loading cards...")
with open('static/data/cards.json', 'r') as f:
    cards = json.load(f)

print(f"Found {len(cards)} cards total\n")
print("Converting first 3 cards as test...\n")

# Convert only first 3 cards
for i in range(min(3, len(cards))):
    card_vc = cards[i]
    card = card_vc.get('credentialSubject', {})
    card_name = card.get('cardName', 'Unknown')
    card_id = card.get('cardId', 'Unknown')
    
    print(f"[{i+1}/3] {card_name} ({card_id})")
    
    images = card.get('cardImages', {})
    
    # Convert large image
    if 'large' in images and images['large'].startswith('http'):
        data_url = download_and_convert_to_data_url(images['large'], max_width=660)
        if data_url:
            images['large'] = data_url
            images['small'] = data_url
    
    time.sleep(0.5)

print(f"\nSaving test file...")
with open('static/data/cards_test.json', 'w') as f:
    json.dump(cards, f, indent=2)

print(f"✓ Done! Saved to static/data/cards_test.json")
print(f"\nTo test: Rename cards_test.json to cards.json")

