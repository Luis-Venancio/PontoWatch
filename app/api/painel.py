"""
Endpoints do painel — consumidos pelo front.
"""
from datetime import date
from fastapi import APIRouter, Query
from app.core.database import get_supabase

router = APIRouter(prefix="/painel", tags=["Painel"])


@router.get("/resumo")
def resumo_do_dia(dia: date = Query(default=None)):
    """
    KPIs do dia: conformes, ausentes, atrasos, fora do local.

    Combina duas fontes: `comparacoes` (conformidade de local/horário —
    só quem tem roteiro) e `presencas_dia` (presença + status_padrao —
    todo mundo, usando o horário padrão da empresa pra quem não tem
    roteiro). "Ausentes" e "total" vêm sempre de `presencas_dia`, que
    cobre os 2 casos sem duplicar contagem.
    """
    dia = dia or date.today()
    db = get_supabase()

    try:
        rows = (
            db.table("comparacoes")
            .select("status_presenca")
            .eq("data_referencia", dia.isoformat())
            .execute()
            .data or []
        )
    except Exception:
        rows = []

    contadores = {"CONFORME": 0, "ATRASO": 0, "FORA_DO_LOCAL": 0, "PARCIAL": 0}
    for r in rows:
        contadores[r["status_presenca"]] = contadores.get(r["status_presenca"], 0) + 1

    try:
        presenca_rows = (
            db.table("presencas_dia")
            .select("bateu_ponto, status_padrao")
            .eq("data_referencia", dia.isoformat())
            .execute()
            .data or []
        )
    except Exception:
        presenca_rows = []

    ausentes = sum(1 for r in presenca_rows if not r["bateu_ponto"])
    conformes_padrao = sum(1 for r in presenca_rows if r["status_padrao"] == "CONFORME")
    atrasos_padrao = sum(1 for r in presenca_rows if r["status_padrao"] == "ATRASO")

    return {
        "data": dia.isoformat(),
        "total": len(presenca_rows) or len(rows),
        "conformes":     contadores["CONFORME"] + conformes_padrao,
        "ausentes":      ausentes,
        "atrasos":       contadores["ATRASO"] + atrasos_padrao,
        "fora_do_local": contadores["FORA_DO_LOCAL"],
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


@router.get("/presenca")
def presenca_geral(dia: date = Query(default=None)):
    """
    Presença de TODOS os funcionários ativos no dia (bateu ponto ou não),
    independente de terem roteiro cadastrado. Complementa /monitoramento,
    que só cobre quem tem roteiro (e traz conformidade de local/GPS).
    """
    dia = dia or date.today()
    db = get_supabase()

    rows = (
        db.table("presencas_dia")
        .select(
            "bateu_ponto, tem_roteiro, status_padrao, primeira_batida, ultima_batida, total_batidas, "
            "funcionarios(nome, equipe, departamento)"
        )
        .eq("data_referencia", dia.isoformat())
        .order("nome", foreign_table="funcionarios")
        .execute()
        .data or []
    )

    presentes = sum(1 for r in rows if r["bateu_ponto"])

    return {
        "data": dia.isoformat(),
        "total": len(rows),
        "presentes": presentes,
        "ausentes": len(rows) - presentes,
        "registros": rows,
    }


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
