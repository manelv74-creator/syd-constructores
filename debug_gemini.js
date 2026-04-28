// ══ DIAGNÓSTICO IA — SYD v4 (con detección automática de modelo) ══
async function debugGemini() {
    if (typeof GEMINI_API_KEY === 'undefined' || !GEMINI_API_KEY) {
        alert('⚠️ No hay API Key configurada.\nPulsa el engranaje ⚙️ y guarda tu Gemini Key primero.');
        return;
    }
    if (typeof weeklyNotes === 'undefined' || weeklyNotes.length === 0) {
        alert('⚠️ No hay notas esta semana. Agrega al menos una nota antes de diagnosticar.');
        return;
    }

    alert('🔬 Iniciando diagnóstico v4...\nEspera ~20 segundos.\nSe descargará un archivo HTML con todo.');

    const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

    // ── 1. Obtener modelos disponibles para esta KEY ──
    let modelosDisponibles = [];
    let modelosError = null;
    let modeloUsado = 'gemini-2.5-flash-preview-04-17'; // fallback
    try {
        const mRes = await fetch(
            `https://generativelanguage.googleapis.com/v1beta/models?key=${GEMINI_API_KEY}&pageSize=50`
        );
        const mData = await mRes.json();
        if (mData.models) {
            // Filtrar solo los que soportan generateContent
            modelosDisponibles = mData.models
                .filter(m => m.supportedGenerationMethods && m.supportedGenerationMethods.includes('generateContent'))
                .map(m => m.name.replace('models/', ''));
            // Preferir flash models
            const flashModels = modelosDisponibles.filter(m => m.includes('flash'));
            if (flashModels.length > 0) modeloUsado = flashModels[0];
            else if (modelosDisponibles.length > 0) modeloUsado = modelosDisponibles[0];
        } else if (mData.error) {
            modelosError = mData.error.message;
        }
    } catch(e) {
        modelosError = 'Error de red: ' + e.message;
    }

    // ── 2. Fotos ──
    let fotoUrls = [];
    try {
        const fotosSnap = await db.collection('obras').doc(session.obra)
            .collection('fotos').orderBy('timestamp', 'desc').limit(8).get();
        fotosSnap.forEach(doc => fotoUrls.push(doc.data().url));
    } catch(e) { console.warn('Debug fotos:', e); }

    // ── 3. Base64 ──
    const imgResults = [];
    for (const url of fotoUrls.slice(0, 4)) {
        const b64 = await getBase64ImageSafe(url);
        imgResults.push({ url, ok: !!b64, b64: b64 || null });
    }

    // ── 4. Prompt ──
    const notasTexto = weeklyNotes.map((n, i) => `${i + 1}. ${n}`).join('\n');
    const prompt = `Eres un Ingeniero Civil Residente de Obra.
Reescribe estas notas como informe técnico profesional.
REGLAS: Tercera persona formal. Sin lenguaje informal. Terminología de ingeniería civil.
NOTAS (NO copiar): ${notasTexto}
Devuelve JSON: {"resumen":"[texto]","avances":["[1]","[2]","[3]","[4]"],"descripciones":["[1]","[2]","[3]","[4]"]}`;

    // ── 5. Llamar Gemini con el modelo detectado automáticamente ──
    const parts = [{ text: prompt }];
    for (const r of imgResults) {
        if (r.ok && r.b64) parts.push({ inlineData: { mimeType: 'image/jpeg', data: r.b64 } });
    }

    let rawResponse = 'Sin respuesta';
    let statusCode = '?';
    let errorMsg = null;
    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${modeloUsado}:generateContent?key=${GEMINI_API_KEY}`;
    try {
        const res = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contents: [{ parts }] })
        });
        statusCode = res.status;
        const data = await res.json();
        rawResponse = JSON.stringify(data, null, 2);
        if (data.error) errorMsg = data.error.message;
    } catch(e) {
        rawResponse = 'ERROR DE RED: ' + e.message;
        errorMsg = e.message;
    }

    // ── 6. Generar HTML ──
    const imgsSent = imgResults.filter(r => r.ok).length;
    const hasError = !!errorMsg || rawResponse.includes('"error"');
    const hasText  = rawResponse.includes('"text"');

    const htmlContent = `<!DOCTYPE html><html><head><meta charset="UTF-8">
<title>Diagnostico IA SYD v4</title>
<style>
  body{font-family:monospace;background:#0a0f1e;color:#e2e8f0;padding:24px;line-height:1.7;margin:0}
  h1{color:#fbbf24;font-size:1.1rem;border-bottom:2px solid #fbbf24;padding-bottom:8px;margin-bottom:20px}
  h3{color:#93c5fd;font-size:0.85rem;margin:20px 0 6px}
  .box{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:14px;white-space:pre-wrap;word-break:break-all;font-size:0.78rem;margin-bottom:10px}
  .ok{color:#10b981;font-weight:bold} .fail{color:#ef4444;font-weight:bold} .warn{color:#fbbf24;font-weight:bold}
  .section{border-left:3px solid #475569;padding-left:14px;margin:16px 0}
  hr{border:none;border-top:1px solid #334155;margin:24px 0}
  li{margin:2px 0}
</style></head><body>
<h1>🔬 DIAGNOSTICO IA v4 — SYD CONSTRUCTORES</h1>

<div class="section">
<h3>📊 RESUMEN EJECUTIVO</h3>
<div class="box">API Key:           ${GEMINI_API_KEY.substring(0,12)}...
Notas cargadas:    <span class="${weeklyNotes.length>0?'ok':'fail'}">${weeklyNotes.length} nota(s)</span>
Fotos en Firebase: <span class="${fotoUrls.length>0?'ok':'warn'}">${fotoUrls.length} foto(s)</span>
Imagenes a Gemini: <span class="${imgsSent>0?'ok':'warn'}">${imgsSent} de ${fotoUrls.length}</span>
Modelo detectado:  <span class="${modelosError?'fail':'ok'}">${esc(modeloUsado)}</span>
URL llamada:       ${esc(apiUrl.replace(GEMINI_API_KEY, 'KEY...'))}
HTTP Status:       <span class="${statusCode===200?'ok':'fail'}">${statusCode}</span>
Gemini respondio:  <span class="${hasText?'ok':'fail'}">${hasText?'SI ✅':'NO ❌'}</span>
Error:             <span class="${hasError?'fail':'ok'}">${hasError?'SI ❌ — '+esc(errorMsg||'ver JSON'):'NO ✅'}</span></div>
</div>

<div class="section">
<h3>🤖 MODELOS DISPONIBLES PARA ESTA KEY (con generateContent)</h3>
<div class="box">${modelosError
  ? '<span class="fail">ERROR al obtener modelos: ' + esc(modelosError) + '</span>'
  : modelosDisponibles.length > 0
    ? modelosDisponibles.map((m,i) => `${i===0?'→ ':i===modelosDisponibles.indexOf(modeloUsado)?'★ ':'  '}${m}${m===modeloUsado?' ← USADO':''}`).join('\n')
    : 'SIN MODELOS DISPONIBLES para esta key'
}</div>
</div>

<hr>
<div class="section">
<h3>📝 NOTAS (${weeklyNotes.length})</h3>
<div class="box">${esc(notasTexto)}</div>
</div>

<div class="section">
<h3>🖼️ CONVERSION BASE64</h3>
<div class="box">${imgResults.length>0
  ? imgResults.map((r,i)=>`Foto ${i+1}: <span class="${r.ok?'ok':'fail'}">${r.ok?'OK':'CORS FALLO'}</span> — ${esc(r.url)}`).join('\n')
  : 'Sin fotos'}</div>
</div>

<hr>
<div class="section">
<h3>📥 RESPUESTA CRUDA DE GEMINI <span class="${hasError?'fail':hasText?'ok':'warn'}">[${hasError?'ERROR':hasText?'OK':'VACÍO'}]</span></h3>
<div class="box">${esc(rawResponse)}</div>
</div>

<p style="color:#475569;font-size:0.7rem;margin-top:24px">
  SYD Debug v4 | ${new Date().toLocaleString('es-MX')}
</p>
</body></html>`;

    // ── 7. Descargar HTML ──
    const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `debug_syd_v4_${Date.now()}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    alert('✅ Debug v4 descargado.\nRevisa la sección "MODELOS DISPONIBLES" — te dirá exactamente qué modelos acepta tu key.');
}
