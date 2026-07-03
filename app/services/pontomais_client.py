"""
Cliente para a API REST do Ponto Mais.
Documentação: https://documenter.getpostman.com/view/4785048/RWMCvVxN
"""
import httpx
from datetime import date
from loguru import logger
from app.core.config import get_settings


class PontoMaisClient:
    """
    Wrapper sobre a API do Ponto Mais.

    Autenticação: token público obtido em
    app.pontomais.com.br → Marketplace → API Pontomais.
    """

    def __init__(self):
        s = get_settings()
        self._base = s.pm_api_base_url.rstrip("/")
        self._headers = {
            "access-token": s.pm_api_token,
            "Content-Type": "application/json",
        }
        # Timeout generoso pois a API pode ser lenta em bases grandes
        self._client = httpx.Client(headers=self._headers, timeout=30)

    # ──────────────────────────────────────────────────────────
    # Auxiliar
    # ──────────────────────────────────────────────────────────

    def _get(self, endpoint: str, params: dict = None) -> dict:
        url = f"{self._base}/{endpoint.lstrip('/')}"
        logger.debug(f"GET {url} params={params}")
        r = self._client.get(url, params=params)
        r.raise_for_status()
        return r.json()

    def _post(self, endpoint: str, body: dict) -> dict:
        url = f"{self._base}/{endpoint.lstrip('/')}"
        logger.debug(f"POST {url}")
        r = self._client.post(url, json=body)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def _extrair_lista(data) -> list:
        """
        A API do Ponto Mais retorna o array dentro de uma chave nomeada
        pelo recurso (ex: {"employees": [...], "meta": {...}}), não em
        "data". Pega a primeira chave cujo valor é uma lista.
        """
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for chave, valor in data.items():
                if chave != "meta" and isinstance(valor, list):
                    return valor
        return []

    def _paginate(self, endpoint: str, params: dict = None) -> list:
        """
        Percorre todas as páginas de um endpoint paginado.
        O Ponto Mais usa page + per_page nos query params.
        """
        params = params or {}
        params.setdefault("per_page", 100)
        results = []
        page = 1
        while True:
            params["page"] = page
            data = self._get(endpoint, params)

            items = self._extrair_lista(data)
            if not items:
                break
            results.extend(items)

            # Se veio menos que per_page, chegamos ao fim
            if len(items) < params["per_page"]:
                break
            page += 1

        logger.info(f"  {endpoint}: {len(results)} registros carregados")
        return results

    # ──────────────────────────────────────────────────────────
    # Endpoints
    # ──────────────────────────────────────────────────────────

    def listar_funcionarios(self, apenas_ativos: bool = True) -> list[dict]:
        """
        GET /employees
        Retorna todos os colaboradores cadastrados.
        """
        params = {"active": "true"} if apenas_ativos else {}
        return self._paginate("/employees", params)

    def listar_batidas(self, data_inicio: date, data_fim: date) -> list[dict]:
        """
        POST /reports/time_cards
        Relatório de registros de ponto no intervalo informado.
        Retorna lista de dicts com: registration_number, date, time,
        time_card_index, original_address, geolocation, device_description.
        """
        body = {
            "report": {
                "start_date": data_inicio.isoformat(),
                "end_date": data_fim.isoformat(),
                "group_by": "employee",
                "columns": (
                    "employee_name,registration_number,date,time,"
                    "time_card_index,original_address,geolocation,"
                    "device_description,source"
                ),
                "format": "json",
            }
        }
        data = self._post("/reports/time_cards", body)
        return self._extrair_registros_relatorio(data)

    @staticmethod
    def _extrair_registros_relatorio(data: dict) -> list[dict]:
        """
        Os endpoints /reports/* (ex: time_cards) retornam a estrutura:
        {"heading": {...}, "data": [ [ {"header": {...}, "data": [<registros>],
        "footer": ..., "totals": [...]}, ... ] ], "meta": {...}}
        onde o array externo em "data" agrupa por página e o array interno
        agrupa por colaborador/equipe (conforme group_by). Achata tudo para
        uma lista simples de registros.
        """
        registros = []
        paginas = data.get("data", []) if isinstance(data, dict) else []
        for pagina in paginas:
            if not isinstance(pagina, list):
                continue
            for bloco in pagina:
                if isinstance(bloco, dict):
                    registros.extend(bloco.get("data") or [])
        return registros

    def batidas_do_dia(self, dia: date) -> list[dict]:
        return self.listar_batidas(dia, dia)

    def listar_turnos(self) -> list[dict]:
        """GET /work_shifts — escalas cadastradas no Ponto Mais."""
        return self._paginate("/work_shifts")

    def listar_departamentos(self) -> list[dict]:
        """GET /departments"""
        return self._paginate("/departments")

    def listar_equipes(self) -> list[dict]:
        """GET /teams"""
        return self._paginate("/teams")

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
