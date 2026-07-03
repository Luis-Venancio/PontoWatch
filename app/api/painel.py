"""
Endpoints do painel — consumidos pelo front.
"""
from datetime import date
from fastapi import APIRouter, Query
from app.core.database import get_supabase

router = APIRouter(prefix="/painel", tags=["Painel"])


@router.get("/resumo")
def resumo_do_dia(dia: date = Query(default=None)):
    """KPIs do dia: conformes, ausentes, atrasos, fora do local."""
    dia = dia or date.today()

    try:
        db = get_supabase()
        rows = (
            db.table("comparacoes")
            .select("status_presenca")
            .eq("data_referencia", dia.isoformat())
            .execute()
            .data or []
        )
    except Exception:
        rows = []

    contadores = {"CONFORME": 0, "AUSENTE": 0, "ATRASO": 0, "FORA_DO_LOCAL": 0, "PARCIAL": 0}
    for r in rows:
        contadores[r["status_presenca"]] = contadores.get(r["status_presenca"], 0) + 1

    return {
        "data": dia.isoformat(),
        "total": len(rows),
        "conformes":    contadores["CONFORME"],
        "ausentes":     contadores["AUSENTE"],
        "atrasos":      contadores["ATRASO"],
        "fora_do_local":contadores["FORA_DO_LOCAL"],
    }


@router.get("/monitoramento")
def monitoramento_tempo_real(dia: date = Query(default=None)):
    """
    Tabela de monitoramento: funcionário × parada × status × GPS.
    """
    dia = dia or date.today()
    db = get_supabase()

    rows = (
        db.table("comparacoes")
        .select(
            "id, status_presenca, status_geo, "
            "hora_prevista_entrada, hora_real_entrada, "
            "minutos_atraso_entrada, distancia_entrada_m, dentro_raio_entrada, "
            "funcionarios(nome, equipe, departamento), locais(nome), roteiros(ordem)"
        )
        .eq("data_referencia", dia.isoformat())
        .order("nome", foreign_table="funcionarios")
        .execute()
        .data or []
    )

    return {"data": dia.isoformat(), "registros": rows}


@router.get("/por-equipe")
def conformidade_por_equipe(dia: date = Query(default=None)):
    """Conformidade agrupada por equipe."""
    dia = dia or date.today()
    db = get_supabase()

    rows = (
        db.table("comparacoes")
        .select("status_presenca, funcionarios(equipe)")
        .eq("data_referencia", dia.isoformat())
        .execute()
        .data or []
    )

    grupos: dict[str, dict] = {}
    for r in rows:
        equipe = (r.get("funcionarios") or {}).get("equipe") or "Sem equipe"
        g = grupos.setdefault(equipe, {"equipe": equipe, "total": 0, "conformes": 0})
        g["total"] += 1
        if r["status_presenca"] == "CONFORME":
            g["conformes"] += 1

    for g in grupos.values():
        g["pct"] = round(g["conformes"] / g["total"] * 100, 1) if g["total"] else 0

    return {"data": dia.isoformat(), "equipes": sorted(grupos.values(), key=lambda x: x["equipe"])}
