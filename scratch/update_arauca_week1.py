import json

path = r"e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\obras\Arauca 182\data.json"
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update Week 1 (index 0)
data["zones"][0]["tasks"][0] = "Preliminares Sótano"
data["zones"][0]["details"][0]["title"] = "Preliminares Sótano"

data["zones"][1]["tasks"][0] = "Preliminares Planta Baja"
data["zones"][1]["details"][0]["title"] = "Preliminares Planta Baja"

data["zones"][2]["tasks"][0] = "Preliminares Planta Alta"
data["zones"][2]["details"][0]["title"] = "Preliminares Planta Alta"

data["zones"][3]["tasks"][0] = "Preliminares Patio y Cochera"
data["zones"][3]["details"][0]["title"] = "Preliminares Patio y Cochera"

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated Week 1 for all zones in ARAUCA182")
