#!/usr/bin/env python3
"""
Convert Pokemon cards from simple format to W3C Verifiable Credential format.

Old format:
{
  "id": "swsh12pt5-160",
  "name": "Pikachu",
  "set": "swsh12pt5",
  ...
}

New format:
{
  "type": ["VerifiableCredential", "CardCredential"],
  "credentialSubject": {
    "type": ["PokemonCard", "CollectibleCard"],
    "cardId": "swsh12pt5-160",
    "cardName": "Pikachu",
    "cardSet": "swsh12pt5",
    ...
  }
}
"""

import json
import sys

def convert_card_to_vc(card):
    """Convert a single card to Verifiable Credential format"""
    return {
        "type": ["VerifiableCredential", "CardCredential"],
        "credentialSubject": {
            "type": ["PokemonCard", "CollectibleCard"],
            "cardId": card.get("id"),
            "cardName": card.get("name"),
            "cardSet": card.get("set"),
            "cardSupertype": card.get("supertype"),
            "cardSubtypes": card.get("subtypes", []),
            "cardTypes": card.get("types", []),
            "cardNumber": card.get("number"),
            "cardRarity": card.get("rarity"),
            "cardImages": card.get("images", {})
        }
    }

def convert_cards_file(input_file, output_file):
    """Convert entire cards.json file to VC format"""
    with open(input_file, 'r') as f:
        cards = json.load(f)
    
    vc_cards = [convert_card_to_vc(card) for card in cards]
    
    with open(output_file, 'w') as f:
        json.dump(vc_cards, f, indent=2)
    
    print(f"✓ Converted {len(vc_cards)} cards from {input_file} to {output_file}")
    print(f"  Format: W3C Verifiable Credential with credentialSubject")

if __name__ == '__main__':
    input_file = 'static/data/cards.json'
    output_file = 'static/data/cards_vc.json'
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    convert_cards_file(input_file, output_file)

