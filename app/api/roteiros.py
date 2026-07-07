"""
Endpoints de roteiros — criação e consulta.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from app.core.database import get_supabase
from app.services.comparacao_engine import _config
from app.services.importador_roteiro import parse_planilha, montar_preview, montar_mensagem_whatsapp

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


class LinhaImportadaIn(BaseModel):
    secao: Optional[str] = None
    tecnico_texto: str
    funcionario_id: Optional[str] = None
    categoria: str   # "local" | "ausencia" | "sem_local"
    unidade_texto: Optional[str] = None
    local_id: Optional[str] = None
    motivo_ausencia: Optional[str] = None
    atividade_texto: Optional[str] = None
    os_texto: Optional[str] = None


class ImportarConfirmarIn(BaseModel):
    data_roteiro: date
    linhas: list[LinhaImportadaIn]


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


@router.post("/importar/preview")
async def importar_preview(arquivo: UploadFile = File(...), data_roteiro: date = Form(...)):
    """
    Lê a planilha (CSV) usada hoje pelos coordenadores de RJ/SP e devolve,
    linha a linha, a classificação (local/ausência/sem local) e os
    casamentos de técnico/local encontrados — sem gravar nada ainda. A tela
    de conferência do frontend usa isso para montar os selects antes de
    publicar.
    """
    conteudo = await arquivo.read()
    linhas = parse_planilha(conteudo, arquivo.filename or "")

    db = get_supabase()
    funcionarios = db.table("funcionarios").select("id, nome").eq("ativo", True).execute().data or []
    locais = db.table("locais").select("id, nome").eq("ativo", True).execute().data or []

    preview = montar_preview(linhas, funcionarios, locais)
    return {"data_roteiro": data_roteiro.isoformat(), "total": len(preview), "linhas": preview}


@router.post("/importar/confirmar")
def importar_confirmar(payload: ImportarConfirmarIn):
    """
    Grava o resultado já conferido/editado pelo usuário na tela de
    importação: uma parada (horário padrão da empresa) por técnico com
    local resolvido, ou uma ausência justificada em `presencas_dia` por
    técnico marcado como Férias/Atestado/etc. Linhas "sem local" (ex.:
    trabalho interno) não geram nada — a pessoa cai no fluxo padrão do job
    diário. Linhas sem `funcionario_id` (técnico que ainda não existe no
    Ponto Mais) também não geram registro no banco — mas ainda entram na
    mensagem de WhatsApp (ver `montar_mensagem_whatsapp`), já que a pessoa
    precisa saber onde trabalhar mesmo sem cadastro pra rastrear o ponto.
    """
    db = get_supabase()
    hora_entrada = _config(db, "horario_padrao_entrada", "08:00")
    hora_saida = _config(db, "horario_padrao_saida", "17:48")
    tolerancia = int(_config(db, "tolerancia_padrao_min", "15"))
    data_iso = payload.data_roteiro.isoformat()

    roteiros_publicados = ausencias_registradas = ignorados = 0

    for linha in payload.linhas:
        if not linha.funcionario_id or linha.categoria == "sem_local":
            ignorados += 1
            continue

        if linha.categoria == "local":
            if not linha.local_id:
                ignorados += 1
                continue
            observacao = linha.atividade_texto or None
            if linha.os_texto:
                observacao = f"{observacao} (OS: {linha.os_texto})" if observacao else f"OS: {linha.os_texto}"

            db.table("roteiros").delete() \
                .eq("funcionario_id", linha.funcionario_id) \
                .eq("data_roteiro", data_iso) \
                .execute()
            db.table("roteiros").insert({
                "funcionario_id": linha.funcionario_id,
                "data_roteiro": data_iso,
                "ordem": 1,
                "local_id": linha.local_id,
                "hora_prevista_entrada": hora_entrada,
                "hora_prevista_saida": hora_saida,
                "tolerancia_min": tolerancia,
                "observacao": observacao,
            }).execute()
            roteiros_publicados += 1

        elif linha.categoria == "ausencia":
            db.table("presencas_dia").upsert({
                "funcionario_id": linha.funcionario_id,
                "data_referencia": data_iso,
                "tem_roteiro": False,
                "bateu_ponto": False,
                "status_padrao": "JUSTIFICADA",
                "motivo_ausencia": linha.motivo_ausencia or "Ausência justificada",
            }, on_conflict="funcionario_id,data_referencia").execute()
            ausencias_registradas += 1

        else:
            ignorados += 1

    local_ids = {l.local_id for l in payload.linhas if l.funcionario_id and l.categoria == "local" and l.local_id}
    nomes_locais = {}
    if local_ids:
        rows = db.table("locais").select("id, nome").in_("id", list(local_ids)).execute().data or []
        nomes_locais = {r["id"]: r["nome"] for r in rows}

    mensagem = montar_mensagem_whatsapp(
        payload.data_roteiro,
        [l.model_dump() for l in payload.linhas],
        nomes_locais,
    )

    return {
        "ok": True,
        "roteiros_publicados": roteiros_publicados,
        "ausencias_registradas": ausencias_registradas,
        "ignorados": ignorados,
        "mensagem_whatsapp": mensagem,
    }


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
