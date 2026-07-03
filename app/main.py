"""
PontoWatch — aplicação principal.

Inicia:
  - FastAPI com todos os routers
  - APScheduler com o job diário no horário configurado
"""
from contextlib import asynccontextmanager
from datetime import date
from loguru import logger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config import get_settings
from app.api import painel, roteiros, alertas, locais, funcionarios
from app.services.job_diario import executar_job


# ──────────────────────────────────────────────────────────────
# Scheduler
# ──────────────────────────────────────────────────────────────

scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")


def _configurar_job():
    s = get_settings()
    hora, minuto = s.job_hora.split(":")
    scheduler.add_job(
        func=executar_job,
        trigger=CronTrigger(hour=int(hora), minute=int(minuto)),
        id="job_diario",
        replace_existing=True,
    )
    logger.info(f"Job diário agendado para {s.job_hora} (America/Sao_Paulo)")


# ──────────────────────────────────────────────────────────────
# Lifespan (startup / shutdown)
# ──────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    _configurar_job()
    scheduler.start()
    logger.info("PontoWatch iniciado ✅")
    yield
    scheduler.shutdown()
    logger.info("PontoWatch encerrado")


# ──────────────────────────────────────────────────────────────
# App
# ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="PontoWatch API",
    description="Monitoramento de ponto e geolocalização integrado ao Ponto Mais",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Em produção: especifique o domínio do front
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(painel.router)
app.include_router(roteiros.router)
app.include_router(alertas.router)
app.include_router(locais.router)
app.include_router(funcionarios.router)


# ──────────────────────────────────────────────────────────────
# Endpoints utilitários
# ──────────────────────────────────────────────────────────────

@app.get("/")
def health():
    return {"status": "ok", "app": "PontoWatch"}


@app.post("/job/executar")
def rodar_job_manual(dia: date = None):
    """
    Dispara o job manualmente (útil para testes e reprocessamento).
    Exemplo: POST /job/executar?dia=2025-06-19
    """
    resultado = executar_job(dia)
    return resultado


@app.get("/job/proximo")
def proximo_job():
    """Retorna quando o job será executado novamente."""
    job = scheduler.get_job("job_diario")
    if not job:
        return {"erro": "Job não encontrado"}
    return {"proxima_execucao": str(job.next_run_time)}
