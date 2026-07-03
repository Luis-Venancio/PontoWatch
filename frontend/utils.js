/**
 * utils.js — funções compartilhadas entre todas as páginas
 */

// ── Datas ─────────────────────────────────────────────────────
export function hojeISO() {
  return new Date().toISOString().slice(0, 10);
}

export function formatarData(isoStr) {
  if (!isoStr) return "—";
  const [y, m, d] = isoStr.split("-");
  return `${d}/${m}/${y}`;
}

export function formatarHora(timeStr) {
  if (!timeStr) return "—";
  return timeStr.slice(0, 5); // "HH:MM"
}

export function diaSemana(isoStr) {
  const dias = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
  const d = new Date(isoStr + "T12:00:00");
  return dias[d.getDay()];
}

// ── Status ────────────────────────────────────────────────────
const STATUS_MAP = {
  CONFORME:     { label: "Conforme",     cls: "ok"      },
  AUSENTE:      { label: "Ausente",      cls: "absent"  },
  ATRASO:       { label: "Atraso",       cls: "late"    },
  FORA_DO_LOCAL:{ label: "Fora do local",cls: "geo"     },
  PARCIAL:      { label: "Parcial",      cls: "pending" },
};

export function pillStatus(status) {
  const s = STATUS_MAP[status] || { label: status, cls: "pending" };
  return `<span class="pill ${s.cls}">${s.label}</span>`;
}

export function pillGeo(statusGeo) {
  if (!statusGeo) return "—";
  if (statusGeo === "OK")         return `<span class="pill ok">✅ No local</span>`;
  if (statusGeo === "DIVERGENTE") return `<span class="pill geo">⚠️ Divergente</span>`;
  if (statusGeo === "SEM_GPS")    return `<span class="pill pending">Sem GPS</span>`;
  return statusGeo;
}

export function nivelAlerta(nivel) {
  if (nivel === 3) return `<span class="alert-level l3">CRÍTICO</span>`;
  if (nivel === 2) return `<span class="alert-level l2">ATENÇÃO</span>`;
  return `<span class="alert-level l1">AVISO</span>`;
}

// ── Toast ─────────────────────────────────────────────────────
let toastTimer = null;

export function toast(msg, tipo = "ok") {
  let el = document.getElementById("toast");
  if (!el) {
    el = document.createElement("div");
    el.id = "toast";
    el.style.cssText = `
      position:fixed;bottom:24px;right:24px;z-index:9999;
      padding:12px 20px;border-radius:10px;font-size:13px;font-weight:600;
      transition:opacity .3s;pointer-events:none;
    `;
    document.body.appendChild(el);
  }
  el.textContent = msg;
  el.style.background = tipo === "ok" ? "#00C9A7" : tipo === "erro" ? "#E5534B" : "#F5A623";
  el.style.color = tipo === "ok" ? "#0F1E36" : "#fff";
  el.style.opacity = "1";
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.style.opacity = "0"; }, 3000);
}

// ── Loading state ─────────────────────────────────────────────
export function setLoading(el, sim) {
  if (!el) return;
  if (sim) {
    el.dataset.originalText = el.textContent;
    el.textContent = "Carregando…";
    el.disabled = true;
  } else {
    el.textContent = el.dataset.originalText || el.textContent;
    el.disabled = false;
  }
}

// ── Delta de minutos (exibe com cor) ─────────────────────────
export function deltaMin(min) {
  if (min === null || min === undefined) return "—";
  const cor = min <= 0 ? "var(--green)" : min <= 15 ? "var(--amber)" : "var(--red)";
  const sinal = min > 0 ? `+${min}` : `${min}`;
  return `<span style="color:${cor};font-family:var(--mono)">${sinal} min</span>`;
}

// ── Distância GPS ─────────────────────────────────────────────
export function distanciaGPS(metros, raio) {
  if (metros === null || metros === undefined) return "—";
  const ok = metros <= raio;
  const cor = ok ? "var(--green)" : "var(--red)";
  const icone = ok ? "✅" : "⚠️";
  return `<span style="color:${cor};font-family:var(--mono)">${icone} ${Math.round(metros)}m</span>`;
}
