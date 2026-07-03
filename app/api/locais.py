"""
Endpoints de locais de atendimento — CRUD completo.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.database import get_supabase

router = APIRouter(prefix="/locais", tags=["Locais"])


# ──────────────────────────────────────────────────────────────
# Schema
# ──────────────────────────────────────────────────────────────

class LocalIn(BaseModel):
    nome: str
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    raio_aceitacao_m: Optional[int] = 200
    ativo: Optional[bool] = True
    observacao: Optional[str] = None


# ──────────────────────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────────────────────

@router.get("/")
def listar_locais(apenas_ativos: bool = True):
    """Lista todos os locais de atendimento cadastrados."""
    db = get_supabase()
    q = db.table("locais").select("*").order("nome")
    if apenas_ativos:
        q = q.eq("ativo", True)
    rows = q.execute().data or []
    return {"locais": rows, "total": len(rows)}


@router.get("/{local_id}")
def buscar_local(local_id: str):
    """Retorna um local pelo ID."""
    db = get_supabase()
    rows = db.table("locais").select("*").eq("id", local_id).execute().data or []
    if not rows:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return rows[0]


@router.post("/", status_code=201)
def criar_local(local: LocalIn):
    """Cria um novo local de atendimento."""
    db = get_supabase()
    row = db.table("locais").insert(local.model_dump()).execute()
    return row.data[0] if row.data else {}


@router.put("/{local_id}")
def atualizar_local(local_id: str, local: LocalIn):
    """Atualiza os dados de um local existente."""
    db = get_supabase()
    rows = db.table("locais").select("id").eq("id", local_id).execute().data or []
    if not rows:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    row = db.table("locais").update(local.model_dump()).eq("id", local_id).execute()
    return row.data[0] if row.data else {}


@router.delete("/{local_id}")
def remover_local(local_id: str):
    """
    Desativa um local (soft delete) para preservar histórico.
    Use ?forcar=true para remoção permanente.
    """
    db = get_supabase()
    db.table("locais").update({"ativo": False}).eq("id", local_id).execute()
    return {"ok": True, "mensagem": "Local desativado com sucesso"}


@router.delete("/{local_id}/permanente")
def remover_local_permanente(local_id: str):
    """Remove permanentemente um local. Use com cuidado — não pode ser desfeito."""
    db = get_supabase()
    db.table("locais").delete().eq("id", local_id).execute()
    return {"ok": True, "mensagem": "Local removido permanentemente"}
