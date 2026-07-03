/**
 * config.js
 *
 * Frontend e backend são servidos pelo mesmo processo FastAPI
 * (StaticFiles montado em app/main.py), então a API sempre está
 * na mesma origem — não precisa editar nada antes do deploy.
 */
window.PONTOWATCH_API_URL = window.location.origin;
