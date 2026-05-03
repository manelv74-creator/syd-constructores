from PIL import Image
import os

def resize_icon(source_path, target_path, size):
    try:
        img = Image.open(source_path)
        # Handle RGBA if necessary
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create a new image with white background if it's transparent? 
        # Actually, if the user said "fondo blanco", the logo probably has it or should have it.
        # Let's just resize it first.
        
        img.thumbnail((size, size), Image.Resampling.LANCZOS)
        
        # Create a square background
        new_img = Image.new("RGBA", (size, size), (255, 255, 255, 255))
        
        # Center the image
        x = (size - img.width) // 2
        y = (size - img.height) // 2
        new_img.paste(img, (x, y), img)
        
        new_img.save(target_path, "PNG")
        print(f"Created {target_path} ({size}x{size})")
    except Exception as e:
        print(f"Error processing {source_path}: {e}")

assets_dir = r"e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\assets"
logo_path = os.path.join(assets_dir, "logo_syd.png")

if os.path.exists(logo_path):
    resize_icon(logo_path, os.path.join(assets_dir, "icon-192.png"), 192)
    resize_icon(logo_path, os.path.join(assets_dir, "icon-512.png"), 512)
else:
    print(f"Logo not found at {logo_path}")
