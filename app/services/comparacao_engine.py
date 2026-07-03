"""
Motor de comparação: roteiro previsto × batidas reais.

Para cada funcionário e cada parada do dia:
  1. Busca a batida de entrada mais próxima do horário previsto
  2. Calcula distância GPS entre batida e local esperado (Haversine)
  3. Determina status: CONFORME | ATRASO | AUSENTE | FORA_DO_LOCAL | PARCIAL
  4. Persiste na tabela `comparacoes` e gera alertas
"""
import math
from datetime import date, datetime, time, timedelta
from loguru import logger
from app.core.database import get_supabase


# ──────────────────────────────────────────────────────────────
# Haversine
# ──────────────────────────────────────────────────────────────

def distancia_metros(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calcula a distância entre dois pontos geográficos em metros.
    Fórmula de Haversine — precisa o suficiente para distâncias curtas.
    """
    R = 6_371_000  # raio da Terra em metros
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ──────────────────────────────────────────────────────────────
# Engine principal
# ──────────────────────────────────────────────────────────────

def processar_dia(dia: date) -> dict:
    """
    Processa todas as comparações do dia informado.
    Retorna um resumo com contadores por status.
    """
    db = get_supabase()
    resumo = {"conformes": 0, "atrasos": 0, "ausentes": 0, "fora_do_local": 0, "erros": 0}

    # 1. Busca todos os roteiros do dia
    roteiros = (
        db.table("roteiros")
        .select("*, locais(*), funcionarios(id, nome)")
        .eq("data_roteiro", dia.isoformat())
        .execute()
        .data or []
    )

    if not roteiros:
        logger.info(f"Nenhum roteiro cadastrado para {dia}")
        return resumo

    # 2. Busca todas as batidas do dia em memória (evita N queries)
    batidas_raw = (
        db.table("batidas_ponto")
        .select("*")
        .gte("data_hora", f"{dia.isoformat()}T00:00:00")
        .lte("data_hora", f"{dia.isoformat()}T23:59:59")
        .execute()
        .data or []
    )

    # Agrupa batidas por funcionário para lookup rápido
    batidas_por_func: dict[str, list[dict]] = {}
    for b in batidas_raw:
        batidas_por_func.setdefault(b["funcionario_id"], []).append(b)

    # 3. Para cada parada do roteiro, processa a comparação
    comparacoes = []
    alertas = []

    for roteiro in roteiros:
        try:
            comp, alert_list = _comparar_parada(roteiro, batidas_por_func, dia)
            comparacoes.append(comp)
            alertas.extend(alert_list)
            resumo[_status_para_chave(comp["status_presenca"])] += 1
        except Exception as e:
            logger.error(f"Erro ao processar roteiro {roteiro['id']}: {e}")
            resumo["erros"] += 1

    # 4. Persiste comparações e alertas
    if comparacoes:
        db.table("comparacoes").upsert(
            comparacoes, on_conflict="roteiro_id"
        ).execute()

    if alertas:
        db.table("alertas").insert(alertas).execute()

    logger.info(f"Dia {dia} processado: {resumo}")
    return resumo


# ──────────────────────────────────────────────────────────────
# Presença geral (independente de roteiro)
# ──────────────────────────────────────────────────────────────

def processar_presenca_dia(dia: date) -> dict:
    """
    Gera um registro de presença (bateu ponto ou não) para TODOS os
    funcionários ativos no dia informado, independente de terem roteiro
    cadastrado. Complementa `processar_dia()`, que só avalia conformidade
    de local para quem tem roteiro.
    """
    db = get_supabase()

    funcionarios = db.table("funcionarios").select("id").eq("ativo", True).execute().data or []

    batidas_raw = (
        db.table("batidas_ponto")
        .select("funcionario_id, data_hora")
        .gte("data_hora", f"{dia.isoformat()}T00:00:00")
        .lte("data_hora", f"{dia.isoformat()}T23:59:59")
        .execute()
        .data or []
    )
    batidas_por_func: dict[str, list[str]] = {}
    for b in batidas_raw:
        batidas_por_func.setdefault(b["funcionario_id"], []).append(b["data_hora"])

    roteiros_hoje = (
        db.table("roteiros")
        .select("funcionario_id")
        .eq("data_roteiro", dia.isoformat())
        .execute()
        .data or []
    )
    funcs_com_roteiro = {r["funcionario_id"] for r in roteiros_hoje}

    registros = []
    for f in funcionarios:
        fid = f["id"]
        horarios = sorted(batidas_por_func.get(fid, []))
        registros.append({
            "funcionario_id":  fid,
            "data_referencia": dia.isoformat(),
            "tem_roteiro":     fid in funcs_com_roteiro,
            "bateu_ponto":     len(horarios) > 0,
            "primeira_batida": _hora_str(horarios[0]) if horarios else None,
            "ultima_batida":   _hora_str(horarios[-1]) if horarios else None,
            "total_batidas":   len(horarios),
        })

    if registros:
        db.table("presencas_dia").upsert(
            registros, on_conflict="funcionario_id,data_referencia"
        ).execute()

    presentes = sum(1 for r in registros if r["bateu_ponto"])
    return {
        "total": len(registros),
        "presentes": presentes,
        "ausentes": len(registros) - presentes,
    }


def _hora_str(data_hora_iso: str) -> str | None:
    try:
        dh = datetime.fromisoformat(data_hora_iso)
        return dh.time().isoformat()
    except Exception:
        return None


# ──────────────────────────────────────────────────────────────
# Lógica por parada
# ──────────────────────────────────────────────────────────────

def _comparar_parada(
    roteiro: dict,
    batidas_por_func: dict[str, list[dict]],
    dia: date,
) -> tuple[dict, list[dict]]:

    func_id   = roteiro["funcionario_id"]
    local     = roteiro["locais"]
    func_nome = roteiro["funcionarios"]["nome"]
    local_nome = local["nome"]

    hora_prev_entrada = _parse_time(roteiro["hora_prevista_entrada"])
    hora_prev_saida   = _parse_time(roteiro["hora_prevista_saida"])
    tolerancia_min    = roteiro.get("tolerancia_min") or 15
    raio_m            = local.get("raio_aceitacao_m") or 200
    lat_ref           = local.get("latitude")
    lng_ref           = local.get("longitude")

    batidas_func = batidas_por_func.get(func_id, [])

    # Encontra a batida de ENTRADA mais próxima da hora prevista
    bat_entrada = _batida_mais_proxima(batidas_func, dia, hora_prev_entrada, tipos=["ENTRADA"])
    bat_saida   = _batida_mais_proxima(batidas_func, dia, hora_prev_saida,   tipos=["SAIDA"])

    # ── Calcula horários e atrasos ──
    hora_real_entrada = None
    hora_real_saida   = None
    atraso_entrada    = None
    antecip_saida     = None

    if bat_entrada:
        hora_real_entrada = _hora_da_batida(bat_entrada)
        atraso_entrada = _diff_minutos(hora_prev_entrada, hora_real_entrada)

    if bat_saida:
        hora_real_saida = _hora_da_batida(bat_saida)
        antecip_saida = _diff_minutos(hora_real_saida, hora_prev_saida)  # positivo = saiu antes

    # ── Calcula distância GPS ──
    dist_entrada = None
    dist_saida   = None
    no_local_entrada = None
    no_local_saida   = None

    if bat_entrada and lat_ref and lng_ref:
        lat_r = bat_entrada.get("latitude_real")
        lng_r = bat_entrada.get("longitude_real")
        if lat_r and lng_r:
            dist_entrada = round(distancia_metros(lat_ref, lng_ref, float(lat_r), float(lng_r)), 2)
            no_local_entrada = dist_entrada <= raio_m

    if bat_saida and lat_ref and lng_ref:
        lat_r = bat_saida.get("latitude_real")
        lng_r = bat_saida.get("longitude_real")
        if lat_r and lng_r:
            dist_saida = round(distancia_metros(lat_ref, lng_ref, float(lat_r), float(lng_r)), 2)
            no_local_saida = dist_saida <= raio_m

    # ── Determina status ──
    status_presenca = _calcular_status(
        bat_entrada, atraso_entrada, tolerancia_min, no_local_entrada
    )
    status_geo = _calcular_status_geo(no_local_entrada, bat_entrada)

    # ── Monta registro de comparação ──
    comp = {
        "roteiro_id":              roteiro["id"],
        "funcionario_id":          func_id,
        "local_id":                local["id"],
        "data_referencia":         dia.isoformat(),
        "batida_entrada_id":       bat_entrada["id"] if bat_entrada else None,
        "batida_saida_id":         bat_saida["id"]   if bat_saida   else None,
        "hora_prevista_entrada":   str(hora_prev_entrada),
        "hora_real_entrada":       str(hora_real_entrada) if hora_real_entrada else None,
        "hora_prevista_saida":     str(hora_prev_saida),
        "hora_real_saida":         str(hora_real_saida)   if hora_real_saida   else None,
        "minutos_atraso_entrada":  atraso_entrada,
        "minutos_saida_antecip":   antecip_saida,
        "distancia_entrada_m":     dist_entrada,
        "distancia_saida_m":       dist_saida,
        "dentro_raio_entrada":     no_local_entrada,
        "dentro_raio_saida":       no_local_saida,
        "status_presenca":         status_presenca,
        "status_geo":              status_geo,
    }

    # ── Gera alertas ──
    alertas = _gerar_alertas(
        comp, func_id, func_nome, local_nome, dia,
        atraso_entrada, dist_entrada, raio_m, bat_entrada
    )

    return comp, alertas


# ──────────────────────────────────────────────────────────────
# Determinação de status
# ──────────────────────────────────────────────────────────────

def _calcular_status(bat_entrada, atraso_min, tolerancia_min, no_local) -> str:
    if not bat_entrada:
        return "AUSENTE"
    if no_local is False:
        return "FORA_DO_LOCAL"
    if atraso_min and atraso_min > tolerancia_min:
        return "ATRASO"
    return "CONFORME"


def _calcular_status_geo(no_local, bat_entrada) -> str | None:
    if not bat_entrada:
        return None
    if bat_entrada.get("latitude_real") is None:
        return "SEM_GPS"
    return "OK" if no_local else "DIVERGENTE"


# ──────────────────────────────────────────────────────────────
# Geração de alertas
# ──────────────────────────────────────────────────────────────

def _gerar_alertas(
    comp, func_id, func_nome, local_nome, dia,
    atraso_min, dist_entrada, raio_m, bat_entrada
) -> list[dict]:

    alertas = []
    comp_id = None  # será linkado após insert; por ora deixamos None

    def alerta(tipo, nivel, desc):
        return {
            "comparacao_id":  comp_id,
            "funcionario_id": func_id,
            "data_referencia": dia.isoformat(),
            "tipo_alerta":    tipo,
            "nivel":          nivel,
            "descricao":      desc,
            "enviado":        False,
        }

    if comp["status_presenca"] == "AUSENTE":
        alertas.append(alerta(
            "AUSENCIA", 3,
            f"{func_nome} não registrou presença em '{local_nome}' "
            f"(previsto: {comp['hora_prevista_entrada']})."
        ))

    elif comp["status_presenca"] == "FORA_DO_LOCAL":
        alertas.append(alerta(
            "FORA_DO_LOCAL", 2,
            f"{func_nome} bateu ponto a {dist_entrada:.0f}m de '{local_nome}' "
            f"(raio aceito: {raio_m}m)."
        ))

    elif comp["status_presenca"] == "ATRASO":
        alertas.append(alerta(
            "ATRASO", 1 if atraso_min <= 30 else 2,
            f"{func_nome} chegou com {atraso_min} min de atraso em '{local_nome}'."
        ))

    if not bat_entrada and comp["status_geo"] == "SEM_GPS":
        alertas.append(alerta(
            "SEM_BATIDA", 2,
            f"Batida de {func_nome} sem dados de GPS em '{local_nome}'."
        ))

    return alertas


# ──────────────────────────────────────────────────────────────
# Auxiliares de tempo
# ──────────────────────────────────────────────────────────────

def _parse_time(t) -> time:
    if isinstance(t, time):
        return t
    if isinstance(t, str):
        parts = t.split(":")
        return time(int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0)
    raise ValueError(f"Não foi possível converter '{t}' em time")


def _hora_da_batida(batida: dict) -> time | None:
    dh = batida.get("data_hora")
    if not dh:
        return None
    try:
        return datetime.fromisoformat(dh).time()
    except Exception:
        return None


def _diff_minutos(esperado: time, real: time) -> int | None:
    """Retorna real − esperado em minutos. Positivo = atrasado."""
    if not esperado or not real:
        return None
    base = datetime(2000, 1, 1)
    return int((
        datetime.combine(base.date(), real) - datetime.combine(base.date(), esperado)
    ).total_seconds() / 60)


def _batida_mais_proxima(
    batidas: list[dict],
    dia: date,
    hora_ref: time,
    tipos: list[str],
    janela_horas: int = 2,
) -> dict | None:
    """
    Dentre as batidas do tipo informado, retorna a mais próxima
    de hora_ref dentro de uma janela de ±janela_horas.
    """
    ref_dt = datetime.combine(dia, hora_ref)
    candidatas = []

    for b in batidas:
        if b.get("tipo") not in tipos:
            continue
        bat_dt_str = b.get("data_hora")
        if not bat_dt_str:
            continue
        try:
            bat_dt = datetime.fromisoformat(bat_dt_str)
        except Exception:
            continue
        # data_hora vem do Supabase como TIMESTAMPTZ (aware), mas foi gravado
        # como horário local "naive" (ver _montar_datetime em sync_service.py).
        # Remove o tzinfo para comparar como wall-clock local, não UTC real.
        if bat_dt.tzinfo is not None:
            bat_dt = bat_dt.replace(tzinfo=None)
        diff = abs((bat_dt - ref_dt).total_seconds()) / 3600
        if diff <= janela_horas:
            candidatas.append((diff, b))

    if not candidatas:
        return None
    candidatas.sort(key=lambda x: x[0])
    return candidatas[0][1]


def _status_para_chave(status: str) -> str:
    return {
        "CONFORME":     "conformes",
        "ATRASO":       "atrasos",
        "AUSENTE":      "ausentes",
        "FORA_DO_LOCAL":"fora_do_local",
        "PARCIAL":      "conformes",
    }.get(status, "erros")
