"""
Serviço de sincronização: Ponto Mais → Supabase.
Executado pelo job diário (06:00) e disponível como endpoint manual.
"""
import re
from datetime import date, datetime
from loguru import logger
from app.services.pontomais_client import PontoMaisClient
from app.core.database import get_supabase


def sincronizar_funcionarios() -> int:
    """
    Traz todos os funcionários ativos do Ponto Mais e faz upsert
    na tabela `funcionarios` do Supabase.
    Retorna a quantidade sincronizada.
    """
    db = get_supabase()

    with PontoMaisClient() as pm:
        funcionarios = pm.listar_funcionarios()

    if not funcionarios:
        logger.warning("Nenhum funcionário retornado pela API")
        return 0

    registros = []
    for f in funcionarios:
        registros.append({
            "pm_employee_id": f["id"],
            "nome": f.get("name") or f.get("full_name", ""),
            "cpf": f.get("cpf"),
            "matricula": f.get("registration_number"),
            "cargo": _nome(f.get("job_title")),
            "departamento": _nome(f.get("department")),
            "equipe": _nome(f.get("team")),
            "unidade_negocio": _nome(f.get("business_unit")),
            "email": f.get("email"),
            "ativo": f.get("active", True),
            "atualizado_em": datetime.utcnow().isoformat(),
        })

    # Upsert pelo ID do Ponto Mais (conflict em pm_employee_id)
    db.table("funcionarios").upsert(
        registros, on_conflict="pm_employee_id"
    ).execute()

    logger.info(f"Funcionários sincronizados: {len(registros)}")
    return len(registros)


def sincronizar_batidas(dia: date) -> int:
    """
    Traz todas as batidas de um dia e faz upsert na tabela
    `batidas_ponto`. Retorna a quantidade inserida/atualizada.
    Usa POST /reports/time_cards — identificação por matrícula.
    """
    db = get_supabase()

    with PontoMaisClient() as pm:
        batidas = pm.batidas_do_dia(dia)

    if not batidas:
        logger.info(f"Sem batidas para {dia}")
        return 0

    # Mapa matricula → {id: uuid, pm_employee_id: int}
    func_map = _carregar_mapa_por_matricula(db)

    registros = []
    for b in batidas:
        matricula = b.get("registration_number")
        func_info = func_map.get(str(matricula)) if matricula else None
        if not func_info:
            logger.warning(f"Matrícula '{matricula}' não encontrada — pulando batida")
            continue

        data_iso = _parse_data_pm(b.get("date"))
        hora_str = b.get("time")
        idx = b.get("time_card_index", "")
        lat, lon = _parse_geo(b.get("geolocation"))

        # ID sintético: matricula + data + hora + índice
        pm_id = f"{matricula}_{data_iso}_{hora_str}_{idx}"

        registros.append({
            "pm_time_card_id": pm_id,
            "funcionario_id": func_info["id"],
            "pm_employee_id": func_info["pm_employee_id"],
            "data_hora": _montar_datetime(data_iso, hora_str),
            "tipo": _mapear_tipo(idx),
            "latitude_real": lat,
            "longitude_real": lon,
            "endereco_registrado": b.get("original_address"),
            "dispositivo": b.get("device_description"),
        })

    if registros:
        db.table("batidas_ponto").upsert(
            registros, on_conflict="pm_time_card_id"
        ).execute()

    logger.info(f"Batidas sincronizadas para {dia}: {len(registros)}")
    return len(registros)


# ──────────────────────────────────────────────────────────────
# Auxiliares
# ──────────────────────────────────────────────────────────────

def _nome(obj) -> str | None:
    """Extrai .name de um sub-objeto da API, se existir."""
    if isinstance(obj, dict):
        return obj.get("name")
    return obj  # já é string ou None


def _float_ou_none(v) -> float | None:
    try:
        return float(v) if v is not None else None
    except (ValueError, TypeError):
        return None


def _montar_datetime(data_str: str | None, hora_str: str | None) -> str | None:
    """Combina '2025-06-20' + '08:05:00' → ISO 8601 UTC."""
    if not data_str:
        return None
    hora_str = hora_str or "00:00:00"
    return f"{data_str}T{hora_str}"


def _mapear_tipo(tipo_api: str | None) -> str:
    """
    Normaliza o time_card_index do relatório para nosso enum.
    Valores vindos da API: '1ª Entrada', '1ª Saída', '2ª Entrada', '2ª Saída'.
    """
    if not tipo_api:
        return "ENTRADA"
    t = tipo_api.lower()
    # Entradas: qualquer "Nª entrada" → ENTRADA (exceto 2ª que é retorno do intervalo)
    if "entrada" in t:
        if t.startswith("2"):
            return "INTERVALO_FIM"
        return "ENTRADA"
    # Saídas: 1ª saída = início do intervalo, última = saída final
    if "saída" in t or "saida" in t:
        if t.startswith("1"):
            return "INTERVALO_INICIO"
        return "SAIDA"
    # Fallbacks genéricos (caso a API mude)
    mapa = {
        "in": "ENTRADA",
        "out": "SAIDA",
        "interval_start": "INTERVALO_INICIO",
        "interval_end": "INTERVALO_FIM",
    }
    return mapa.get(t, "ENTRADA")


def _parse_data_pm(data_str: str | None) -> str | None:
    """Normaliza data do relatório para YYYY-MM-DD.
    Aceita ISO '2026-06-30' ou PT-BR 'Ter, 30/06/2026'.
    """
    if not data_str:
        return None
    if re.match(r"\d{4}-\d{2}-\d{2}", data_str):
        return data_str[:10]
    # Remove dia da semana se presente: "Ter, 30/06/2026" → "30/06/2026"
    limpa = re.sub(r"^[A-Za-záéíóúâêîôûãõàèìòùç]+,\s*", "", data_str, flags=re.IGNORECASE)
    try:
        return datetime.strptime(limpa.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return data_str


def _parse_geo(geo_str: str | None) -> tuple:
    """Extrai (lat, lon) de string 'lat,lng'. Retorna (None, None) se inválido."""
    if not geo_str or not isinstance(geo_str, str) or not geo_str.strip():
        return None, None
    partes = geo_str.split(",")
    if len(partes) >= 2:
        try:
            return float(partes[0].strip()), float(partes[1].strip())
        except ValueError:
            pass
    return None, None


def _carregar_mapa_por_matricula(db) -> dict:
    """Retorna {matricula: {id, pm_employee_id}} para FK lookup pelo relatório."""
    rows = db.table("funcionarios").select("id, pm_employee_id, matricula").execute()
    result = {}
    for r in (rows.data or []):
        mat = r.get("matricula")
        if mat:
            result[str(mat)] = {"id": r["id"], "pm_employee_id": r["pm_employee_id"]}
    return result
