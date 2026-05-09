import re

def bust_cache():
    path_index = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'

    with open(path_index, 'r', encoding='utf-8') as f:
        text = f.read()

    # Add cache buster to fetch calls
    text = text.replace("fetch('database/projects.json')", "fetch('database/projects.json?v=' + Date.now())")
    text = text.replace("fetch(obra.dataFile || `database/${obraId.toLowerCase()}.json`)", "fetch((obra.dataFile || `database/${obraId.toLowerCase()}.json`) + '?v=' + Date.now())")

    # Bump version
    text = text.replace('v2.1.1', 'v2.1.2')

    with open(path_index, 'w', encoding='utf-8') as f:
        f.write(text)

    print('Added cache busters to fetch requests and bumped to v2.1.2')

if __name__ == '__main__':
    bust_cache()
