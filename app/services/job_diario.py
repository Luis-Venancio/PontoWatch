"""
Orquestrador do job diário.

Ordem de execução:
  1. Sincronizar funcionários (Ponto Mais → Supabase)
  2. Sincronizar batidas do dia
  3. Processar comparações (previsto × real)
  4. Disparar alertas por e-mail
  5. Registrar log de execução
"""
from datetime import date, datetime
from loguru import logger
from app.services.sync_service import sincronizar_funcionarios, sincronizar_batidas
from app.services.comparacao_engine import processar_dia, processar_presenca_dia
from app.services.notificacoes import disparar_alertas_pendentes
from app.core.database import get_supabase


def executar_job(dia: date | None = None) -> dict:
    """
    Ponto de entrada do job. Se `dia` não for informado,
    usa a data atual.
    """
    dia = dia or date.today()
    inicio = datetime.utcnow()
    db = get_supabase()

    log_id = _criar_log(db, dia, inicio)
    resultado = {
        "data": dia.isoformat(),
        "funcionarios_sync": 0,
        "batidas_sync": 0,
        "comparacoes": {},
        "presenca": {},
        "alertas_enviados": 0,
        "status": "SUCESSO",
        "erro": None,
    }

    try:
        logger.info(f"=== JOB DIÁRIO INICIADO — {dia} ===")

        # 1. Funcionários
        logger.info("Passo 1/4: sincronizando funcionários...")
        resultado["funcionarios_sync"] = sincronizar_funcionarios()

        # 2. Batidas
        logger.info(f"Passo 2/4: sincronizando batidas de {dia}...")
        resultado["batidas_sync"] = sincronizar_batidas(dia)

        # 3. Comparações (conformidade de local — só quem tem roteiro)
        logger.info("Passo 3/5: processando comparações...")
        resultado["comparacoes"] = processar_dia(dia)

        # 4. Presença geral (bateu ponto ou não — todo mundo)
        logger.info("Passo 4/5: processando presença geral...")
        resultado["presenca"] = processar_presenca_dia(dia)

        # 5. Alertas
        logger.info("Passo 5/5: disparando alertas...")
        resultado["alertas_enviados"] = disparar_alertas_pendentes(dia)

        logger.info(f"=== JOB CONCLUÍDO — {resultado} ===")

    except Exception as e:
        logger.exception(f"Erro no job: {e}")
        resultado["status"] = "FALHA"
        resultado["erro"] = str(e)

    finally:
        _atualizar_log(db, log_id, resultado, inicio)

    return resultado


# ──────────────────────────────────────────────────────────────
# Log de execução
# ──────────────────────────────────────────────────────────────

def _criar_log(db, dia: date, inicio: datetime) -> str:
    row = db.table("log_sincronizacao").insert({
        "data_referencia": dia.isoformat(),
        "iniciado_em": inicio.isoformat(),
        "status": "EXECUTANDO",
    }).execute()
    return row.data[0]["id"]


def _atualizar_log(db, log_id: str, resultado: dict, inicio: datetime):
    comp = resultado.get("comparacoes", {})
    db.table("log_sincronizacao").update({
        "finalizado_em":    datetime.utcnow().isoformat(),
        "total_funcionarios": resultado.get("funcionarios_sync", 0),
        "total_batidas":    resultado.get("batidas_sync", 0),
        "total_erros":      comp.get("erros", 0),
        "status":           resultado["status"],
        "detalhe_erro":     resultado.get("erro"),
    }).eq("id", log_id).execute()
