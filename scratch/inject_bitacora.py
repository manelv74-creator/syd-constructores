import re

def inject_bitacora():
    path = r'e:\NEGOCIO\GUADALAJARA\PROYECTOS\Aplicacion SYD\index.html'
    
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # ═══════════════════════════════════════════
    # 1. ADD TAB BUTTON (after Accesos tab)
    # ═══════════════════════════════════════════
    tab_btn = '    <button class="tab-btn" id="tabBitacora" style="display:none" onclick="switchTab(\'bitacora\',this)">&#x1F4DD; Bit\u00e1cora</button>\n'
    
    if 'tabBitacora' not in html:
        html = html.replace(
            '<button class="tab-btn" id="tabAccesos"',
            tab_btn + '    <button class="tab-btn" id="tabAccesos"'
        )
        print("[OK] Tab button injected")

    # ═══════════════════════════════════════════
    # 2. ADD VIEW HTML (before </main>)
    # ═══════════════════════════════════════════
    bitacora_view = '''    <div class="view" id="view-bitacora">
        <!-- BITACORA DE OBRA - Solo Master -->
        <div style="margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                <div>
                    <div style="font-size:1.1rem; font-weight:800; color:#fff; display:flex; align-items:center; gap:8px;">
                        \U0001F4D3 Bit\u00e1cora de Obra
                    </div>
                    <div style="font-size:0.72rem; color:var(--muted); margin-top:4px;">
                        <span id="bitacoraObraName"></span> \u00b7 <span id="bitacoraSemanaLabel">Semana 1</span>
                    </div>
                </div>
                <div id="bitacoraNotaCount" style="background:rgba(59,130,246,0.2); color:#93c5fd; padding:4px 12px; border-radius:20px; font-size:0.72rem; font-weight:700;">0 notas</div>
            </div>

            <!-- Selector de semana -->
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:16px;">
                <button onclick="changeBitacoraSemana(-1)" style="width:36px; height:36px; border-radius:50%; border:1px solid var(--border); background:rgba(255,255,255,0.06); color:var(--text); font-size:1.1rem; cursor:pointer; display:flex; align-items:center; justify-content:center;">\u25c0</button>
                <div style="flex:1; text-align:center;">
                    <span id="bitacoraWeekDisplay" style="font-size:1.2rem; font-weight:800; color:var(--accent2);">Semana 1</span>
                </div>
                <button onclick="changeBitacoraSemana(1)" style="width:36px; height:36px; border-radius:50%; border:1px solid var(--border); background:rgba(255,255,255,0.06); color:var(--text); font-size:1.1rem; cursor:pointer; display:flex; align-items:center; justify-content:center;">\u25b6</button>
            </div>

            <!-- Input de nota -->
            <div style="background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:14px; margin-bottom:16px;">
                <textarea id="bitacoraInput" rows="3" placeholder="Escribe una nota sobre el avance de la obra..." style="width:100%; background:transparent; border:none; color:#fff; font-family:Inter,sans-serif; font-size:0.85rem; resize:vertical; outline:none; line-height:1.5;"></textarea>
                <div style="display:flex; gap:8px; margin-top:10px;">
                    <button onclick="guardarNotaBitacora()" style="flex:1; background:linear-gradient(135deg,#3b82f6,#8b5cf6); color:#fff; border:none; padding:10px; border-radius:12px; font-weight:700; font-size:0.82rem; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px;">
                        \u2795 Guardar Nota
                    </button>
                    <button onclick="dictarNotaBitacora()" id="btnDictarBitacora" style="background:rgba(255,255,255,0.08); color:#fff; border:1px solid var(--border); padding:10px 16px; border-radius:12px; font-weight:700; font-size:0.82rem; cursor:pointer;">
                        \U0001F3A4
                    </button>
                </div>
            </div>

            <!-- Timeline de notas -->
            <div id="bitacoraTimeline" style="margin-bottom:20px;">
                <div style="text-align:center; padding:30px; color:var(--muted); font-size:0.8rem;">Sin notas para esta semana</div>
            </div>

            <!-- Acciones de informe -->
            <div style="background:linear-gradient(135deg, #1e3a8a 0%, #1e1b4b 100%); border-radius:20px; padding:20px; border:1px solid rgba(255,255,255,0.1);">
                <div style="font-size:0.9rem; font-weight:800; color:#fff; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
                    \U0001F4CB Informe Semanal
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                    <button onclick="generarInformeBitacora()" id="btnGenerarBitacora" style="background:#10b981; color:#fff; border:none; padding:12px; border-radius:14px; font-weight:700; font-size:0.82rem; cursor:pointer;">
                        \U0001F680 Generar Informe
                    </button>
                    <button onclick="verHistorialBitacora()" style="background:rgba(255,255,255,0.08); color:#fff; border:1px solid rgba(255,255,255,0.1); padding:12px; border-radius:14px; font-weight:700; font-size:0.82rem; cursor:pointer;">
                        \U0001F4C5 Historial
                    </button>
                </div>
            </div>
        </div>
        <div class="section-gap"></div>
    </div>
'''
    
    if 'view-bitacora' not in html:
        html = html.replace('</main>', bitacora_view + '</main>')
        print("[OK] Bitacora view injected")

    # ═══════════════════════════════════════════
    # 3. ADD JS FUNCTIONS (before </body>)
    # ═══════════════════════════════════════════
    bitacora_js = '''<script>
// ══════════════════════════════════════
// BITACORA DE OBRA — Modulo Master
// ══════════════════════════════════════
let bitacoraSemana = 1;
let bitacoraRecognition = null;

function initBitacoraView() {
    bitacoraSemana = currentWeek;
    const obraLabel = document.getElementById('bitacoraObraName');
    if(obraLabel && currentObra) obraLabel.textContent = currentObra.name || currentObra.id;
    updateBitacoraSemanaUI();
    cargarNotasBitacora();
}

function changeBitacoraSemana(delta) {
    bitacoraSemana = Math.max(1, Math.min(TOTAL_WEEKS, bitacoraSemana + delta));
    updateBitacoraSemanaUI();
    cargarNotasBitacora();
}

function updateBitacoraSemanaUI() {
    const label = document.getElementById('bitacoraSemanaLabel');
    const display = document.getElementById('bitacoraWeekDisplay');
    if(label) label.textContent = 'Semana ' + bitacoraSemana;
    if(display) display.textContent = 'Semana ' + bitacoraSemana;
}

async function guardarNotaBitacora() {
    const input = document.getElementById('bitacoraInput');
    const texto = input.value.trim();
    if(!texto) { alert('Escribe algo antes de guardar.'); return; }
    if(!db || !session || !session.obra) { alert('No hay conexi\u00f3n.'); return; }
    
    try {
        const now = new Date();
        await db.collection('obras').doc(session.obra).collection('bitacora').add({
            semana: bitacoraSemana,
            texto: texto,
            fecha: now.toLocaleDateString('es-MX'),
            hora: now.toLocaleTimeString('es-MX', {hour:'2-digit', minute:'2-digit'}),
            timestamp: firebase.firestore.FieldValue.serverTimestamp(),
            usuario: session.email || 'master'
        });
        input.value = '';
        cargarNotasBitacora();
    } catch(e) { alert('Error al guardar: ' + e.message); }
}

async function cargarNotasBitacora() {
    if(!db || !session || !session.obra) return;
    const container = document.getElementById('bitacoraTimeline');
    if(!container) return;
    
    try {
        const snap = await db.collection('obras').doc(session.obra).collection('bitacora')
            .where('semana', '==', bitacoraSemana)
            .orderBy('timestamp', 'desc')
            .get();
        
        if(snap.empty) {
            container.innerHTML = '<div style="text-align:center; padding:30px; color:var(--muted); font-size:0.8rem;">Sin notas para esta semana</div>';
            document.getElementById('bitacoraNotaCount').textContent = '0 notas';
            return;
        }
        
        let html = '';
        let count = 0;
        snap.forEach(doc => {
            const d = doc.data();
            count++;
            html += `
                <div style="background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:14px; margin-bottom:10px; position:relative;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div style="flex:1;">
                            <div style="font-size:0.65rem; color:var(--muted); margin-bottom:6px; display:flex; align-items:center; gap:6px;">
                                <span style="background:rgba(59,130,246,0.2); color:#93c5fd; padding:2px 8px; border-radius:10px; font-weight:700;">${d.fecha || ''}</span>
                                <span>${d.hora || ''}</span>
                            </div>
                            <div style="font-size:0.85rem; color:#e2e8f0; line-height:1.5;">${d.texto}</div>
                        </div>
                        <button onclick="borrarNotaBitacora('${doc.id}')" style="background:none; border:none; color:rgba(239,68,68,0.6); cursor:pointer; font-size:1rem; padding:4px 8px; flex-shrink:0;" title="Eliminar">\u2715</button>
                    </div>
                </div>`;
        });
        container.innerHTML = html;
        document.getElementById('bitacoraNotaCount').textContent = count + ' nota' + (count !== 1 ? 's' : '');
    } catch(e) {
        container.innerHTML = '<div style="color:#f87171; padding:16px; text-align:center;">Error: ' + e.message + '</div>';
    }
}

async function borrarNotaBitacora(id) {
    if(!confirm('\u00bfEliminar esta nota?')) return;
    try {
        await db.collection('obras').doc(session.obra).collection('bitacora').doc(id).delete();
        cargarNotasBitacora();
    } catch(e) { alert('Error: ' + e.message); }
}

function dictarNotaBitacora() {
    const Speech = window.SpeechRecognition || window.webkitSpeechRecognition;
    if(!Speech) { alert('Tu navegador no soporta dictado por voz.'); return; }
    
    if(!bitacoraRecognition) {
        bitacoraRecognition = new Speech();
        bitacoraRecognition.lang = 'es-MX';
        bitacoraRecognition.onresult = (e) => {
            const text = e.results[0][0].transcript;
            document.getElementById('bitacoraInput').value += (document.getElementById('bitacoraInput').value ? '\\n' : '') + text;
        };
        bitacoraRecognition.onstart = () => {
            document.getElementById('btnDictarBitacora').style.background = '#ef4444';
            document.getElementById('btnDictarBitacora').textContent = '\U0001F6D1';
        };
        bitacoraRecognition.onend = () => {
            document.getElementById('btnDictarBitacora').style.background = 'rgba(255,255,255,0.08)';
            document.getElementById('btnDictarBitacora').textContent = '\U0001F3A4';
        };
    }
    try { bitacoraRecognition.start(); } catch(e) { bitacoraRecognition.stop(); }
}

async function generarInformeBitacora() {
    if(!db || !session || !session.obra) return;
    const btn = document.getElementById('btnGenerarBitacora');
    const oldText = btn.innerHTML;
    btn.innerHTML = '\u23f3 Generando...';
    btn.disabled = true;
    
    try {
        // 1. Recopilar notas de la semana
        const snap = await db.collection('obras').doc(session.obra).collection('bitacora')
            .where('semana', '==', bitacoraSemana)
            .orderBy('timestamp', 'asc')
            .get();
        
        if(snap.empty) { alert('No hay notas para generar el informe de esta semana.'); return; }
        
        let notas = [];
        snap.forEach(doc => notas.push(doc.data()));
        
        const obraName = (currentObra && currentObra.name) ? currentObra.name : session.obra;
        const now = new Date();
        
        // 2. Generar HTML del informe
        let notasHtml = notas.map(n => 
            `<tr><td style="padding:8px 12px; border-bottom:1px solid #eee; font-size:0.8rem; color:#64748b; white-space:nowrap;">${n.fecha || ''}<br>${n.hora || ''}</td><td style="padding:8px 12px; border-bottom:1px solid #eee; font-size:0.85rem; color:#1e293b;">${n.texto}</td></tr>`
        ).join('');
        
        const informeHtml = `
            <div style="font-family:'Inter',Arial,sans-serif; max-width:700px; margin:0 auto; padding:20px;">
                <div style="background:linear-gradient(135deg,#1e3a8a,#1e1b4b); color:#fff; padding:24px; border-radius:16px 16px 0 0;">
                    <div style="font-size:1.3rem; font-weight:800;">\U0001F3D7\ufe0f ${obraName}</div>
                    <div style="font-size:0.85rem; opacity:0.8; margin-top:4px;">Bit\u00e1cora de Obra \u2014 Semana ${bitacoraSemana}</div>
                    <div style="font-size:0.7rem; opacity:0.6; margin-top:8px;">Generado: ${now.toLocaleDateString('es-MX')} a las ${now.toLocaleTimeString('es-MX', {hour:'2-digit', minute:'2-digit'})}</div>
                </div>
                <div style="background:#fff; border:1px solid #e2e8f0; border-top:none; border-radius:0 0 16px 16px; padding:20px;">
                    <div style="font-size:0.9rem; font-weight:700; color:#1e293b; margin-bottom:12px;">\U0001F4DD Registro de Actividades (${notas.length} notas)</div>
                    <table style="width:100%; border-collapse:collapse;">
                        <thead>
                            <tr style="background:#f8fafc;">
                                <th style="padding:10px 12px; text-align:left; font-size:0.7rem; color:#64748b; text-transform:uppercase; font-weight:700;">Fecha</th>
                                <th style="padding:10px 12px; text-align:left; font-size:0.7rem; color:#64748b; text-transform:uppercase; font-weight:700;">Nota</th>
                            </tr>
                        </thead>
                        <tbody>${notasHtml}</tbody>
                    </table>
                    <div style="margin-top:20px; padding-top:16px; border-top:1px solid #e2e8f0; font-size:0.7rem; color:#94a3b8; text-align:center;">
                        SYD Constructores \u00b7 Informe generado autom\u00e1ticamente
                    </div>
                </div>
            </div>`;
        
        // 3. Guardar en Firestore
        const docRef = await db.collection('obras').doc(session.obra).collection('informes_bitacora').add({
            semana: bitacoraSemana,
            obra: session.obra,
            obraName: obraName,
            titulo: 'Bit\u00e1cora Semana ' + bitacoraSemana + ' - ' + obraName,
            totalNotas: notas.length,
            html: informeHtml,
            fechaGenerado: firebase.firestore.FieldValue.serverTimestamp(),
            fechaTexto: now.toLocaleDateString('es-MX'),
            enviado: false,
            emailMaster: session.email
        });
        
        console.log('[SYD] Informe bit\u00e1cora guardado:', docRef.id);
        
        // 4. Mostrar informe en modal
        mostrarInformeBitacora(informeHtml, docRef.id);
        
    } catch(e) {
        alert('Error al generar informe: ' + e.message);
        console.error(e);
    } finally {
        btn.innerHTML = oldText;
        btn.disabled = false;
    }
}

function mostrarInformeBitacora(html, docId) {
    const old = document.getElementById('bitacoraModal');
    if(old) old.remove();
    
    const modal = document.createElement('div');
    modal.id = 'bitacoraModal';
    modal.style.cssText = 'position:fixed; inset:0; z-index:99999; background:#f1f5f9; overflow-y:auto;';
    
    const toolbar = document.createElement('div');
    toolbar.style.cssText = 'position:sticky; top:0; z-index:10; background:#1e293b; padding:12px 16px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 2px 10px rgba(0,0,0,0.3);';
    toolbar.innerHTML = `
        <button onclick="document.getElementById('bitacoraModal').remove()" style="background:rgba(255,255,255,0.1); color:#fff; border:none; padding:8px 16px; border-radius:10px; font-weight:700; cursor:pointer;">\u2190 Volver</button>
        <div style="display:flex; gap:8px;">
            <button onclick="enviarInformeBitacoraEmail('${docId}')" style="background:#10b981; color:#fff; border:none; padding:8px 16px; border-radius:10px; font-weight:700; font-size:0.8rem; cursor:pointer;">\U0001F4E7 Enviar Email</button>
        </div>`;
    
    const content = document.createElement('div');
    content.style.cssText = 'padding:20px;';
    content.innerHTML = html;
    
    modal.appendChild(toolbar);
    modal.appendChild(content);
    document.body.appendChild(modal);
}

async function enviarInformeBitacoraEmail(docId) {
    // Por ahora mostrar instrucciones (el cron lo automatizar\u00e1)
    alert('\U0001F4E7 El informe est\u00e1 guardado en la base de datos.\\n\\nEl sistema lo enviar\u00e1 autom\u00e1ticamente por email cada viernes.\\n\\nTambi\u00e9n puedes compartir el informe copiando el enlace.');
}

async function verHistorialBitacora() {
    if(!db || !session || !session.obra) return;
    
    const old = document.getElementById('bitacoraHistModal');
    if(old) old.remove();
    
    const modal = document.createElement('div');
    modal.id = 'bitacoraHistModal';
    modal.style.cssText = 'position:fixed; inset:0; z-index:100000; background:rgba(0,0,0,0.85); display:flex; align-items:center; justify-content:center; padding:20px;';
    
    const container = document.createElement('div');
    container.style.cssText = 'background:#1f2937; width:100%; max-width:500px; max-height:80vh; border-radius:24px; padding:24px; overflow-y:auto; border:1px solid rgba(255,255,255,0.1);';
    
    container.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
            <h3 style="margin:0; font-size:1rem; color:#fff;">\U0001F4C5 Historial de Informes</h3>
            <button onclick="document.getElementById('bitacoraHistModal').remove()" style="background:none; border:none; font-size:1.5rem; cursor:pointer; color:#94a3b8;">&times;</button>
        </div>
        <div id="bitacoraHistList" style="display:flex; flex-direction:column; gap:10px;">
            <div style="text-align:center; padding:20px; color:#64748b;">Cargando...</div>
        </div>`;
    
    modal.appendChild(container);
    document.body.appendChild(modal);
    modal.addEventListener('click', (e) => { if(e.target === modal) modal.remove(); });
    
    try {
        const snap = await db.collection('obras').doc(session.obra).collection('informes_bitacora')
            .orderBy('fechaGenerado', 'desc')
            .limit(20)
            .get();
        
        const list = document.getElementById('bitacoraHistList');
        if(snap.empty) {
            list.innerHTML = '<div style="text-align:center; padding:20px; color:#64748b;">No hay informes generados a\u00fan.</div>';
            return;
        }
        
        let html = '';
        snap.forEach(doc => {
            const d = doc.data();
            html += `
                <div onclick="abrirInformeBitacora('${doc.id}')" style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:14px; cursor:pointer; transition:all 0.2s;">
                    <div style="font-size:0.85rem; font-weight:700; color:#fff;">${d.titulo || 'Informe Semana ' + d.semana}</div>
                    <div style="font-size:0.7rem; color:#64748b; margin-top:4px;">${d.fechaTexto || ''} \u00b7 ${d.totalNotas || 0} notas</div>
                </div>`;
        });
        list.innerHTML = html;
    } catch(e) {
        document.getElementById('bitacoraHistList').innerHTML = '<div style="color:#f87171; padding:16px;">Error: ' + e.message + '</div>';
    }
}

async function abrirInformeBitacora(docId) {
    try {
        const doc = await db.collection('obras').doc(session.obra).collection('informes_bitacora').doc(docId).get();
        if(doc.exists && doc.data().html) {
            document.getElementById('bitacoraHistModal').remove();
            mostrarInformeBitacora(doc.data().html, docId);
        }
    } catch(e) { alert('Error: ' + e.message); }
}
</script>
'''
    
    if 'guardarNotaBitacora' not in html:
        html = html.replace('</body>', bitacora_js + '</body>')
        print("[OK] Bitacora JS injected")

    # ═══════════════════════════════════════════
    # 4. UPDATE launchApp() to show/hide bitacora tab
    # ═══════════════════════════════════════════
    show_bitacora_tab = """
    // Bitacora tab: only Master
    const tabBit = document.getElementById('tabBitacora');
    if(tabBit) tabBit.style.display = session.role==='master' ? '' : 'none';
"""
    if 'tabBitacora' not in html.split('launchApp')[1].split('function ')[0] if 'launchApp' in html else '':
        # Insert after the tabAccesos visibility line
        html = html.replace(
            "if(tabAcc) tabAcc.style.display = session.role==='master' ? '' : 'none';",
            "if(tabAcc) tabAcc.style.display = session.role==='master' ? '' : 'none';\n" + show_bitacora_tab
        )
        print("[OK] launchApp updated for Bitacora tab")

    # ═══════════════════════════════════════════
    # 5. UPDATE switchTab() to handle bitacora
    # ═══════════════════════════════════════════
    bitacora_tab_handler = """
    if(tab === 'bitacora') initBitacoraView();
"""
    if "initBitacoraView" not in html:
        # Find switchTab function and add handler
        html = html.replace(
            "else if(currentTab==='accesos')",
            "else if(currentTab==='bitacora') { initBitacoraView(); }\n    else if(currentTab==='accesos')"
        )
        print("[OK] switchTab handler added for bitacora")

    # Bump version
    html = html.replace('v2.3.2', 'v2.4.0')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("[OK] All changes written. Version bumped to v2.4.0")

if __name__ == '__main__':
    inject_bitacora()
