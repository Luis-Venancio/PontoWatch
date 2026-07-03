/**
 * layout.js — injeta sidebar + topbar em todas as páginas
 * e gerencia o relógio do topbar.
 */
export function montarLayout(paginaAtiva, tituloPagina) {
  const navItems = [
    { id: "painel",       icon: "📊", label: "Painel Hoje",       href: "index.html",        secao: "Operação" },
    { id: "roteiros",     icon: "📋", label: "Roteiros",           href: "roteiros.html",     secao: null },
    { id: "mapa",         icon: "🗺️", label: "Mapa ao Vivo",       href: "mapa.html",         secao: null },
    { id: "alertas",      icon: "🔔", label: "Alertas",            href: "alertas.html",      secao: null, badge: true },
    { id: "locais",       icon: "📍", label: "Locais",             href: "locais.html",       secao: "Cadastros" },
    { id: "funcionarios", icon: "👤", label: "Funcionários",       href: "funcionarios.html", secao: null },
    { id: "historico",    icon: "📈", label: "Histórico",          href: "historico.html",    secao: "Análise" },
  ];

  let navHtml = "";
  let secaoAtual = null;
  for (const item of navItems) {
    if (item.secao !== secaoAtual) {
      if (item.secao) navHtml += `<div class="nav-section">${item.secao}</div>`;
      secaoAtual = item.secao;
    }
    const ativo = item.id === paginaAtiva ? "active" : "";
    const badge = item.badge ? `<span class="badge" id="badge-alertas">0</span>` : "";
    navHtml += `
      <a class="nav-item ${ativo}" href="${item.href}">
        <span class="icon">${item.icon}</span> ${item.label} ${badge}
      </a>`;
  }

  document.body.insertAdjacentHTML("afterbegin", `
    <div class="sidebar">
      <div class="logo">
        <div class="logo-mark">RH · Automação</div>
        <div class="logo-name">Ponto<span style="color:var(--teal)">Watch</span></div>
      </div>
      <nav class="nav">${navHtml}</nav>
      <div class="sidebar-footer">
        <div class="user-chip">
          <div class="avatar">GC</div>
          <div>
            <div class="user-name">Gestor Central</div>
            <div class="user-role">Coordenador RH</div>
          </div>
        </div>
      </div>
    </div>
    <div class="main">
      <div class="topbar">
        <div class="topbar-title">${tituloPagina}</div>
        <div class="topbar-date" id="topbar-date"></div>
      </div>
      <div class="content" id="content"></div>
    </div>
  `);

  _iniciarRelogio();
  _carregarBadgeAlertas();
}

function _iniciarRelogio() {
  const el = document.getElementById("topbar-date");
  const tick = () => {
    const now = new Date();
    const dias  = ["Dom","Seg","Ter","Qua","Qui","Sex","Sáb"];
    const meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"];
    el.textContent = `${dias[now.getDay()]}, ${now.getDate()} ${meses[now.getMonth()]} ${now.getFullYear()} · ${String(now.getHours()).padStart(2,"0")}:${String(now.getMinutes()).padStart(2,"0")}`;
  };
  tick();
  setInterval(tick, 30_000);
}

async function _carregarBadgeAlertas() {
  try {
    const { api } = await import("./api.js");
    const hoje = new Date().toISOString().slice(0, 10);
    const data = await api.alertas.listar(hoje, 2);
    const pendentes = (data.alertas || []).filter(a => !a.enviado).length;
    const badge = document.getElementById("badge-alertas");
    if (badge) {
      badge.textContent = pendentes;
      badge.style.display = pendentes > 0 ? "inline" : "none";
    }
  } catch (_) { /* silencioso se API offline */ }
}
