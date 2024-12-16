from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path
import random

def create_gradient_image(width, height, color1, color2):
    """Create a gradient background."""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    for y in range(height):
        r = int(color1[0] * (1 - y/height) + color2[0] * (y/height))
        g = int(color1[1] * (1 - y/height) + color2[1] * (y/height))
        b = int(color1[2] * (1 - y/height) + color2[2] * (y/height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return image

def add_data_elements(image):
    """Add data visualization elements to the image."""
    draw = ImageDraw.Draw(image)

    # Add scatter plot points
    for _ in range(20):
        x = random.randint(50, 250)
        y = random.randint(50, 350)
        size = random.randint(4, 8)
        draw.ellipse([x-size, y-size, x+size, y+size], fill='white', outline='white')

    # Add bar chart
    bar_width = 30
    spacing = 20
    x_start = 500
    for i in range(4):
        height = random.randint(50, 150)
        x = x_start + (bar_width + spacing) * i
        y_bottom = 350
        draw.rectangle([x, y_bottom - height, x + bar_width, y_bottom],
                      fill='white', outline='white')

    # Add connecting lines
    for i in range(3):
        x1 = random.randint(300, 400)
        y1 = random.randint(100, 300)
        x2 = random.randint(400, 500)
        y2 = random.randint(100, 300)
        draw.line([x1, y1, x2, y2], fill='white', width=2)

    return image

def add_text(image, title, subtitle):
    """Add text to the image."""
    draw = ImageDraw.Draw(image)

    # Try to use a nice font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    # Add title
    draw.text((400, 100), title, font=title_font, fill='white', anchor="mm")
    # Add subtitle
    draw.text((400, 180), subtitle, font=subtitle_font, fill='white', anchor="mm")

    return image

def create_blog_images():
    """Create images for all blog posts."""
    # Ensure images directory exists
    Path('images').mkdir(exist_ok=True)

    # Image configurations
    configs = [
        {
            'filename': 'ml-oops-part3.jpg',
            'color1': (79, 70, 229),  # Indigo-600
            'color2': (129, 140, 248),  # Indigo-400
            'title': 'ML (O)Ops!',
            'subtitle': 'Part 3: What Data to Collect?'
        },
        {
            'filename': 'ml-oops-part2.jpg',
            'color1': (4, 120, 87),   # Dark green
            'color2': (52, 211, 153),  # Light green
            'title': 'ML (O)Ops!',
            'subtitle': 'Part 2: Tracking Changes'
        },
        {
            'filename': 'ml-oops-part1.jpg',
            'color1': (30, 64, 175),  # Dark blue
            'color2': (96, 165, 250),  # Light blue
            'title': 'ML (O)Ops!',
            'subtitle': 'Part 1: Deployment & Performance'
        }
    ]

    for config in configs:
        # Create base image with gradient
        img = create_gradient_image(800, 400, config['color1'], config['color2'])

        # Add data visualization elements
        img = add_data_elements(img)

        # Add text
        img = add_text(img, config['title'], config['subtitle'])

        # Save image
        output_path = os.path.join('images', config['filename'])
        img.save(output_path, quality=95)
        print(f"Generated {output_path}")

if __name__ == '__main__':
    create_blog_images()