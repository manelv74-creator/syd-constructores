import os

def clean_and_bump():
    files = {
        r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html': 'v1.9.3',
        r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\sw.js': 'v1.9.3'
    }

    corrections = {
        'Ã¢â€¢Â': '═',
        'Ã‚Â·': '·',
        'Ã©': 'é',
        'Ã¡': 'á',
        'Ã³': 'ó',
        'Ãº': 'ú',
        'Ã±': 'ñ',
        'Ã°Å¸â€”': '🗑️',
        'Ã°Å¸â€œâ€¦': '📅',
        'Ã¢Å¡â„¢Ã¯Â¸Â': '⚙️',
        'Ã¢Å“â€¦': '✅',
        'Ã°Å¸Â¤â€“': '🤖',
        'Ã°Å¸Å’': '🌐',
        'Ã¢â€ â€™': '→',
        'Ã°Å¸â€”â€˜Ã¯Â¸Â': '🗑️',
        'Ã¢Å¡Â¡': '⚡',
        'Ã°Å¸â€˜Â': '👁️',
        'Ã°Å¸Â Â': '🏠',
        'ÃƒÂ³': 'ó',
        'ÃƒÂ¡': 'á',
        'ÃƒÂ©': 'é',
        'ÃƒÂº': 'ú',
        'ÃƒÂ±': 'ñ',
        'ÃƒÂ': 'í'
    }

    for path, version in files.items():
        if not os.path.exists(path): continue
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Limpieza de mojibake
        for old, new in corrections.items():
            content = content.replace(old, new)
        
        # Bump Version
        content = content.replace('v1.9.2', version)
        content = content.replace('v1.9.1', version)
        content = content.replace('v1.9.0', version)
        
        # Force Cache update in sw.js
        if 'sw.js' in path:
            content = content.replace("CACHE_NAME = 'syd-app-v1.9.2'", f"CACHE_NAME = 'syd-app-{version}'")
            content = content.replace("CACHE_NAME = 'syd-app-v1.9.1'", f"CACHE_NAME = 'syd-app-{version}'")
            content = content.replace("CACHE_NAME = 'syd-app-v1.9.0'", f"CACHE_NAME = 'syd-app-{version}'")

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(path)} to {version}")

if __name__ == "__main__":
    clean_and_bump()
