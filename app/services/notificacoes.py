"""
Serviço de notificações: dispara e-mails para alertas pendentes.
"""
import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loguru import logger
from app.core.config import get_settings
from app.core.database import get_supabase


def disparar_alertas_pendentes(dia: date) -> int:
    """
    Busca alertas não enviados do dia, agrupa por nível e
    envia e-mails. Retorna quantidade de alertas processados.
    """
    db = get_supabase()
    s = get_settings()

    if not s.smtp_user or not s.email_rh:
        logger.warning("SMTP não configurado — alertas não serão enviados por e-mail")
        return 0

    alertas = (
        db.table("alertas")
        .select("*, funcionarios(nome)")
        .eq("data_referencia", dia.isoformat())
        .eq("enviado", False)
        .order("nivel", desc=True)
        .execute()
        .data or []
    )

    if not alertas:
        logger.info("Nenhum alerta pendente para envio")
        return 0

    # Separa críticos (3) de atenção (2) e avisos (1)
    criticos  = [a for a in alertas if a["nivel"] == 3]
    atencao   = [a for a in alertas if a["nivel"] == 2]
    avisos    = [a for a in alertas if a["nivel"] == 1]

    corpo = _montar_corpo_email(dia, criticos, atencao, avisos)
    assunto = f"[PontoWatch] Alertas de ponto — {dia.strftime('%d/%m/%Y')} ({len(criticos)} críticos)"

    sucesso = _enviar_email(s, s.email_rh, assunto, corpo)

    if sucesso:
        ids = [a["id"] for a in alertas]
        # Marca em lotes de 50 para não exceder limites da API
        for i in range(0, len(ids), 50):
            lote = ids[i:i+50]
            db.table("alertas").update({
                "enviado": True,
                "enviado_em": date.today().isoformat() + "T00:00:00"
            }).in_("id", lote).execute()

        logger.info(f"{len(alertas)} alertas enviados por e-mail")
    else:
        logger.error("Falha no envio de e-mail — alertas permanecem como pendentes")

    return len(alertas) if sucesso else 0


# ──────────────────────────────────────────────────────────────
# Montagem do e-mail
# ──────────────────────────────────────────────────────────────

def _montar_corpo_email(dia: date, criticos, atencao, avisos) -> str:
    total = len(criticos) + len(atencao) + len(avisos)
    data_fmt = dia.strftime("%d/%m/%Y")

    def secao(titulo, emoji, items, cor):
        if not items:
            return ""
        linhas = "".join(
            f"<li style='margin-bottom:6px'>{a['descricao']}</li>"
            for a in items
        )
        return f"""
        <div style='margin-bottom:16px'>
          <h3 style='color:{cor};margin-bottom:8px'>{emoji} {titulo} ({len(items)})</h3>
          <ul style='padding-left:20px;color:#333'>{linhas}</ul>
        </div>"""

    return f"""
    <html><body style='font-family:Arial,sans-serif;max-width:640px;margin:0 auto;padding:20px'>
      <div style='background:#0F1E36;color:#00C9A7;padding:16px 20px;border-radius:8px;margin-bottom:20px'>
        <h2 style='margin:0'>PontoWatch — Relatório de Alertas</h2>
        <p style='margin:4px 0 0;color:#8B9BB4'>{data_fmt} · {total} ocorrências</p>
      </div>

      {secao('Críticos', '🔴', criticos, '#E5534B')}
      {secao('Atenção', '🟡', atencao, '#F5A623')}
      {secao('Avisos', '🔵', avisos, '#8B9BB4')}

      <hr style='border:1px solid #eee;margin:20px 0'>
      <p style='color:#999;font-size:12px'>
        Gerado automaticamente pelo PontoWatch · Job diário
      </p>
    </body></html>
    """


def _enviar_email(s, destinatario: str, assunto: str, corpo_html: str) -> bool:
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = assunto
        msg["From"]    = s.smtp_user
        msg["To"]      = destinatario
        msg.attach(MIMEText(corpo_html, "html"))

        with smtplib.SMTP(s.smtp_host, s.smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(s.smtp_user, s.smtp_pass)
            server.sendmail(s.smtp_user, destinatario, msg.as_string())

        return True
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {e}")
        return False
