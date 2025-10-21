# Pokemon Cards - Flask/Jinja2 Edition

A Flask + Jinja2 conversion of the Pokemon Cards CSS holographic effects showcase.

## Overview

This is a server-side rendered version of the Pokemon Cards holographic effects demo, originally built with Svelte by [@simeydotme](https://github.com/simeydotme/pokemon-cards-css).

## Features

- Display of 90+ Pokemon cards with various holographic effects
- Categories include:
  - Common & Uncommon cards
  - Reverse Holo
  - Regular Holofoil
  - Galaxy/Cosmos Holo
  - Amazing Rare
  - Radiant Holo
  - Pokemon V (Regular, Full Art, Alternate Art)
  - VMax (Regular and Rainbow)
  - VStar
  - Trainer Gallery
  - Rainbow Rare
  - Secret Rare (Gold)
  - Shiny Vault

- Interactive 3D hover effects using CSS transforms
- All holographic effects rendered with pure CSS

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements-flask.txt
```

## Running the App

```bash
python app.py
```

Then visit: http://localhost:5000

## Structure

```
pokemon-cards-css/
├── app.py                  # Main Flask application
├── templates/              # Jinja2 templates
│   ├── base.jinja         # Base layout
│   ├── index.jinja        # Main card listing page
│   └── components/
│       └── card.jinja     # Card component macro
├── static/                 # Static assets
│   ├── css/               # All CSS files (copied from original)
│   ├── data/              # cards.json data
│   ├── img/               # Card images and backgrounds
│   └── js/
│       └── cards.js       # Interactive card effects
```

## Credits

Original CSS effects and concept by [Simon Goellner (@simeydotme)](https://github.com/simeydotme)

Flask/Jinja2 conversion for educational purposes.

