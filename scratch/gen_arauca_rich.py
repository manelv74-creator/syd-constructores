import json

def create_rich_project_data():
    project_id = "arauca182"
    project_name = "ARAUCA182"
    total_weeks = 60
    
    # Subtasks extracted from budget
    SUBTASKS_OG_SOTANO = ["A0101 Preliminares", "A0102 Muros de Contención", "A0103 Cimentación", "A0104 Albañilerías", "A0105 Losa", "A0106/7/8 Instalaciones H-S-P", "A0109/10 Eléctrica/Solares", "A0111/12 Cisterna/Pozo", "A0113 Herrerías", "A0114 Limpieza"]
    SUBTASKS_AC_SOTANO = ["B0101 Accesorios Eléctricos", "B0102 Tableros/Interrup.", "B0103 Recubrimientos/Pintura", "B0104 Cancelería", "B0105 Carpintería", "B0106 Muebles Sanitarios", "B0107 Herrería", "B0108 Limpieza"]
    
    SUBTASKS_OG_PB = ["A0201 Preliminares", "A0202 Cimentación", "A0203 Muros Concreto", "A0204 Albañilerías", "A0205 Estructura Acero", "A0206 Losa", "A0207/8/9 Instalaciones H-S-P", "A0210/11 Eléctrica/Aire Acond.", "A0213 Limpieza"]
    SUBTASKS_AC_PB = ["B0201 Accesorios Eléctricos", "B0202 Tablero/Interrup.", "B0203 Recubrimientos/Pintura", "B0204 Cancelería", "B0205 Carpintería", "B0206 Muebles Sanitarios", "B0207 Limpieza"]
    
    SUBTASKS_OG_PA = ["A0301 Preliminares", "A0302 Muros Concreto", "A0303 Estructura Acero", "A0304 Albañilerías", "A0305 Albañilerías Azotea", "A0306 Losa", "A0307/8/9 Instalaciones H-S-P", "A0310/11 Eléctrica/Aire Acond.", "A0314 Gas", "A0315 Limpieza"]
    SUBTASKS_AC_PA = ["B0301 Accesorios Eléctricos", "B0302 Interrup. Eléctricos", "B0303 Recubrimientos/Pintura", "B0304 Cancelería", "B0305 Carpintería", "B0306 Herrería", "B0307 Muebles Sanitarios", "B0308 Limpieza"]
    
    SUBTASKS_PATIO = ["C0101 Preliminares", "C0102 Muro Perimetral", "C0103 Albañilerías", "C0201 Accesorios Eléctricos", "C0203 Recubrimientos/Pintura", "C0204 Jardinería", "C0205 Limpieza"]

    # Timeline definitions
    # Sótano: W1-15 (OG), W30-50 (AC)
    # PB: W16-30 (OG), W40-55 (AC)
    # PA: W31-45 (OG), W45-60 (AC)
    # Patio: W10-25 (OG), W50-60 (AC)

    zones_config = [
        {
            "name": "Zona 1: Sótano", "emoji": "🏠",
            "og_range": (1, 15), "og_sub": SUBTASKS_OG_SOTANO,
            "ac_range": (30, 50), "ac_sub": SUBTASKS_AC_SOTANO
        },
        {
            "name": "Zona 2: Planta Baja", "emoji": "🛋️",
            "og_range": (16, 30), "og_sub": SUBTASKS_OG_PB,
            "ac_range": (40, 55), "ac_sub": SUBTASKS_AC_PB
        },
        {
            "name": "Zona 3: Planta Alta", "emoji": "🛏️",
            "og_range": (31, 45), "og_sub": SUBTASKS_OG_PA,
            "ac_range": (45, 60), "ac_sub": SUBTASKS_AC_PA
        },
        {
            "name": "Zona 4: Patio y Cochera", "emoji": "🚗",
            "og_range": (10, 25), "og_sub": SUBTASKS_PATIO[:3],
            "ac_range": (50, 60), "ac_sub": SUBTASKS_PATIO[3:]
        }
    ]

    zones = []
    for z in zones_config:
        tasks = ["S/A"] * total_weeks
        details = [{"title": "S/A", "desc": "Sin actividad programada", "subtasks": []} for _ in range(total_weeks)]
        
        # Fill OG
        start, end = z["og_range"]
        sub_list = z["og_sub"]
        duration = end - start + 1
        for i in range(duration):
            w_idx = start + i - 1
            st_idx = int((i / duration) * len(sub_list))
            main_t = sub_list[st_idx].split(" ", 1)[1] if " " in sub_list[st_idx] else sub_list[st_idx]
            tasks[w_idx] = main_t
            details[w_idx] = {
                "title": f"Obra Gris: {main_t}",
                "desc": f"Fase de obra gris y estructura en {z['name']}.",
                "subtasks": sub_list[max(0, st_idx-1):min(len(sub_list), st_idx+2)] # Show current, prev and next as context
            }
            
        # Fill AC
        start, end = z["ac_range"]
        sub_list = z["ac_sub"]
        duration = end - start + 1
        for i in range(duration):
            w_idx = start + i - 1
            st_idx = int((i / duration) * len(sub_list))
            main_t = sub_list[st_idx].split(" ", 1)[1] if " " in sub_list[st_idx] else sub_list[st_idx]
            tasks[w_idx] = main_t
            details[w_idx] = {
                "title": f"Acabados: {main_t}",
                "desc": f"Fase de acabados, instalaciones finales y detalles en {z['name']}.",
                "subtasks": sub_list[max(0, st_idx-1):min(len(sub_list), st_idx+2)]
            }
            
        zones.append({
            "zone": z["name"],
            "emoji": z["emoji"],
            "tasks": tasks,
            "details": details,
            "progress": [0] * total_weeks
        })

    data = {
        "obra_id": project_id,
        "obra_name": project_name,
        "obra_sub": "Residencial ARAUCA182",
        "hero_img": "obras/Arauca 182/Render Fachada.jpeg",
        "zones": zones
    }
    
    output_path = r"e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\obras\Arauca 182\data.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Created rich data at {output_path}")

create_rich_project_data()
