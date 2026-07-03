# PontoWatch

Aplicação FastAPI (backend + frontend servidos juntos, mesmo processo) que integra
o **Ponto Mais** com o **Supabase** para monitoramento de ponto e geolocalização.

---

## Estrutura

```
pontowatch/
├── app/
│   ├── main.py                    # FastAPI + scheduler + monta frontend/ como estático
│   ├── core/
│   │   ├── config.py              # Settings (lê .env)
│   │   └── database.py            # Cliente Supabase
│   ├── api/
│   │   ├── painel.py              # GET /painel/...
│   │   ├── roteiros.py            # POST/GET /roteiros/...
│   │   └── alertas.py             # GET/PATCH /alertas/...
│   └── services/
│       ├── pontomais_client.py    # Wrapper API Ponto Mais
│       ├── sync_service.py        # Sync funcionários + batidas
│       ├── comparacao_engine.py   # Motor previsto × real + Haversine
│       ├── job_diario.py          # Orquestrador do job
│       └── notificacoes.py        # Envio de e-mails
├── frontend/                      # HTML/JS estático, servido pelo próprio FastAPI
├── Procfile                       # Comando de start (Railway)
├── requirements.txt
└── .env.example
```

---

## Setup local

```bash
# 1. Clonar e criar ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
# .venv\Scripts\activate       # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com seus tokens (Ponto Mais e Supabase)

# 4. Rodar o banco de dados
# Execute o schema_supabase_ponto.sql no Supabase SQL Editor

# 5. Iniciar a aplicação (backend + frontend juntos)
uvicorn app.main:app --reload --port 8001
```

Acesse:
- http://localhost:8001/ — Frontend (painel, roteiros, mapa, etc.)
- http://localhost:8001/docs — Swagger interativo da API
- http://localhost:8001/health — Health check

---

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `PM_API_TOKEN` | Token público da API Ponto Mais (Marketplace) |
| `PM_API_BASE_URL` | URL base da API (padrão já configurado) |
| `SUPABASE_URL` | URL do seu projeto Supabase |
| `SUPABASE_SERVICE_KEY` | Chave `service_role` do Supabase |
| `JOB_HORA` | Horário do job diário, ex: `06:00` |
| `SMTP_*` | Configurações de e-mail para alertas |
| `EMAIL_RH` | Destinatário do relatório diário |

---

## Endpoints principais

### Job
| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/job/executar` | Roda o job manualmente |
| `GET` | `/job/proximo` | Quando o job roda novamente |

### Painel
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/painel/resumo?dia=YYYY-MM-DD` | KPIs do dia |
| `GET` | `/painel/monitoramento?dia=` | Tabela em tempo real |
| `GET` | `/painel/por-equipe?dia=` | Conformidade por equipe |

### Roteiros
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/roteiros/{func_id}/{data}` | Roteiro de um funcionário |
| `POST` | `/roteiros/parada` | Adiciona parada |
| `POST` | `/roteiros/publicar` | Salva roteiro completo |
| `DELETE` | `/roteiros/parada/{id}` | Remove parada |
| `GET` | `/roteiros/pendentes/{data}` | Funcionários sem roteiro |

### Alertas
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/alertas/?dia=&nivel_min=` | Lista alertas |
| `PATCH` | `/alertas/{id}/resolver` | Marca como resolvido |

---

## Deploy (Railway)

Backend e frontend são um único serviço (mesmo processo, mesma porta), então
o deploy é um só passo — não há CORS nem URLs separadas para configurar.

```bash
# 1. Instale o Railway CLI
npm install -g @railway/cli

# 2. Login e deploy
railway login
railway init
railway up

# 3. Configure as variáveis de ambiente no dashboard Railway
# Settings → Variables → adicione todas do .env
```

O `Procfile` já define o comando de start (`uvicorn app.main:app --host 0.0.0.0 --port $PORT`).
Alternativa: **Render.com** (mesma facilidade, plano gratuito disponível).

---

## Fluxo do job diário

```
06:00 ──► Sync funcionários (Ponto Mais → Supabase)
     ──► Sync batidas do dia
     ──► Motor de comparação (roteiro × batidas + Haversine)
     ──► Gera alertas na tabela `alertas`
     ──► Envia e-mail para RH com resumo
     ──► Registra log em `log_sincronizacao`
```

---

## Próximos passos sugeridos

- [ ] Autenticação JWT nos endpoints (Supabase Auth)
- [ ] Webhook Ponto Mais para receber batidas em tempo real
- [ ] Endpoint de relatório PDF (ReportLab)
- [ ] Notificação WhatsApp (Twilio ou Z-API)
- [ ] Integração com Google Maps para geocoding automático pelo CEP
