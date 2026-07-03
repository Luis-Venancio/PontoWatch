"""
Endpoints de alertas.
"""
from datetime import date
from fastapi import APIRouter, Query
from app.core.database import get_supabase

router = APIRouter(prefix="/alertas", tags=["Alertas"])


@router.get("/")
def listar_alertas(
    dia: date = Query(default=None),
    nivel_min: int = Query(default=1, ge=1, le=3),
    apenas_pendentes: bool = Query(default=False),
):
    dia = dia or date.today()
    db = get_supabase()

    q = (
        db.table("alertas")
        .select("*, funcionarios(nome, equipe)")
        .eq("data_referencia", dia.isoformat())
        .gte("nivel", nivel_min)
        .order("nivel", desc=True)
        .order("criado_em", desc=True)
    )
    if apenas_pendentes:
        q = q.eq("enviado", False)

    return {"alertas": q.execute().data or []}


@router.patch("/{alerta_id}/resolver")
def marcar_resolvido(alerta_id: str):
    db = get_supabase()
    db.table("alertas").update({"enviado": True}).eq("id", alerta_id).execute()
    return {"ok": True}
