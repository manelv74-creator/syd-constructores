// ══ DIAGNÓSTICO IA — SYD (debug_gemini.js) ══
async function debugGemini() {
    if (typeof GEMINI_API_KEY === 'undefined' || !GEMINI_API_KEY) {
        alert('⚠️ No hay API Key configurada.\nPulsa el engranaje ⚙️ y guarda tu Gemini Key primero.');
        return;
    }
    if (typeof weeklyNotes === 'undefined' || weeklyNotes.length === 0) {
        alert('⚠️ No hay notas esta semana. Agrega al menos una nota antes de diagnosticar.');
        return;
    }

    alert('🔬 Iniciando diagnóstico completo...\nEspera ~15 segundos mientras llamo a Gemini.\nSe descargará un archivo HTML con el resultado completo.');

    // ── 1. Fotos ──
    let fotoUrls = [];
    try {
        const fotosSnap = await db.collection('obras').doc(session.obra)
            .collection('fotos').orderBy('timestamp', 'desc').limit(8).get();
        fotosSnap.forEach(doc => fotoUrls.push(doc.data().url));
    } catch(e) { console.warn('Debug fotos:', e); }

    // ── 2. Base64 ──
    const imgResults = [];
    for (const url of fotoUrls.slice(0, 4)) {
        const b64 = await getBase64ImageSafe(url);
        imgResults.push({ url, ok: !!b64, b64: b64 || null });
    }

    // ── 3. Prompt ──
    const notasTexto = weeklyNotes.map((n, i) => `${i + 1}. ${n}`).join('\n');
    const prompt = `Eres un Ingeniero Civil Residente de Obra redactando un INFORME SEMANAL FORMAL.

TAREA: Reescribe las notas de campo como documento técnico profesional de ingeniería civil.

REGLAS:
1. NUNCA copies las notas. Reescribe con vocabulario diferente.
2. NUNCA uses lenguaje informal.
3. Tercera persona formal y voz pasiva técnica.
4. USA: "se ejecutó la instalación", "se completó la habilitación", "aparatos sanitarios", "prueba hidráulica"

NOTAS DEL RESIDENTE (NO copiar):
${notasTexto}

CONTEXTO: Remodelación residencial. Fase: instalaciones y acabados. Fotos: ${fotoUrls.length}

Devuelve ÚNICAMENTE JSON (sin markdown):
{"resumen":"[3 párrafos técnicos]","avances":["[avance 1]","[avance 2]","[avance 3]","[avance 4]"],"descripciones":["[pie foto 1]","[pie foto 2]","[pie foto 3]","[pie foto 4]"]}`;

    // ── 4. Llamar Gemini ──
    const parts = [{ text: prompt }];
    for (const r of imgResults) {
        if (r.ok && r.b64) parts.push({ inlineData: { mimeType: 'image/jpeg', data: r.b64 } });
    }

    let rawResponse = 'Sin respuesta';
    let statusCode = '?';
    let errorMsg = null;
    try {
        const res = await fetch(
            `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`,
            { method: 'POST', headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ contents: [{ parts }] }) }
        );
        statusCode = res.status;
        const data = await res.json();
        rawResponse = JSON.stringify(data, null, 2);
        if (data.error) errorMsg = data.error.message;
    } catch(e) {
        rawResponse = 'ERROR DE RED: ' + e.message;
        errorMsg = e.message;
    }

    // ── 5. Generar HTML de diagnóstico ──
    const imgsSent = imgResults.filter(r => r.ok).length;
    const hasError = !!errorMsg || rawResponse.includes('"error"');
    const hasText  = rawResponse.includes('"text"');
    const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

    const htmlContent = `<!DOCTYPE html><html><head><meta charset="UTF-8">
<title>Diagnostico IA SYD</title>
<style>
  body{font-family:monospace;background:#0a0f1e;color:#e2e8f0;padding:24px;line-height:1.7;margin:0}
  h1{color:#fbbf24;font-size:1.1rem;border-bottom:2px solid #fbbf24;padding-bottom:8px;margin-bottom:20px}
  h3{color:#93c5fd;font-size:0.85rem;margin:20px 0 6px}
  .box{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:14px;white-space:pre-wrap;word-break:break-all;font-size:0.78rem;margin-bottom:10px}
  .ok{color:#10b981;font-weight:bold} .fail{color:#ef4444;font-weight:bold} .warn{color:#fbbf24;font-weight:bold}
  .section{border-left:3px solid #475569;padding-left:14px;margin:16px 0}
  hr{border:none;border-top:1px solid #334155;margin:24px 0}
</style></head><body>
<h1>🔬 DIAGNOSTICO IA — SYD CONSTRUCTORES</h1>

<div class="section">
<h3>📊 RESUMEN EJECUTIVO</h3>
<div class="box">API Key:           ${GEMINI_API_KEY.substring(0,12)}...
Notas cargadas:    <span class="${weeklyNotes.length>0?'ok':'fail'}">${weeklyNotes.length} nota(s)</span>
Fotos en Firebase: <span class="${fotoUrls.length>0?'ok':'warn'}">${fotoUrls.length} foto(s)</span>
Imagenes a Gemini: <span class="${imgsSent>0?'ok':'warn'}">${imgsSent} de ${fotoUrls.length} (${imgsSent===0?'TODAS fallaron por CORS':'algunas OK'})</span>
HTTP Status:       <span class="${statusCode===200?'ok':'fail'}">${statusCode}</span>
Gemini respondio:  <span class="${hasText?'ok':'fail'}">${hasText?'SI OK':'NO - ver abajo'}</span>
Error:             <span class="${hasError?'fail':'ok'}">${hasError?'SI - '+esc(errorMsg||'ver JSON'):'NO'}</span></div>
</div>

<hr>
<div class="section">
<h3>📝 NOTAS DISPONIBLES (${weeklyNotes.length})</h3>
<div class="box">${esc(notasTexto)}</div>
</div>

<div class="section">
<h3>📷 FOTOS EN FIREBASE (${fotoUrls.length})</h3>
<div class="box">${fotoUrls.length>0 ? fotoUrls.map((u,i)=>`Foto ${i+1}: ${esc(u)}`).join('\n') : 'SIN FOTOS'}</div>
</div>

<div class="section">
<h3>🖼️ CONVERSION BASE64</h3>
<div class="box">${imgResults.length>0
  ? imgResults.map((r,i)=>`Foto ${i+1}: <span class="${r.ok?'ok':'fail'}">${r.ok?'CONVERTIDA OK':'FALLO CORS - no se enviara a Gemini'}</span>\n  URL: ${esc(r.url)}`).join('\n\n')
  : 'Sin fotos'}</div>
</div>

<div class="section">
<h3>📤 PROMPT ENVIADO A GEMINI</h3>
<div class="box">${esc(prompt)}</div>
</div>

<hr>
<div class="section">
<h3>📥 RESPUESTA CRUDA DE GEMINI <span class="${hasError?'fail':hasText?'ok':'warn'}">[${hasError?'ERROR':hasText?'OK':'VACIO'}]</span></h3>
<div class="box">${esc(rawResponse)}</div>
</div>

<p style="color:#475569;font-size:0.7rem;margin-top:24px">
  Generado: ${new Date().toLocaleString('es-MX')} | SYD Debug v3 (descargado como archivo)
</p>
</body></html>`;

    // ── 6. Descargar como archivo HTML (evita bloqueo de popups) ──
    const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `debug_syd_${Date.now()}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    alert(`✅ Diagnóstico completo.\n\nSe descargó "debug_syd_*.html"\nÁbrelo en el navegador para ver:\n• Lo que se envió a Gemini\n• La respuesta cruda\n• Si las imágenes se enviaron`);
}
