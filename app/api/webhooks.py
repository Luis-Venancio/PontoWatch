"""
Recebe eventos em tempo real do Ponto Mais (push), como complemento ao
job diário (que continua sendo a fonte de verdade e o único disparo de
e-mail de alertas).

Documentação: seção "Webhooks" em pontomais-api-integracao.md.
"""
from datetime import date
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException
from loguru import logger
from pydantic import BaseModel

from app.core.config import get_settings
from app.services.sync_service import sincronizar_batidas
from app.services.comparacao_engine import processar_dia, processar_presenca_dia

router = APIRouter(prefix="/webhooks/pontomais", tags=["Webhooks"])


class EquipeWebhook(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[str] = None


class ColaboradorWebhook(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    registration_number: Optional[str] = None
    team: Optional[EquipeWebhook] = None


class RegistroPontoWebhook(BaseModel):
    date: str
    time: str
    address: Optional[str] = None
    employee: ColaboradorWebhook


def _validar_token(token: Optional[str]):
    esperado = get_settings().pontomais_webhook_token
    if not esperado:
        logger.warning("PONTOMAIS_WEBHOOK_TOKEN não configurado — aceitando webhook sem validação")
        return
    if token != esperado:
        raise HTTPException(status_code=401, detail="Token inválido")


def _reprocessar_dia(dia: date):
    """Roda em background: só re-sincroniza dados e recalcula comparações/presença.
    Não dispara e-mail — isso continua exclusivo do job diário das 06:00."""
    try:
        sincronizar_batidas(dia)
        processar_dia(dia)
        processar_presenca_dia(dia)
        logger.info(f"Webhook: dia {dia} reprocessado com sucesso")
    except Exception as e:
        logger.exception(f"Webhook: erro ao reprocessar {dia}: {e}")


@router.post("/registro-ponto")
def evento_registro_ponto(
    payload: RegistroPontoWebhook,
    background_tasks: BackgroundTasks,
    token: Optional[str] = Header(default=None),
):
    _validar_token(token)

    logger.info(
        f"Webhook recebido: {payload.employee.name} "
        f"(matrícula {payload.employee.registration_number}) "
        f"bateu ponto em {payload.date} {payload.time} — {payload.address}"
    )

    dia = date.fromisoformat(payload.date)
    background_tasks.add_task(_reprocessar_dia, dia)

    return {"ok": True}
