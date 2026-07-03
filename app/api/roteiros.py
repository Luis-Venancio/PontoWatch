"""
Endpoints de roteiros — criação e consulta.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.database import get_supabase

router = APIRouter(prefix="/roteiros", tags=["Roteiros"])


# ──────────────────────────────────────────────────────────────
# Schemas
# ──────────────────────────────────────────────────────────────

class ParadaIn(BaseModel):
    funcionario_id: str
    data_roteiro: date
    ordem: int
    local_id: str
    hora_prevista_entrada: str   # "HH:MM"
    hora_prevista_saida: str     # "HH:MM"
    tolerancia_min: Optional[int] = 15
    observacao: Optional[str] = None


class PublicarRoteiroIn(BaseModel):
    funcionario_id: str
    data_roteiro: date
    paradas: list[ParadaIn]


# ──────────────────────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────────────────────

@router.post("/parada")
def adicionar_parada(parada: ParadaIn):
    """Adiciona uma única parada ao roteiro."""
    db = get_supabase()
    row = db.table("roteiros").insert(parada.model_dump(mode="json")).execute()
    return row.data[0] if row.data else {}


@router.put("/parada/{parada_id}")
def atualizar_parada(parada_id: str, parada: ParadaIn):
    """Atualiza uma parada existente."""
    db = get_supabase()
    row = (
        db.table("roteiros")
        .update(parada.model_dump(mode="json"))
        .eq("id", parada_id)
        .execute()
    )
    return row.data[0] if row.data else {}


@router.delete("/parada/{parada_id}")
def remover_parada(parada_id: str):
    """Remove uma parada do roteiro."""
    db = get_supabase()
    db.table("roteiros").delete().eq("id", parada_id).execute()
    return {"ok": True}


@router.post("/publicar")
def publicar_roteiro(payload: PublicarRoteiroIn):
    """
    Salva (ou substitui) o roteiro completo de um funcionário para
    uma data. Remove paradas anteriores e insere as novas.
    """
    db = get_supabase()

    # Remove roteiro existente do dia para esse funcionário
    db.table("roteiros").delete()\
        .eq("funcionario_id", payload.funcionario_id)\
        .eq("data_roteiro", payload.data_roteiro.isoformat())\
        .execute()

    if not payload.paradas:
        return {"ok": True, "paradas_salvas": 0}

    registros = [p.model_dump() for p in payload.paradas]
    # Garante que data_roteiro é string ISO
    for r in registros:
        r["data_roteiro"] = str(r["data_roteiro"])

    db.table("roteiros").insert(registros).execute()

    return {"ok": True, "paradas_salvas": len(registros)}


@router.get("/pendentes/{data}")
def funcionarios_sem_roteiro(data: date):
    """
    Retorna funcionários ativos que ainda não têm roteiro
    cadastrado para a data informada.
    Útil para lembrar o gestor de completar o planejamento.
    """
    db = get_supabase()

    todos = (
        db.table("funcionarios")
        .select("id, nome, equipe")
        .eq("ativo", True)
        .execute()
        .data or []
    )

    com_roteiro = set(
        r["funcionario_id"] for r in
        db.table("roteiros")
        .select("funcionario_id")
        .eq("data_roteiro", data.isoformat())
        .execute()
        .data or []
    )

    sem_roteiro = [f for f in todos if f["id"] not in com_roteiro]
    return {"data": data.isoformat(), "sem_roteiro": sem_roteiro, "total": len(sem_roteiro)}


# Rota dinâmica por último: senão captura por engano rotas estáticas
# como /roteiros/pendentes/{data} (FastAPI casa por ordem de registro).
@router.get("/{funcionario_id}/{data}")
def buscar_roteiro(funcionario_id: str, data: date):
    """Retorna as paradas do roteiro de um funcionário em uma data."""
    db = get_supabase()
    rows = (
        db.table("roteiros")
        .select("*, locais(id, nome, latitude, longitude, raio_aceitacao_m)")
        .eq("funcionario_id", funcionario_id)
        .eq("data_roteiro", data.isoformat())
        .order("ordem")
        .execute()
        .data or []
    )
    return {"funcionario_id": funcionario_id, "data": data.isoformat(), "paradas": rows}
