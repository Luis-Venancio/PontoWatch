/**
 * api.js — cliente centralizado para o backend PontoWatch
 *
 * Configure a variável API_BASE para apontar ao seu backend.
 * Em desenvolvimento: http://localhost:8001
 * Em produção: https://seu-app.railway.app
 */

const API_BASE = window.PONTOWATCH_API_URL || "http://localhost:8001";

async function request(method, path, body = null) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(`${API_BASE}${path}`, opts);
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`[${res.status}] ${path} → ${err}`);
  }
  return res.json();
}

// ── Painel ────────────────────────────────────────────────────
export const api = {
  painel: {
    resumo:        (dia) => request("GET", `/painel/resumo${dia ? `?dia=${dia}` : ""}`),
    monitoramento: (dia) => request("GET", `/painel/monitoramento${dia ? `?dia=${dia}` : ""}`),
    porEquipe:     (dia) => request("GET", `/painel/por-equipe${dia ? `?dia=${dia}` : ""}`),
    presenca:      (dia) => request("GET", `/painel/presenca${dia ? `?dia=${dia}` : ""}`),
  },

  // ── Roteiros ────────────────────────────────────────────────
  roteiros: {
    buscar:    (funcId, data)  => request("GET",    `/roteiros/${funcId}/${data}`),
    pendentes: (data)          => request("GET",    `/roteiros/pendentes/${data}`),
    publicar:  (payload)       => request("POST",   `/roteiros/publicar`, payload),
    addParada: (parada)        => request("POST",   `/roteiros/parada`, parada),
    delParada: (id)            => request("DELETE", `/roteiros/parada/${id}`),
  },

  // ── Alertas ─────────────────────────────────────────────────
  alertas: {
    listar:   (dia, nivelMin) => request("GET",   `/alertas/?dia=${dia}&nivel_min=${nivelMin ?? 1}`),
    resolver: (id)            => request("PATCH",  `/alertas/${id}/resolver`),
  },

  // ── Job ─────────────────────────────────────────────────────
  job: {
    executar: (dia) => request("POST", `/job/executar${dia ? `?dia=${dia}` : ""}`),
    proximo:  ()    => request("GET",  `/job/proximo`),
  },
};
