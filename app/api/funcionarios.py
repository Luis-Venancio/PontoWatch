"""
Endpoints de funcionários — consulta dos dados sincronizados do Ponto Mais.
(Somente leitura — a escrita é feita via sync_service.py)
"""
from typing import Optional
from fastapi import APIRouter, Query
from app.core.database import get_supabase

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])


@router.get("", include_in_schema=False)
@router.get("/")
def listar_funcionarios(
    apenas_ativos: bool = Query(default=True),
    equipe: Optional[str] = Query(default=None),
    busca: Optional[str] = Query(default=None, description="Filtra por nome ou matrícula"),
):
    """
    Lista todos os funcionários sincronizados do Ponto Mais.
    Suporta filtro por status, equipe e busca por nome/matrícula.
    """
    db = get_supabase()
    q = db.table("funcionarios").select(
        "id, pm_employee_id, nome, cpf, matricula, cargo, departamento, equipe, unidade_negocio, email, ativo, atualizado_em"
    ).order("nome")

    if apenas_ativos:
        q = q.eq("ativo", True)
    if equipe:
        q = q.eq("equipe", equipe)

    rows = q.execute().data or []

    if busca:
        busca_lower = busca.lower()
        rows = [
            r for r in rows
            if busca_lower in (r.get("nome") or "").lower()
            or busca_lower in (r.get("matricula") or "").lower()
        ]

    return {"funcionarios": rows, "total": len(rows)}


@router.get("/equipes")
def listar_equipes():
    """Retorna todas as equipes únicas cadastradas."""
    db = get_supabase()
    rows = db.table("funcionarios").select("equipe").eq("ativo", True).execute().data or []
    equipes = sorted({r["equipe"] for r in rows if r.get("equipe")})
    return {"equipes": equipes}


@router.get("/{funcionario_id}")
def buscar_funcionario(funcionario_id: str):
    """Retorna os dados de um funcionário pelo UUID interno."""
    from fastapi import HTTPException
    db = get_supabase()
    rows = (
        db.table("funcionarios")
        .select("*")
        .eq("id", funcionario_id)
        .execute()
        .data or []
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return rows[0]
