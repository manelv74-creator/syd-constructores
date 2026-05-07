import os
import html

def sanitize_file():
    path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'
    sw_path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\sw.js'
    version = "v1.9.5"

    if not os.path.exists(path):
        print("File not found")
        return

    # 1. Leer el archivo intentando detectar la basura
    with open(path, 'rb') as f:
        content_bin = f.read()
    
    # Intentar decodificar lo mas limpio posible
    try:
        text = content_bin.decode('utf-8')
    except:
        text = content_bin.decode('latin-1')

    # 2. Diccionario de sanacion de basura (Mojibake)
    # Buscamos los patrones exactos de la captura de pantalla
    mojibake_fixes = {
        'Ã°Å¸Â Â': '&#x1F3E0;', # 🏠
        'Ã°Å¸â€˜Â': '&#x1F441;', # 👁️
        'Ã¢Å¡Â¡': '&#x26A1;',    # ⚡
        'Ã¢â‚¬Â¦': '...',
        'Ã¢â€ â€™': '&#x2192;',  # →
        'Ã°Å¸â€œÂ²': '&#x1F4F2;', # 📱
        'Ã°Å¸â€”â€˜Ã¯Â¸Â': '&#x1F5D1;', # 🗑️
        'Ã°Å¸â€œâ€¦': '&#x1F4C5;', # 📅
        'Ã¢Å¡â„¢Ã¯Â¸Â': '&#x2699;',    # ⚙️
        'Ã¢Å“â€¦': '&#x2705;',    # ✅
        'Ã°Å¸Â¤â€“': '&#x1F916;', # 🤖
        'Ã°Å¸Å’': '&#x1F310;',    # 🌐
        'ÃƒÂ³': '&oacute;',
        'ÃƒÂ¡': '&aacute;',
        'ÃƒÂ©': '&eacute;',
        'ÃƒÂº': '&uacute;',
        'ÃƒÂ±': '&ntilde;',
        'ÃƒÂ­': '&iacute;',
        'Ã³': '&oacute;',
        'Ã¡': '&aacute;',
        'Ã©': '&eacute;',
        'Ãº': '&uacute;',
        'Ã±': '&ntilde;',
        'Ã­': '&iacute;',
        'Ã‚Â·': '&middot;',
        'Ã°Å¸â€”': '&#x1F5D1;',
        'Ã¢â€¢Â': '&#x2550;'
    }

    for bad, good in mojibake_fixes.items():
        text = text.replace(bad, good)

    # 3. Sanacion de caracteres especiales restantes (Tildes y Emojis sueltos)
    # Convertimos cualquier caracter no-ASCII a su entidad HTML segura
    def char_to_entity(c):
        o = ord(c)
        if o > 127:
            return f'&#{o};'
        return c

    # Aplicamos a todo el archivo para blindarlo
    sanitized_text = "".join(char_to_entity(c) for c in text)

    # 4. Bump Version
    sanitized_text = sanitized_text.replace('v1.9.4', version)
    sanitized_text = sanitized_text.replace('v1.9.3', version)
    sanitized_text = sanitized_text.replace('v1.9.2', version)

    # 5. Guardar INDEX.HTML
    with open(path, 'w', encoding='utf-8') as f:
        f.write(sanitized_text)
    print(f"index.html sanitized and bumped to {version}")

    # 6. Guardar SW.JS
    if os.path.exists(sw_path):
        with open(sw_path, 'r', encoding='utf-8', errors='ignore') as f:
            sw_text = f.read()
        sw_text = sw_text.replace('v1.9.4', version)
        sw_text = sw_text.replace('v1.9.3', version)
        sw_text = sw_text.replace('syd-app-v1.9.4', f"syd-app-{version}")
        sw_text = sw_text.replace('syd-app-v1.9.3', f"syd-app-{version}")
        with open(sw_path, 'w', encoding='utf-8') as f:
            f.write(sw_text)
        print(f"sw.js sanitized and bumped to {version}")

if __name__ == "__main__":
    sanitize_file()
