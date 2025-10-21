#!/usr/bin/env python3
"""
Convert card image URLs to base64 data URLs.

This embeds the images directly in the JSON file as data URLs,
making the app work offline without external image dependencies.
"""

import json
import base64
import requests
from io import BytesIO
from PIL import Image
import sys
import time

def download_and_convert_to_data_url(url, max_width=None):
    """Download an image and convert it to a data URL"""
    try:
        print(f"  Downloading: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Open image
        img = Image.open(BytesIO(response.content))
        
        # Optionally resize to reduce file size
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

def convert_cards_to_data_urls(input_file, output_file, use_small=False, max_width=660):
    """Convert all card images to data URLs"""
    print(f"Loading cards from {input_file}...")
    with open(input_file, 'r') as f:
        cards = json.load(f)
    
    total_cards = len(cards)
    print(f"Found {total_cards} cards to process\n")
    
    for i, card_vc in enumerate(cards, 1):
        card = card_vc.get('credentialSubject', {})
        card_name = card.get('cardName', 'Unknown')
        card_id = card.get('cardId', 'Unknown')
        
        print(f"[{i}/{total_cards}] {card_name} ({card_id})")
        
        images = card.get('cardImages', {})
        
        # Convert large image
        if not use_small and 'large' in images and images['large'].startswith('http'):
            data_url = download_and_convert_to_data_url(images['large'], max_width=max_width)
            if data_url:
                images['large'] = data_url
                # Update small to same as large if requested
                images['small'] = data_url
        
        # Or convert small image
        elif use_small and 'small' in images and images['small'].startswith('http'):
            data_url = download_and_convert_to_data_url(images['small'], max_width=max_width)
            if data_url:
                images['small'] = data_url
                images['large'] = data_url
        
        # Rate limiting - be nice to the server
        if i < total_cards:
            time.sleep(0.5)
    
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(cards, f, indent=2)
    
    print(f"✓ Done! All {total_cards} cards converted to data URLs")
    
    # Calculate file size
    import os
    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"  Output file size: {size_mb:.2f} MB")

if __name__ == '__main__':
    input_file = 'static/data/cards.json'
    output_file = 'static/data/cards_with_data_urls.json'
    
    # Options
    use_small_images = '--small' in sys.argv  # Use small images instead of large
    max_width = 660  # Resize images to this width (660px is card width)
    
    if '--help' in sys.argv or '-h' in sys.argv:
        print("""
Usage: python convert_images_to_data_urls.py [OPTIONS]

Options:
  --small       Use small images instead of large (faster, smaller file)
  --width N     Maximum image width in pixels (default: 660)
  --help, -h    Show this help message

Examples:
  python convert_images_to_data_urls.py
  python convert_images_to_data_urls.py --small
  python convert_images_to_data_urls.py --width 400
        """)
        sys.exit(0)
    
    if '--width' in sys.argv:
        idx = sys.argv.index('--width')
        max_width = int(sys.argv[idx + 1])
    
    print("=" * 60)
    print("Pokemon Cards - Image to Data URL Converter")
    print("=" * 60)
    print(f"Settings:")
    print(f"  - Image source: {'small' if use_small_images else 'large'}")
    print(f"  - Max width: {max_width}px")
    print(f"  - Input: {input_file}")
    print(f"  - Output: {output_file}")
    print("=" * 60)
    print()
    
    try:
        convert_cards_to_data_urls(input_file, output_file, use_small_images, max_width)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Partial results may be saved.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)

