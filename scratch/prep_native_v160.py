import os

def prep():
    path_index = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'
    sw_path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\sw.js'
    version = 'v2.1.0'

    # Read native v1.6.0 index.html
    with open(path_index, 'r', encoding='utf-8') as f:
        content = f.read()

    # Bump versions
    content = content.replace('v1.6.0', version)
    content = content.replace('v1.5.2', version)

    # Clean legacy mojibake just in case
    corrections = {
        'Ã°Å¸Â Â': '🏠', 'Ã°Å¸â€˜Â': '👁️', 'Ã¢Å¡Â¡': '⚡', 'Ã¢â‚¬Â¦': '...', 'Ã¢â€ â€™': '→',
        'Ã°Å¸â€œÂ²': '📱', 'Ã°Å¸â€”â€˜Ã¯Â¸Â': '🗑️', 'Ã°Å¸â€œâ€¦': '📅', 'Ã¢Å¡â„¢Ã¯Â¸Â': '⚙️',
        'Ã¢Å“â€¦': '✅', 'Ã°Å¸Â¤â€“': '🤖', 'Ã°Å¸Å’': '🌐', 'ÃƒÂ³': 'ó', 'ÃƒÂ¡': 'á',
        'ÃƒÂ©': 'é', 'ÃƒÂº': 'ú', 'ÃƒÂ±': 'ñ', 'ÃƒÂ­': 'í', 'Ã³': 'ó', 'Ã¡': 'á',
        'Ã©': 'é', 'Ãº': 'ú', 'Ã±': 'ñ', 'Ã­': 'í', 'Ã‚Â·': '·', 'Ã¢â€¢Â': '═'
    }
    for old, new in corrections.items():
        content = content.replace(old, new)

    # Save
    with open(path_index, 'w', encoding='utf-8') as f:
        f.write(content)

    # Read sw.js
    if os.path.exists(sw_path):
        with open(sw_path, 'r', encoding='utf-8') as f:
            sw_text = f.read()
        
        sw_text = sw_text.replace('v1.6.0', version)
        sw_text = sw_text.replace('v1.5.2', version)
        sw_text = sw_text.replace('syd-app-v1.6.0', f'syd-app-{version}')
        
        with open(sw_path, 'w', encoding='utf-8') as f:
            f.write(sw_text)

    print('Native v1.6.0 prepared and bumped to v2.1.0')

if __name__ == '__main__':
    prep()
