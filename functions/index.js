const { onDocumentCreated } = require("firebase-functions/v2/firestore");
const { onSchedule } = require("firebase-functions/v2/scheduler");
const admin = require("firebase-admin");

admin.initializeApp();
const db = admin.firestore();

// ══════════════════════════════════════
// 1. PUSH: Notificación al subir foto
// ══════════════════════════════════════
exports.enviarNotificacionFotoNueva = onDocumentCreated(
  "obras/{obraId}/galeria/{fotoId}",
  async (event) => {
    const snap = event.data;
    if (!snap) return;

    const fotoData = snap.data();
    const obraId = event.params.obraId;

    console.log(`[SYD-BOT] Nueva foto detectada en obra: ${obraId}`, fotoData);

    try {
      const tokensRef = db.collection(`obras/${obraId}/tokens`);
      const tokensSnap = await tokensRef.get();

      if (tokensSnap.empty) {
        console.log(`[SYD-BOT] No hay clientes registrados en ${obraId}`);
        return;
      }

      const message = {
        notification: {
          title: "¡Nuevo Avance de Obra! 🏗️",
          body: `Se ha subido una nueva fotografía a la zona: ${fotoData.zona || 'Tu Proyecto'}`,
        },
        data: {
          click_action: "FLUTTER_NOTIFICATION_CLICK",
          url: "https://manelv74-creator.github.io/syd-constructores/"
        },
        tokens: []
      };

      tokensSnap.forEach(doc => {
        const tData = doc.data();
        if (tData.token) message.tokens.push(tData.token);
      });

      if (message.tokens.length === 0) return;

      const response = await admin.messaging().sendEachForMulticast(message);
      console.log(`[SYD-BOT] Push enviados. OK: ${response.successCount}, Fail: ${response.failureCount}`);
    } catch (error) {
      console.error("[SYD-BOT] Error push:", error);
    }
  }
);

// ══════════════════════════════════════
// 2. CRON: Recordatorio viernes 08:00 AM (CST = UTC-6 → 14:00 UTC)
//    "Recuerda generar tus notas de bitácora"
// ══════════════════════════════════════
exports.recordatorioBitacoraViernes = onSchedule(
  {
    schedule: "0 14 * * 5",  // Viernes 14:00 UTC = 08:00 CST (Guadalajara)
    timeZone: "America/Mexico_City",
    region: "us-central1"
  },
  async (event) => {
    console.log("[SYD-CRON] Ejecutando recordatorio de bitácora (Viernes 08:00 AM CST)");

    try {
      // Buscar todos los tokens del Master en todas las obras
      const obrasSnap = await db.collection("obras").get();

      for (const obraDoc of obrasSnap.docs) {
        const obraId = obraDoc.id;
        const tokensSnap = await db.collection(`obras/${obraId}/tokens`)
          .where("role", "==", "master")
          .get();

        if (tokensSnap.empty) continue;

        const tokens = [];
        tokensSnap.forEach(doc => {
          if (doc.data().token) tokens.push(doc.data().token);
        });

        if (tokens.length === 0) continue;

        const message = {
          notification: {
            title: "📝 Recordatorio: Bitácora de Obra",
            body: `No olvides agregar tus notas de la semana para ${obraId}. El informe se enviará mañana sábado.`,
          },
          tokens: tokens
        };

        await admin.messaging().sendEachForMulticast(message);
        console.log(`[SYD-CRON] Recordatorio enviado a ${tokens.length} master(s) de ${obraId}`);
      }
    } catch (error) {
      console.error("[SYD-CRON] Error en recordatorio:", error);
    }
  }
);

