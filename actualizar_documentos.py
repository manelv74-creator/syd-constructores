import os
import json
import glob

def update_documentos():
    base_dir = r"e:/NEGOCIO/GUADALAJARA/PROYECTOS/Aplicacion SYD/obras"
    
    if not os.path.exists(base_dir):
        print(f"Error: No se encontró el directorio '{base_dir}'")
        return

    # Iterar sobre las carpetas de obras (e.g., obras/sauces)
    for obra_folder in os.listdir(base_dir):
        obra_path = os.path.join(base_dir, obra_folder)
        
        if not os.path.isdir(obra_path):
            continue
            
        data_json_path = os.path.join(obra_path, "data.json")
        docs_folder_path = os.path.join(obra_path, "Documentos")
        
        if not os.path.exists(data_json_path):
            print(f"Saltando {obra_folder}: No tiene data.json")
            continue
            
        # Leer el JSON actual
        try:
            with open(data_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error leyendo {data_json_path}: {e}")
            continue
            
        documentos = []
        
        # Buscar archivos en la carpeta Documentos
        if os.path.exists(docs_folder_path) and os.path.isdir(docs_folder_path):
            # Obtener todos los PDFs
            pdf_files = glob.glob(os.path.join(docs_folder_path, "*.pdf"))
            for pdf_file in pdf_files:
                filename = os.path.basename(pdf_file)
                # La ruta debe ser relativa desde la raíz web (donde está index.html)
                relative_path = f"obras/{obra_folder}/Documentos/{filename}"
                documentos.append({
                    "nombre": filename,
                    "ruta": relative_path
                })
        
        # Actualizar el json
        data["documentos"] = documentos
        
        # Guardar cambios
        try:
            with open(data_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Actualizado {obra_folder}: {len(documentos)} documento(s) encontrados.")
        except Exception as e:
            print(f"Error guardando {data_json_path}: {e}")

if __name__ == "__main__":
    print("Iniciando actualización de documentos...")
    update_documentos()
    print("Actualización completada.")
