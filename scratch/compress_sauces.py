import os
import json

def compress_schedule():
    projects_path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\database\projects.json'
    sauces_data_path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\obras\sauces\data.json'
    
    NEW_WEEKS = 20
    OLD_WEEKS = 32

    # 1. Update projects.json
    with open(projects_path, 'r', encoding='utf-8') as f:
        projects = json.load(f)
    
    for p in projects:
        if p['id'] == 'sauces':
            p['totalSemanas'] = NEW_WEEKS
            
    with open(projects_path, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)

    # 2. Update sauces data.json
    with open(sauces_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for zone in data['zones']:
        new_tasks = [""] * NEW_WEEKS
        new_details = [{"title": "S/A", "desc": "Sin actividad programada para esta semana."} for _ in range(NEW_WEEKS)]
        new_progress = [0] * NEW_WEEKS

        for old_i in range(OLD_WEEKS):
            # Map old week index to new week index proportionally
            new_i = min(int(old_i * (NEW_WEEKS / OLD_WEEKS)), NEW_WEEKS - 1)
            
            # Tasks: if there's a task, put it in the new slot. 
            # If slot already has a task, append it if it's different.
            old_task = zone['tasks'][old_i]
            if old_task:
                if not new_tasks[new_i]:
                    new_tasks[new_i] = old_task
                elif old_task not in new_tasks[new_i]:
                    new_tasks[new_i] += " / " + old_task

            # Details: merge titles and descriptions
            old_detail = zone['details'][old_i]
            if old_detail['title'] != "S/A":
                if new_details[new_i]['title'] == "S/A":
                    new_details[new_i] = old_detail.copy()
                elif old_detail['title'] not in new_details[new_i]['title']:
                    new_details[new_i]['title'] += " / " + old_detail['title']
                    new_details[new_i]['desc'] += " " + old_detail['desc']

            # Progress: keep the max progress for that mapped week
            new_progress[new_i] = max(new_progress[new_i], zone['progress'][old_i])

        zone['tasks'] = new_tasks
        zone['details'] = new_details
        zone['progress'] = new_progress

    with open(sauces_data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Compressed Sauces schedule from {OLD_WEEKS} to {NEW_WEEKS} weeks successfully.")

if __name__ == '__main__':
    compress_schedule()
