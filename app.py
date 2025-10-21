from flask import Flask, render_template
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'brutality-holographic-cards-2024'

# Load card data (Verifiable Credential format)
# Each card is a VC with credentialSubject containing card data
def load_cards():
    """
    Load cards in W3C Verifiable Credential format:
    {
      "type": ["VerifiableCredential", "CardCredential"],
      "credentialSubject": {
        "type": ["BrutalityCard", "CollectibleCard"],
        "cardId": "...",
        "cardName": "...",
        "cardSet": "...",
        ...
      }
    }
    """
    with open('static/data/cards.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    """Display all Brutality cards - organized in template"""
    cards = load_cards()
    return render_template('index.jinja', cards=cards)

@app.route('/card/<card_id>')
def card_detail(card_id):
    """Display a single card (VC format)"""
    cards = load_cards()
    # Find card by cardId in credentialSubject
    card_vc = next((c for c in cards if c.get('credentialSubject', {}).get('cardId') == card_id), None)
    
    if not card_vc:
        return "Card not found", 404
    
    return render_template('card.jinja', card=card_vc)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

