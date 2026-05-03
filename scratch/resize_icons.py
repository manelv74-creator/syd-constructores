from PIL import Image
import os

def resize_icon(source_path, target_path, size):
    try:
        img = Image.open(source_path)
        
        # Create a solid white background (RGB, no transparency)
        new_img = Image.new("RGB", (size, size), (255, 255, 255))
        
        # Handle source image
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Resize maintaining aspect ratio
        img.thumbnail((size, size), Image.Resampling.LANCZOS)
        
        # Center the image on the solid white background
        x = (size - img.width) // 2
        y = (size - img.height) // 2
        
        # Paste using the image itself as a mask if it has an alpha channel
        new_img.paste(img, (x, y), img)
        
        new_img.save(target_path, "PNG") # Still PNG but solid RGB content
        print(f"Created {target_path} ({size}x{size}) - SOLID WHITE")
    except Exception as e:
        print(f"Error processing {source_path}: {e}")

assets_dir = r"e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\assets"
logo_path = os.path.join(assets_dir, "logo_syd.png")

if os.path.exists(logo_path):
    # Use new filenames to force cache refresh
    resize_icon(logo_path, os.path.join(assets_dir, "icon-solid-192.png"), 192)
    resize_icon(logo_path, os.path.join(assets_dir, "icon-solid-512.png"), 512)
else:
    print(f"Logo not found at {logo_path}")