// ══════════════════════════════════════
// 3. CRON: Informe semanal sábado 14:00 (CST = UTC-6 → 20:00 UTC)
//    Genera y guarda el informe de bitácora. Si no hay notas: "SEMANA SIN BITÁCORA"
// ══════════════════════════════════════
exports.enviarInformeBitacoraSemanal = onSchedule(
  {
    schedule: "0 14 * * 6",  // Sábado 14:00 CST (timeZone lo maneja)
    timeZone: "America/Mexico_City",
    region: "us-central1"
  },
  async (event) => {
    console.log("[SYD-CRON] Generando informe semanal de bitácora (Sábado 14:00 CST)");

    try {
      const obrasSnap = await db.collection("obras").get();

      for (const obraDoc of obrasSnap.docs) {
        const obraId = obraDoc.id;
        const obraData = obraDoc.data();
        const obraName = obraData.name || obraData.nombre || obraId;

        // Calcular semana actual (semanas desde inicio del proyecto)
        const now = new Date();
        const weekNum = getWeekNumber(now);

        // Buscar notas de esta semana
        const notasSnap = await db.collection(`obras/${obraId}/bitacora`)
          .where("semana", "==", weekNum)
          .orderBy("timestamp", "asc")
          .get();

        let informeHtml;
        let totalNotas = 0;
        let titulo;

        if (notasSnap.empty) {
          // ═══ SIN NOTAS ═══
          titulo = `SEMANA SIN BITÁCORA - Semana ${weekNum} - ${obraName}`;
          informeHtml = `
            <div style="font-family:'Inter',Arial,sans-serif; max-width:700px; margin:0 auto; padding:20px;">
              <div style="background:linear-gradient(135deg,#92400e,#78350f); color:#fff; padding:24px; border-radius:16px 16px 0 0;">
                <div style="font-size:1.3rem; font-weight:800;">⚠️ ${obraName}</div>
                <div style="font-size:0.85rem; opacity:0.8; margin-top:4px;">Semana ${weekNum} — SEMANA SIN BITÁCORA</div>
                <div style="font-size:0.7rem; opacity:0.6; margin-top:8px;">${now.toLocaleDateString('es-MX')}</div>
              </div>
              <div style="background:#fff; border:1px solid #e2e8f0; border-top:none; border-radius:0 0 16px 16px; padding:40px; text-align:center;">
                <div style="font-size:1.5rem; font-weight:800; color:#92400e; margin-bottom:8px;">SEMANA SIN BITÁCORA</div>
                <div style="font-size:0.85rem; color:#64748b;">No se registraron notas durante esta semana.</div>
              </div>
            </div>`;
        } else {
          // ═══ CON NOTAS ═══
          let notas = [];
          notasSnap.forEach(doc => { notas.push(doc.data()); totalNotas++; });

          titulo = `Bitácora Semana ${weekNum} - ${obraName}`;
          const notasRows = notas.map(n =>
            `<tr><td style="padding:8px 12px; border-bottom:1px solid #eee; font-size:0.8rem; color:#64748b; white-space:nowrap;">${n.fecha || ''}<br>${n.hora || ''}</td><td style="padding:8px 12px; border-bottom:1px solid #eee; font-size:0.85rem; color:#1e293b;">${n.texto}</td></tr>`
          ).join('');

          informeHtml = `
            <div style="font-family:'Inter',Arial,sans-serif; max-width:700px; margin:0 auto; padding:20px;">
              <div style="background:linear-gradient(135deg,#1e3a8a,#1e1b4b); color:#fff; padding:24px; border-radius:16px 16px 0 0;">
                <div style="font-size:1.3rem; font-weight:800;">🏗️ ${obraName}</div>
                <div style="font-size:0.85rem; opacity:0.8; margin-top:4px;">Bitácora de Obra — Semana ${weekNum}</div>
                <div style="font-size:0.7rem; opacity:0.6; margin-top:8px;">${now.toLocaleDateString('es-MX')}</div>
              </div>
              <div style="background:#fff; border:1px solid #e2e8f0; border-top:none; border-radius:0 0 16px 16px; padding:20px;">
                <div style="font-size:0.9rem; font-weight:700; color:#1e293b; margin-bottom:12px;">📝 Registro (${totalNotas} notas)</div>
                <table style="width:100%; border-collapse:collapse;">
                  <thead><tr style="background:#f8fafc;">
                    <th style="padding:10px 12px; text-align:left; font-size:0.7rem; color:#64748b; text-transform:uppercase;">Fecha</th>
                    <th style="padding:10px 12px; text-align:left; font-size:0.7rem; color:#64748b; text-transform:uppercase;">Nota</th>
                  </tr></thead>
                  <tbody>${notasRows}</tbody>
                </table>
                <div style="margin-top:20px; padding-top:16px; border-top:1px solid #e2e8f0; font-size:0.7rem; color:#94a3b8; text-align:center;">
                  SYD Constructores · Informe automático semanal
                </div>
              </div>
            </div>`;
        }

        // Guardar informe en Firestore
        await db.collection(`obras/${obraId}/informes_bitacora`).add({
          semana: weekNum,
          obra: obraId,
          obraName: obraName,
          titulo: titulo,
          totalNotas: totalNotas,
          html: informeHtml,
          fechaGenerado: admin.firestore.FieldValue.serverTimestamp(),
          fechaTexto: now.toLocaleDateString('es-MX'),
          generadoPor: 'cron_automatico',
          enviado: true
        });

        console.log(`[SYD-CRON] Informe guardado para ${obraId}: ${titulo}`);

        // Enviar Push al Master avisando que el informe está listo
        const masterTokensSnap = await db.collection(`obras/${obraId}/tokens`)
          .where("role", "==", "master")
          .get();

        if (!masterTokensSnap.empty) {
          const masterTokens = [];
          masterTokensSnap.forEach(doc => {
            if (doc.data().token) masterTokens.push(doc.data().token);
          });

          if (masterTokens.length > 0) {
            await admin.messaging().sendEachForMulticast({
              notification: {
                title: `📋 Informe Semanal: ${obraName}`,
                body: totalNotas > 0
                  ? `Tu bitácora de la semana ${weekNum} con ${totalNotas} notas ha sido generada.`
                  : `Semana ${weekNum}: SEMANA SIN BITÁCORA`,
              },
              tokens: masterTokens
            });
          }
        }
      }
    } catch (error) {
      console.error("[SYD-CRON] Error en informe semanal:", error);
    }
  }
);

// Helper: obtener número de semana del año
function getWeekNumber(date) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}
