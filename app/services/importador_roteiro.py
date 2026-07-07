"""
Importação de roteiro a partir da planilha usada hoje pelos coordenadores
(RJ/SP) — colunas livres: TÉCNICO;Unidade;Atividade;OS, sem horário, com
seções (ex.: "Roteiro da supervisão") e linhas que na verdade são ausência
("Férias", "Atestado") ou trabalho interno sem cliente ("Empresa").

Não decide casamentos ambíguos sozinho — sempre devolve os candidatos para
confirmação manual na tela de importação (ver app/api/roteiros.py).
"""
import csv
import io
import re
import unicodedata

AUSENCIA_TEXTOS = {
    "ferias": "Férias",
    "atestado": "Atestado",
    "licenca": "Licença",
    "licenca medica": "Licença médica",
    "folga": "Folga",
}
SEM_LOCAL_TEXTOS = {"empresa"}


def _normalizar(texto: str) -> str:
    """Minúsculo, sem acento, sem pontuação — usado tanto para classificar
    a Unidade quanto para casar nomes de técnico/local."""
    texto = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"\(.*?\)", " ", texto)  # remove "(Noturno)", "(Diurno)" etc.
    texto = re.sub(r"[^a-z0-9 ]", " ", texto.lower())
    return re.sub(r"\s+", " ", texto).strip()


def classificar_unidade(unidade_texto: str) -> str:
    """Retorna "ausencia" | "sem_local" | "local"."""
    normalizado = _normalizar(unidade_texto)
    if normalizado in AUSENCIA_TEXTOS:
        return "ausencia"
    if normalizado in SEM_LOCAL_TEXTOS:
        return "sem_local"
    return "local"


def motivo_ausencia(unidade_texto: str) -> str:
    return AUSENCIA_TEXTOS.get(_normalizar(unidade_texto), unidade_texto.strip())


def _abrir_texto(conteudo: bytes) -> str:
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            return conteudo.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError("Não foi possível detectar a codificação do arquivo (tentei utf-8 e latin-1)")


def parse_planilha(conteudo: bytes) -> list[dict]:
    """
    Lê o CSV bruto e devolve uma linha por técnico/atividade, já com a seção
    atual anotada (ex.: "Técnicos", "Roteiro da supervisão"). Pula a linha de
    título, o cabeçalho, linhas em branco e linhas que são só um marcador de
    seção nova (só a 1ª coluna preenchida).
    """
    texto = _abrir_texto(conteudo)
    amostra = texto.splitlines()[1] if len(texto.splitlines()) > 1 else texto.splitlines()[0]
    delimitador = ";" if amostra.count(";") > amostra.count(",") else ","

    leitor = csv.reader(io.StringIO(texto), delimiter=delimitador)
    linhas_brutas = list(leitor)
    if not linhas_brutas:
        return []

    resultado = []
    secao_atual = "Técnicos"
    inicio = 0

    # A 1ª linha é sempre um título solto (ex.: "Roteiro técnicos | RIO DE
    # JANEIRO - 07/07/2026"). A 2ª costuma ser o cabeçalho de colunas — pula
    # se bater com o nome esperado, mas não trava se vier diferente.
    if linhas_brutas and linhas_brutas[0]:
        inicio = 1
    if len(linhas_brutas) > 1 and _normalizar(linhas_brutas[1][0] if linhas_brutas[1] else "") in ("tecnico",):
        inicio = 2

    for linha in linhas_brutas[inicio:]:
        campos = [c.strip() for c in linha] + [""] * 4
        tecnico, unidade, atividade, os_num = campos[0], campos[1], campos[2], campos[3]

        if not any([tecnico, unidade, atividade, os_num]):
            continue  # linha em branco (separador de seção)

        if tecnico and not unidade and not atividade and not os_num:
            secao_atual = tecnico  # cabeçalho de nova seção, ex. "Roteiro da supervisão"
            continue

        if not tecnico:
            continue

        resultado.append({
            "secao": secao_atual,
            "tecnico_texto": tecnico,
            "unidade_texto": unidade,
            "atividade_texto": atividade,
            "os_texto": os_num,
        })

    return resultado


def _tokens(texto: str) -> set[str]:
    return set(_normalizar(texto).split())


def casar_texto(texto: str, candidatos: list[dict], campo_nome: str = "nome", max_candidatos: int = 5) -> dict:
    """
    Casa `texto` (livre) contra `candidatos` (lista de dicts com `campo_nome`)
    por subconjunto de tokens nos dois sentidos. Só devolve `match` quando há
    exatamente 1 candidato com melhor pontuação e nenhum empate — senão
    devolve os melhores `candidatos` para escolha manual (nunca decide
    sozinho em caso de ambiguidade).
    """
    tokens_busca = _tokens(texto)
    if not tokens_busca:
        return {"match": None, "candidatos": []}

    pontuados = []
    for c in candidatos:
        tokens_cand = _tokens(c[campo_nome])
        if not tokens_cand:
            continue
        intersecao = tokens_busca & tokens_cand
        if not intersecao:
            continue
        # subconjunto perfeito em qualquer direção pontua mais alto
        subconjunto = tokens_busca <= tokens_cand or tokens_cand <= tokens_busca
        pontuacao = len(intersecao) / max(len(tokens_busca), len(tokens_cand))
        if subconjunto:
            pontuacao += 1.0
        pontuados.append((pontuacao, c))

    if not pontuados:
        return {"match": None, "candidatos": []}

    pontuados.sort(key=lambda x: x[0], reverse=True)
    melhor_pontuacao = pontuados[0][0]
    melhores = [c for p, c in pontuados if p == melhor_pontuacao]

    if len(melhores) == 1 and melhor_pontuacao >= 1.0:
        return {"match": melhores[0], "candidatos": []}

    return {"match": None, "candidatos": [c for _, c in pontuados[:max_candidatos]]}


def montar_preview(linhas: list[dict], funcionarios: list[dict], locais: list[dict]) -> list[dict]:
    """Combina classificação + casamento por linha, pronto para a tela de conferência."""
    preview = []
    for linha in linhas:
        casamento_func = casar_texto(linha["tecnico_texto"], funcionarios)
        categoria = classificar_unidade(linha["unidade_texto"])

        item = {
            "secao": linha["secao"],
            "tecnico_texto": linha["tecnico_texto"],
            "funcionario_match": casamento_func["match"],
            "funcionario_candidatos": casamento_func["candidatos"],
            "categoria": categoria,
            "unidade_texto": linha["unidade_texto"],
            "atividade_texto": linha["atividade_texto"],
            "os_texto": linha["os_texto"],
            "local_match": None,
            "local_candidatos": [],
            "motivo_ausencia": None,
        }

        if categoria == "local":
            casamento_local = casar_texto(linha["unidade_texto"], locais)
            item["local_match"] = casamento_local["match"]
            item["local_candidatos"] = casamento_local["candidatos"]
        elif categoria == "ausencia":
            item["motivo_ausencia"] = motivo_ausencia(linha["unidade_texto"])

        preview.append(item)

    return preview
