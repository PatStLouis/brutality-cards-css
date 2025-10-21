#!/usr/bin/env python3
"""
Convert external image URLs in CSS files to inline data URLs.
This eliminates HTTP requests for texture/foil images.
"""

import os
import base64
import re
from pathlib import Path


def image_to_data_url(image_path):
    """Convert an image file to a data URL"""
    try:
        with open(image_path, 'rb') as f:
            img_bytes = f.read()
        
        # Determine mime type from extension
        ext = Path(image_path).suffix.lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(ext, 'image/png')
        
        # Create data URL
        base64_str = base64.b64encode(img_bytes).decode('utf-8')
        data_url = f"data:{mime_type};base64,{base64_str}"
        
        size_kb = len(img_bytes) / 1024
        print(f"  ✓ {Path(image_path).name} ({size_kb:.1f} KB)")
        
        return data_url
    except Exception as e:
        print(f"  ✗ Error converting {image_path}: {e}")
        return None


def process_css_file(css_path, img_base_dir):
    """Process a CSS file and replace url() references with data URLs"""
    
    print(f"\nProcessing: {css_path}")
    
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Find all url() references
    url_pattern = r'url\(["\']?(/img/[^)"\' ]+)["\']?\)'
    urls = re.findall(url_pattern, content)
    
    if not urls:
        print("  No /img/ URLs found")
        return
    
    print(f"  Found {len(urls)} image URLs")
    
    # Convert each unique URL
    converted = {}
    for url_path in set(urls):
        # Remove leading slash and construct full path
        rel_path = url_path.lstrip('/')
        full_path = os.path.join(img_base_dir, '..', rel_path)
        full_path = os.path.normpath(full_path)
        
        if os.path.exists(full_path):
            data_url = image_to_data_url(full_path)
            if data_url:
                converted[url_path] = data_url
        else:
            print(f"  ! File not found: {full_path}")
    
    # Replace URLs in content
    if converted:
        for url_path, data_url in converted.items():
            # Replace all instances of this URL
            content = re.sub(
                r'url\(["\']?' + re.escape(url_path) + r'["\']?\)',
                f'url("{data_url}")',
                content
            )
        
        # Write back
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Updated with {len(converted)} data URLs")
    else:
        print("  No URLs were converted")


def main():
    print("=" * 60)
    print("Converting CSS Image URLs to Data URLs")
    print("=" * 60)
    
    css_dir = Path("static/css")
    img_dir = Path("static/img")
    
    if not css_dir.exists():
        print(f"Error: CSS directory not found: {css_dir}")
        return
    
    if not img_dir.exists():
        print(f"Error: Image directory not found: {img_dir}")
        return
    
    # Find all CSS files
    css_files = list(css_dir.rglob("*.css"))
    print(f"\nFound {len(css_files)} CSS files")
    
    # Process each CSS file
    for css_file in css_files:
        process_css_file(css_file, img_dir)
    
    print("\n" + "=" * 60)
    print("Done! All CSS images have been inlined as data URLs")
    print("This eliminates HTTP requests for texture/foil images")
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

