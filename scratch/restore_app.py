import os

def restore():
    path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'
    if not os.path.exists(path):
        print("File not found")
        return

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Restoration of launchApp (The version I accidentally broke)
    new_launch = """function launchApp() {
    if((session.role==='master' || session.role==='observer') && !currentObra) {
        if(session.obra) currentObra = OBRAS_CATALOG.find(o => o.id===session.obra) || OBRAS_CATALOG[0];
        else { showObraSelector(); return; }
    }
    if(!currentObra) currentObra = OBRAS_CATALOG[0];
    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('obraSelector').style.display = 'none';
    document.getElementById('appShell').style.display = 'block';
    const roleIcons = { master:'⚡ Master', observer:'👁 Supervisor', client:'🏠 Cliente' };
    document.getElementById('roleBadge').textContent = roleIcons[session.role] || session.role;
    document.getElementById('roleBadge').className = 'role-badge ' + session.role;
    document.getElementById('appSubtitle').textContent = (currentObra.name || 'Proyecto') + ' · v1.9.2';
    const heroImg = document.getElementById('obraHeroImg');
    if(currentObra.img && heroImg) {
        heroImg.src = currentObra.img;
        document.getElementById('obraHeroTitle').textContent = currentObra.name || '';
        document.getElementById('obraHeroSub').textContent = currentObra.location || '';
        document.getElementById('obraHeroWrap').style.display = 'block';
    }
    if(session.role === 'master') {
        document.getElementById('tabAccesos').style.display = '';
        if(typeof loadWeeklyNotes === 'function') loadWeeklyNotes();
    }
    buildWeekDots(); buildGanttTable(); updateDashboard();
}"""

    # Restoration of renderTareas (The version I accidentally broke)
    new_tareas = """function renderTareas() {
    const zones = projectData.map((d,i)=>({data:d,idx:i}));
    const canEdit = session.role==='master';
    const avgP = zones.length > 0 ? Math.round(zones.reduce((s,z)=>s+z.data.progress[currentWeek-1],0)/zones.length) : 0;
    document.getElementById('statsGrid').innerHTML=`
        <div class='stat-card animate-in'><div class='stat-value'>${currentWeek}</div><div class='stat-label'>Semana</div></div>
        <div class='stat-card animate-in'><div class='stat-value' style='color:#3b82f6'>${avgP}%</div><div class='stat-label'>Avance prom.</div></div>
        <div class='stat-card animate-in'><div class='stat-value' style='color:#10b981'>${currentWeek-1}</div><div class='stat-label'>Semanas comp.</div></div>
        <div class='stat-card animate-in'><div class='stat-value' style='color:#8b5cf6'>${TOTAL_WEEKS-currentWeek}</div><div class='stat-label'>Restantes</div></div>
    `;
    let html='';
    zones.forEach(({data:row,idx},i)=>{
        const taskName = row.tasks[currentWeek-1] || 'S/A';
        const prog = row.progress[currentWeek-1];
        const color = ZONE_COLORS[idx % ZONE_COLORS.length];
        const editHtml = canEdit ? `<div class='edit-slider-row' style='margin-top:12px;display:flex;justify-content:space-between;align-items:center;'><span style='font-size:0.7rem;color:#94a3b8;'>Ajustar:</span><div style='display:flex;gap:6px;'><button class='btn-prog' onclick='stepProgress(${idx},-5)'>-5%</button><button class='btn-prog' onclick='stepProgress(${idx},5)'>+5%</button></div></div>` : '';
        html+=`<div class='zone-card animate-in' style='animation-delay:${i*0.05}s;border-left:4px solid ${color};'>
            <div class='zone-card-header'><div class='zone-name-text'>${row.emoji} ${row.zone}</div><div class='zone-pct-badge' style='color:${color};background:${color}15'>${prog}%</div></div>
            <div class='task-chip' style='margin:8px 0;'>${taskName}</div>
            <div class='progress-bar-wrap'><div class='progress-track'><div class='progress-fill' style='width:${prog}%;background:linear-gradient(90deg,${color},${color}88)'></div></div></div>
            ${editHtml}<div id='gallery-${idx}' style='margin-top:10px;'></div></div>`;
    });
    document.getElementById('zoneCards').innerHTML=html;
    zones.forEach(({idx}) => { if(typeof loadFotosGallery === 'function') loadFotosGallery(idx, currentWeek, 'gallery-' + idx); });
}"""

    # Restoration of renderDetalle
    new_detalle = """function renderDetalle() {
    document.getElementById('detailTitle').textContent=`Semana ${currentWeek} · Detalle`;
    let html='';
    projectData.forEach((row,idx)=>{
        const color = ZONE_COLORS[idx % ZONE_COLORS.length];
        const weekDetail = (row.details && row.details[currentWeek-1]) || { desc: 'Sin descripción para esta semana.', subtasks: [] };
        const subtasksHtml = (weekDetail.subtasks || []).map(st => `
            <div class='subtask-item' style='display:flex; align-items:center; gap:8px; margin-top:6px; font-size:0.8rem; color:#cbd5e1;'>
                <div style='width:6px; height:6px; border-radius:50%; background:${color};'></div>
                ${st}
            </div>
        `).join('');
        html+=`
        <div class='detail-card animate-in' style='border-left:4px solid ${color}; margin-bottom:15px; padding:15px; background:rgba(255,255,255,0.02); border-radius:12px;'>
            <div style='font-weight:800; font-size:0.9rem; color:#f8fafc; margin-bottom:4px;'>${row.zone}</div>
            <div style='font-size:0.75rem; color:#94a3b8; margin-bottom:12px;'>${weekDetail.desc}</div>
            <div style='font-size:0.6rem; text-transform:uppercase; color:${color}; font-weight:900; letter-spacing:0.05em;'>Conceptos clave:</div>
            ${subtasksHtml || '<div style=\"font-size:0.7rem; color:#64748b; font-style:italic;\">No hay conceptos listados.</div>'}
        </div>`;
    });
    document.getElementById('detailCards').innerHTML=html;
}"""

    # We need to find where to inject these or replace the simplified ones
    import re
    # Replace launchApp
    content = re.sub(r'function launchApp\(\) \{.*?\}', new_launch, content, flags=re.DOTALL)
    # Replace renderTareas
    content = re.sub(r'function renderTareas\(\) \{.*?\}', new_tareas, content, flags=re.DOTALL)
    # Replace renderDetalle
    content = re.sub(r'function renderDetalle\(\) \{.*?\}', new_detalle, content, flags=re.DOTALL)
    # Fix corrupted version strings and footers
    content = content.replace('Ã‚Â·', '·').replace('Ã©', 'é').replace('Ã¡', 'á').replace('Ã³', 'ó').replace('Ãº', 'ú').replace('Ã±', 'ñ')
    content = content.replace('v1.9.1', 'v1.9.2')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Restoration successful")

if __name__ == "__main__":
    restore()
