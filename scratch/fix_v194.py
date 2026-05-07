import os

def solve():
    path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'
    sw_path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\sw.js'
    
    # 1. FIX INDEX.HTML
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

        replacements = {
            'Ã°Å¸Â Â': '🏠',
            'Ã°Å¸â€˜Â': '👁️',
            'Ã¢Å¡Â¡': '⚡',
            'Ã¢â‚¬Â¦': '...',
            'Ã¢â€ â€™': '→',
            'Ã°Å¸â€œÂ²': '📱',
            'Ã°Å¸â€”â€˜Ã¯Â¸Â': '🗑️',
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
            'ÃƒÂ­': 'í',
            'Ã³': 'ó',
            'Ã¡': 'á',
            'Ã©': 'é',
            'Ãº': 'ú',
            'Ã±': 'ñ',
            'Ã­': 'í',
            'Ã‚Â·': '·',
            'Ã°Å¸â€”': '🗑️',
            'Ã¢â€¢Â': '═',
            'ÃƒÂ­': 'í',
            'ÃƒÂ±': 'ñ'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Bump version to 1.9.4
        text = text.replace('v1.9.3', 'v1.9.4')
        text = text.replace('v1.9.2', 'v1.9.4')
        text = text.replace('v1.9.1', 'v1.9.4')

        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print("index.html fixed to v1.9.4")

    # 2. FIX SW.JS
    if os.path.exists(sw_path):
        with open(sw_path, 'r', encoding='utf-8', errors='ignore') as f:
            sw_text = f.read()
        
        sw_text = sw_text.replace('v1.9.3', 'v1.9.4')
        sw_text = sw_text.replace('v1.9.2', 'v1.9.4')
        sw_text = sw_text.replace('v1.9.1', 'v1.9.4')
        sw_text = sw_text.replace('syd-app-v1.9.3', 'syd-app-v1.9.4')
        sw_text = sw_text.replace('syd-app-v1.9.2', 'syd-app-v1.9.4')

        with open(sw_path, 'w', encoding='utf-8') as f:
            f.write(sw_text)
        print("sw.js fixed to v1.9.4")

if __name__ == "__main__":
    solve()
