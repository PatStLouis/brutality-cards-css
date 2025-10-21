#!/usr/bin/env python3
"""Create a small demo with just 6 cards (all with data URLs)"""

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
        
        img = Image.open(BytesIO(response.content))
        
        if max_width and img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"    Resized to {max_width}x{new_height}")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        img_bytes = buffer.getvalue()
        
        base64_str = base64.b64encode(img_bytes).decode('utf-8')
        data_url = f"data:image/png;base64,{base64_str}"
        
        size_kb = len(img_bytes) / 1024
        print(f"    ✓ Converted ({size_kb:.1f} KB)")
        
        return data_url
        
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return None

print("Creating small demo with 6 cards...")
print()

# Load all cards
with open('static/data/cards.json', 'r') as f:
    all_cards = json.load(f)

# Take first 6 cards
cards = all_cards[:6]

print(f"Converting 6 cards to data URLs...\n")

for i, card_vc in enumerate(cards, 1):
    card = card_vc.get('credentialSubject', {})
    card_name = card.get('cardName', 'Unknown')
    card_id = card.get('cardId', 'Unknown')
    
    print(f"[{i}/6] {card_name} ({card_id})")
    
    images = card.get('cardImages', {})
    
    # Skip if already converted
    if 'large' in images and images['large'].startswith('data:'):
        print("    Already converted (data URL)")
        continue
    
    # Convert large image
    if 'large' in images and images['large'].startswith('http'):
        data_url = download_and_convert_to_data_url(images['large'], max_width=660)
        if data_url:
            images['large'] = data_url
            images['small'] = data_url
    
    time.sleep(0.3)

print(f"\nSaving small demo file...")
with open('static/data/cards_small.json', 'w') as f:
    json.dump(cards, f, indent=2)

import os
size_mb = os.path.getsize('static/data/cards_small.json') / (1024 * 1024)
print(f"✓ Done! Saved 6 cards to static/data/cards_small.json")
print(f"  File size: {size_mb:.2f} MB")
print(f"\nTo use: Rename cards_small.json to cards.json")

