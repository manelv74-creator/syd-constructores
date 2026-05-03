import json
import os

def create_project_data():
    project_id = "arauca182"
    project_name = "ARAUCA182"
    total_weeks = 60
    
    # Define zones and their tasks from budget
    # We will distribute them over the 60 weeks.
    # Obra Gris: Weeks 1-35
    # Acabados: Weeks 30-60
    
    zones_raw = [
        {
            "name": "Zona 1: Sótano",
            "emoji": "🏠",
            "obra_gris": ["Preliminares", "Muros de Contención", "Cimentación", "Albañilerías", "Losa", "Instalaciones Hidráulicas", "Instalaciones Sanitarias", "Instalaciones Pluviales", "Instalaciones Eléctricas", "Herrerías"],
            "acabados": ["Accesorios Eléctricos", "Recubrimientos y Pintura", "Cancelería", "Carpintería", "Muebles Sanitarios", "Herrería Final"]
        },
        {
            "name": "Zona 2: Planta Baja",
            "emoji": "🛋️",
            "obra_gris": ["Preliminares", "Cimentación", "Muros de Concreto", "Albañilerías", "Estructura de Acero", "Losa", "Instalaciones Hidráulicas/Sanitarias/Pluviales/Eléctricas", "Aire Acondicionado"],
            "acabados": ["Accesorios Eléctricos", "Recubrimientos y Pintura", "Cancelería", "Carpintería", "Muebles Sanitarios"]
        },
        {
            "name": "Zona 3: Planta Alta",
            "emoji": "🛏️",
            "obra_gris": ["Preliminares", "Muros de Concreto", "Estructura de Acero", "Albañilerías", "Albañilerías Azotea", "Losa", "Instalaciones Hidráulicas/Sanitarias/Pluviales/Eléctricas", "Aire Acondicionado"],
            "acabados": ["Accesorios Eléctricos", "Recubrimientos y Pintura", "Cancelería", "Carpintería", "Muebles Sanitarios", "Herrería"]
        },
        {
            "name": "Zona 4: Patio y Cochera",
            "emoji": "🚗",
            "obra_gris": ["Preliminares", "Muro Perimetral", "Albañilerías"],
            "acabados": ["Accesorios Eléctricos", "Recubrimientos y Pintura", "Jardinería", "Limpieza Final"]
        }
    ]
    
    zones = []
    for z_raw in zones_raw:
        tasks = [""] * total_weeks
        details = []
        
        # Distribute Obra Gris
        og_tasks = z_raw["obra_gris"]
        og_duration = 30
        for i in range(og_duration):
            task_idx = int((i / og_duration) * len(og_tasks))
            task_name = og_tasks[task_idx]
            tasks[i] = task_name
            details.append({
                "title": f"Obra Gris: {task_name}",
                "desc": f"Ejecución de trabajos de obra gris en {z_raw['name']} según presupuesto."
            })
            
        # Distribute Acabados
        ac_tasks = z_raw["acabados"]
        ac_start = 30
        ac_duration = 30
        for i in range(ac_duration):
            week_idx = ac_start + i
            if week_idx >= total_weeks: break
            task_idx = int((i / ac_duration) * len(ac_tasks))
            task_name = ac_tasks[task_idx]
            tasks[week_idx] = task_name
            details.append({
                "title": f"Acabados: {task_name}",
                "desc": f"Ejecución de acabados y detalles finales en {z_raw['name']}."
            })
            
        # Fill rest with S/A
        while len(details) < total_weeks:
            details.append({"title": "S/A", "desc": "Sin actividad programada para esta semana."})
            
        zones.append({
            "zone": z_raw["name"],
            "emoji": z_raw["emoji"],
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
    
    print(f"Created {output_path}")

create_project_data()
