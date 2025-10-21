#!/usr/bin/env python3
"""
Convert local card images to the proper JSON format with data URLs.
This will take the 3 uploaded cards and create entries for them.
"""

import json
import base64
import os
from PIL import Image
from io import BytesIO


def image_to_data_url(image_path, max_width=660):
    """Convert a local image file to a data URL"""
    try:
        print(f"  Processing: {image_path}")
        
        # Open and process image
        with Image.open(image_path) as img:
            # Resize if needed
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


def create_card_entry(card_id, card_name, image_path, card_type="Lightning", 
                      rarity="Rare Holo", supertype="Pokémon", subtypes=["Basic"]):
    """Create a card entry in the proper VC format with file path instead of data URL"""
    # Store the relative path from static directory
    rel_path = f"/img/cards/{os.path.basename(image_path)}"
    
    return {
        "type": [
            "VerifiableCredential",
            "CardCredential"
        ],
        "credentialSubject": {
            "type": [
                "BrutalityCard",
                "CollectibleCard"
            ],
            "cardId": card_id,
            "cardName": card_name,
            "cardSet": "brutality",
            "cardSupertype": supertype,
            "cardSubtypes": subtypes,
            "cardTypes": [card_type],
            "cardNumber": card_id.split("-")[-1],
            "cardRarity": rarity,
            "cardImages": {
                "large": rel_path
            }
        }
    }


def main():
    print("=" * 60)
    print("Brutality Cards - ALL EFFECTS SAMPLER")
    print("=" * 60)
    print()
    
    cards_dir = "static/img/cards"
    output_file = "static/data/cards.json"
    
    # Find all PNG files in the cards directory
    image_files = [f for f in os.listdir(cards_dir) if f.lower().endswith('.png')]
    image_files.sort()  # Sort for consistent ordering
    
    print(f"Found {len(image_files)} card images in {cards_dir}/")
    print()
    
    if not image_files:
        print("No PNG files found in static/img/cards/")
        return
    
    # All holographic effect configurations
    # Format: (effect_name, type, rarity, supertype, subtypes)
    effect_configs = [
        # Basic effects
        ("Common", "Lightning", "Common", "Pokémon", ["Basic"]),
        ("Uncommon", "Fire", "Uncommon", "Pokémon", ["Basic"]),
        
        # Reverse Holo
        ("Reverse Holo", "Water", "Rare", "Pokémon", ["Basic"]),
        
        # Standard Holo
        ("Holo Rare", "Lightning", "Rare Holo", "Pokémon", ["Basic"]),
        
        # Special Holos
        ("Cosmos Holo", "Psychic", "Rare Holo", "Pokémon", ["Basic"]),
        ("Amazing Rare", "Lightning", "Amazing Rare", "Pokémon", ["Basic"]),
        ("Radiant", "Fire", "Radiant Rare", "Pokémon", ["Basic"]),
        
        # Trainer Gallery
        ("Trainer Gallery Holo", "Lightning", "Rare Holo", "Pokémon", ["Basic"]),
        
        # V Cards
        ("V", "Lightning", "Rare Holo V", "Pokémon", ["Basic", "V"]),
        ("V Full Art", "Fire", "Rare Ultra", "Pokémon", ["Basic", "V"]),
        ("V Alt Art", "Water", "Rare Ultra", "Pokémon", ["Basic", "V"]),
        
        # VMAX Cards
        ("VMAX", "Lightning", "Rare Holo VMAX", "Pokémon", ["VMAX"]),
        ("VMAX Alt/Rainbow", "Fire", "Rare Rainbow", "Pokémon", ["VMAX"]),
        
        # VSTAR
        ("VSTAR", "Psychic", "Rare Holo VSTAR", "Pokémon", ["VSTAR"]),
        
        # Trainer Cards
        ("Trainer Full Art", "Colorless", "Rare Ultra", "Trainer", ["Supporter"]),
        
        # Rainbow & Gold
        ("Rainbow Rare VMAX", "Fire", "Rare Rainbow", "Pokémon", ["VMAX"]),
        ("Rainbow Rare VSTAR", "Lightning", "Rare Rainbow", "Pokémon", ["VSTAR"]),
        
        # Secret Rare (Gold) - different subtypes
        ("Secret Rare Gold Basic", "Metal", "Rare Secret", "Pokémon", ["Basic"]),
        ("Secret Rare Gold V", "Metal", "Rare Secret", "Pokémon", ["V"]),
        ("Secret Rare Gold VMAX", "Metal", "Rare Secret", "Pokémon", ["VMAX"]),
        
        # Trainer Gallery (V / VMax) - different subtypes
        ("Trainer Gallery V", "Lightning", "Rare Holo V", "Pokémon", ["V"]),
        ("Trainer Gallery VMAX", "Fire", "Rare Holo VMAX", "Pokémon", ["VMAX"]),
        
        # Shiny Vault (Basic / Stage 1 / V / VMax)
        ("Shiny Vault Basic", "Lightning", "Shiny Rare", "Pokémon", ["Basic"]),
        ("Shiny Vault Stage 1", "Water", "Shiny Rare", "Pokémon", ["Stage 1"]),
        ("Shiny Vault V", "Fire", "Shiny Rare", "Pokémon", ["V"]),
        ("Shiny Vault VMAX", "Psychic", "Shiny Rare", "Pokémon", ["VMAX"]),
    ]
    
    cards = []
    
    # Just collect image files - no conversion needed
    print("Found card images:\n")
    image_files_data = {}
    for i, image_file in enumerate(image_files):
        base_name = os.path.splitext(image_file)[0]
        image_path = os.path.join(cards_dir, image_file)
        image_files_data[image_file] = image_path
        print(f"  [{i+1}] {base_name}")
    
    # Create card entries - organized by EFFECT category first
    # Store file paths instead of data URLs
    print("\n" + "=" * 60)
    print("Creating card variations organized by effect category...")
    print("=" * 60 + "\n")
    
    card_counter = 1
    for effect_name, card_type, rarity, supertype, subtypes in effect_configs:
        print(f"Effect Category: {effect_name} ({rarity})")
        
        for image_file, image_path in image_files_data.items():
            base_name = os.path.splitext(image_file)[0]
            card_id = f"custom-{card_counter}"
            card_name = f"{base_name} ({effect_name})"
            
            card = create_card_entry(
                card_id=card_id,
                card_name=card_name,
                image_path=image_path,
                card_type=card_type,
                rarity=rarity,
                supertype=supertype,
                subtypes=subtypes
            )
            cards.append(card)
            print(f"  [{card_counter}] {base_name}")
            card_counter += 1
        
        print()
    
    # Save to JSON
    print("=" * 60)
    print(f"Saving {len(cards)} card variations to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(cards, f, indent=2)
    
    # Calculate file size
    size_kb = os.path.getsize(output_file) / 1024
    print(f"✓ Done! Saved {len(cards)} card variations")
    print(f"  ({len(image_files)} cards × {len(effect_configs)} effects)")
    print(f"  Output file: {output_file}")
    print(f"  File size: {size_kb:.1f} KB (paths only, no data URLs)")
    print()
    print("=" * 60)
    print("Card definitions saved with file paths!")
    print("Images will be served directly from /img/cards/")
    print("Start the Flask app to see all holographic effects!")
    print("=" * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()

