# Verifiable Credential Format for Pokemon Cards

This Flask app now supports Pokemon cards in **W3C Verifiable Credential** format, making it compatible with AnonCreds and other credential systems.

## Card Format

### Verifiable Credential Structure

```json
{
  "type": ["VerifiableCredential", "CardCredential"],
  "credentialSubject": {
    "type": ["PokemonCard", "CollectibleCard"],
    "cardId": "swsh12pt5-160",
    "cardSet": "swsh12pt5",
    "cardName": "Pikachu",
    "cardSupertype": "Pokémon",
    "cardSubtypes": ["Basic"],
    "cardTypes": ["Lightning"],
    "cardNumber": "160",
    "cardRarity": "Rare Secret",
    "cardImages": {
      "small": "https://images.pokemontcg.io/swsh12pt5/160.png",
      "large": "https://images.pokemontcg.io/swsh12pt5/160_hires.png"
    }
  }
}
```

## Field Mapping

| Old Format | VC Format (credentialSubject) | Description |
|------------|-------------------------------|-------------|
| `id` | `cardId` | Unique card identifier |
| `name` | `cardName` | Pokemon/Card name |
| `set` | `cardSet` | Set identifier |
| `supertype` | `cardSupertype` | Pokémon, Trainer, or Energy |
| `subtypes` | `cardSubtypes` | Array of subtypes |
| `types` | `cardTypes` | Pokemon types (Fire, Water, etc.) |
| `number` | `cardNumber` | Card number in set |
| `rarity` | `cardRarity` | Rarity level |
| `images` | `cardImages` | Object with small/large URLs |

## Converting Existing Cards

Use the provided conversion script:

```bash
# Convert the current cards.json to VC format
python convert_to_vc_format.py

# Or specify custom input/output files
python convert_to_vc_format.py input.json output.json
```

## Template Usage

The Jinja2 templates automatically extract card data from the `credentialSubject`:

```jinja
{% for card_vc in cards %}
  {{ render_card(card_vc) }}
{% endfor %}
```

The `render_card` macro handles extracting data from the VC structure:

```jinja
{% set card = vc.credentialSubject %}
<div class="card" data-id="{{ card.cardId }}">
  <img src="{{ card.cardImages.large }}" alt="{{ card.cardName }}">
</div>
```

## Benefits

- ✅ Compatible with AnonCreds/Hyperledger Indy
- ✅ W3C Verifiable Credentials standard
- ✅ Can add proofs, issuer, issuanceDate later
- ✅ Extensible for zero-knowledge proofs
- ✅ Works with credential wallets

## Future Enhancements

You can extend the VC format with additional fields:

```json
{
  "@context": ["https://www.w3.org/2018/credentials/v1"],
  "type": ["VerifiableCredential", "CardCredential"],
  "issuer": "did:example:card-issuer",
  "issuanceDate": "2024-10-18T00:00:00Z",
  "credentialSubject": {
    "id": "did:example:holder-123",
    "type": ["PokemonCard", "CollectibleCard"],
    "cardId": "swsh12pt5-160",
    ...
  },
  "proof": {
    "type": "AnonCredsSignature",
    ...
  }
}
```

## AnonCreds Integration

This format is ready for AnonCreds integration. You can:

1. Issue these as revocable credentials
2. Present proofs about card ownership
3. Use selective disclosure (only reveal certain attributes)
4. Implement the revocation roulette game with actual credentials!

