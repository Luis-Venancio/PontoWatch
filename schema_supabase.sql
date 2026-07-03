-- ============================================================
-- SCHEMA: Monitoramento de Ponto — Supabase / PostgreSQL
-- Projeto: PontoWatch — Automação RH × Ponto Mais
-- Como usar: cole este arquivo inteiro no Supabase SQL Editor
--            (Menu lateral → SQL Editor → New Query) e execute.
-- ============================================================


-- ============================================================
-- EXTENSÕES
-- ============================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS earthdistance CASCADE;
CREATE EXTENSION IF NOT EXISTS cube CASCADE;


-- ============================================================
-- 1. FUNCIONÁRIOS
--    Espelho dos dados do Ponto Mais, sincronizado via API
-- ============================================================
CREATE TABLE IF NOT EXISTS funcionarios (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    pm_employee_id   INTEGER     UNIQUE NOT NULL,   -- ID interno do Ponto Mais
    nome             TEXT        NOT NULL,
    cpf              TEXT,
    matricula        TEXT,
    cargo            TEXT,
    departamento     TEXT,
    equipe           TEXT,
    unidade_negocio  TEXT,
    email            TEXT,
    ativo            BOOLEAN     DEFAULT TRUE,
    criado_em        TIMESTAMPTZ DEFAULT NOW(),
    atualizado_em    TIMESTAMPTZ DEFAULT NOW()
);


-- ============================================================
-- 2. LOCAIS DE ATENDIMENTO
--    Cadastro interno — base para comparação de geolocalização
-- ============================================================
CREATE TABLE IF NOT EXISTS locais (
    id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    nome              TEXT        NOT NULL,       -- ex: "Cliente ABC - Unidade Centro"
    endereco          TEXT,
    cidade            TEXT,
    estado            TEXT,
    cep               TEXT,
    latitude          NUMERIC(10, 7),             -- nullable: pode ser preenchido depois
    longitude         NUMERIC(10, 7),
    raio_aceitacao_m  INTEGER     NOT NULL DEFAULT 200,  -- margem em metros
    ativo             BOOLEAN     DEFAULT TRUE,
    observacao        TEXT,
    criado_em         TIMESTAMPTZ DEFAULT NOW()
);


-- ============================================================
-- 3. ROTEIROS DIÁRIOS
--    Define onde cada funcionário deve estar em cada dia
--    Um funcionário pode ter múltiplas paradas por dia
-- ============================================================
CREATE TABLE IF NOT EXISTS roteiros (
    id                     UUID      PRIMARY KEY DEFAULT gen_random_uuid(),
    funcionario_id         UUID      NOT NULL REFERENCES funcionarios(id) ON DELETE CASCADE,
    data_roteiro           DATE      NOT NULL,
    ordem                  SMALLINT  NOT NULL DEFAULT 1,  -- sequência de visitas no dia
    local_id               UUID      NOT NULL REFERENCES locais(id),
    hora_prevista_entrada  TIME      NOT NULL,
    hora_prevista_saida    TIME      NOT NULL,
    tolerancia_min         SMALLINT  DEFAULT 15,          -- minutos de tolerância
    observacao             TEXT,
    criado_em              TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (funcionario_id, data_roteiro, ordem)
);


-- ============================================================
-- 4. BATIDAS DE PONTO
--    Dados brutos recebidos da API Ponto Mais, sem processamento
-- ============================================================
CREATE TABLE IF NOT EXISTS batidas_ponto (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    pm_time_card_id     BIGINT      UNIQUE,              -- ID da batida no Ponto Mais
    funcionario_id      UUID        NOT NULL REFERENCES funcionarios(id),
    pm_employee_id      INTEGER     NOT NULL,
    data_hora           TIMESTAMPTZ NOT NULL,             -- momento exato da batida
    tipo                TEXT,       -- ENTRADA | SAIDA | INTERVALO_INICIO | INTERVALO_FIM
    latitude_real       NUMERIC(10, 7),                  -- geolocalização capturada pelo app
    longitude_real      NUMERIC(10, 7),
    endereco_registrado TEXT,                            -- endereço reverso retornado pelo app
    dispositivo         TEXT,                            -- info do aparelho (se disponível)
    importado_em        TIMESTAMPTZ DEFAULT NOW()
);


-- ============================================================
-- 5. COMPARAÇÕES
--    Cruza roteiro previsto × batida real (resultado do job diário)
-- ============================================================
CREATE TABLE IF NOT EXISTS comparacoes (
    id                     UUID     PRIMARY KEY DEFAULT gen_random_uuid(),
    roteiro_id             UUID     NOT NULL UNIQUE REFERENCES roteiros(id),  -- UNIQUE: upsert por roteiro
    batida_entrada_id      UUID     REFERENCES batidas_ponto(id),
    batida_saida_id        UUID     REFERENCES batidas_ponto(id),
    funcionario_id         UUID     NOT NULL REFERENCES funcionarios(id),
    local_id               UUID     NOT NULL REFERENCES locais(id),
    data_referencia        DATE     NOT NULL,

    -- Horários
    hora_prevista_entrada  TIME,
    hora_real_entrada      TIME,
    hora_prevista_saida    TIME,
    hora_real_saida        TIME,
    minutos_atraso_entrada INTEGER,   -- positivo = atraso, negativo = adiantado
    minutos_saida_antecip  INTEGER,   -- positivo = saiu antes do previsto

    -- Geolocalização
    distancia_entrada_m    NUMERIC(10, 2),  -- distância em metros entre batida e local previsto
    distancia_saida_m      NUMERIC(10, 2),
    dentro_raio_entrada    BOOLEAN,
    dentro_raio_saida      BOOLEAN,

    -- Status calculado
    status_presenca        TEXT NOT NULL,  -- CONFORME | AUSENTE | ATRASO | FORA_DO_LOCAL | PARCIAL
    status_geo             TEXT,           -- OK | DIVERGENTE | SEM_GPS

    processado_em          TIMESTAMPTZ DEFAULT NOW()
);


-- ============================================================
-- 5.1 PRESENÇAS DO DIA
--    Presença (bateu ponto ou não) de TODO funcionário ativo,
--    independente de ter roteiro cadastrado. Complementa `comparacoes`,
--    que só cobre quem tem roteiro (e traz a conformidade de local).
-- ============================================================
CREATE TABLE IF NOT EXISTS presencas_dia (
    id                 UUID     PRIMARY KEY DEFAULT gen_random_uuid(),
    funcionario_id     UUID     NOT NULL REFERENCES funcionarios(id),
    data_referencia    DATE     NOT NULL,
    tem_roteiro        BOOLEAN  NOT NULL DEFAULT FALSE,
    bateu_ponto        BOOLEAN  NOT NULL DEFAULT FALSE,
    primeira_batida    TIME,
    ultima_batida      TIME,
    total_batidas      INTEGER  NOT NULL DEFAULT 0,
    processado_em      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (funcionario_id, data_referencia)
);

CREATE INDEX IF NOT EXISTS idx_presencas_data ON presencas_dia (data_referencia);


-- ============================================================
-- 6. ALERTAS
--    Gerados a partir das comparações para notificação do RH
-- ============================================================
CREATE TABLE IF NOT EXISTS alertas (
    id               UUID      PRIMARY KEY DEFAULT gen_random_uuid(),
    comparacao_id    UUID      REFERENCES comparacoes(id),
    funcionario_id   UUID      NOT NULL REFERENCES funcionarios(id),
    data_referencia  DATE      NOT NULL,
    tipo_alerta      TEXT      NOT NULL,  -- AUSENCIA | ATRASO | FORA_DO_LOCAL | SAIDA_ANTECIPADA | SEM_BATIDA
    nivel            SMALLINT  NOT NULL,  -- 1 = aviso, 2 = atenção, 3 = crítico
    descricao        TEXT,
    enviado          BOOLEAN   DEFAULT FALSE,
    destinatarios    JSONB,               -- [{"nome": "Gestor X", "email": "...", "canal": "email"}]
    enviado_em       TIMESTAMPTZ,
    criado_em        TIMESTAMPTZ DEFAULT NOW()
);


-- ============================================================
-- 7. LOG DE SINCRONIZAÇÃO
--    Rastreia cada execução do job de coleta da API
-- ============================================================
CREATE TABLE IF NOT EXISTS log_sincronizacao (
    id                 UUID      PRIMARY KEY DEFAULT gen_random_uuid(),
    iniciado_em        TIMESTAMPTZ DEFAULT NOW(),
    finalizado_em      TIMESTAMPTZ,
    data_referencia    DATE,
    total_funcionarios INTEGER   DEFAULT 0,
    total_batidas      INTEGER   DEFAULT 0,
    total_erros        INTEGER   DEFAULT 0,
    status             TEXT,     -- SUCESSO | FALHA | PARCIAL | EXECUTANDO
    detalhe_erro       TEXT
);


-- ============================================================
-- 8. CONFIGURAÇÕES DO SISTEMA
--    Parâmetros ajustáveis sem redeploy
-- ============================================================
CREATE TABLE IF NOT EXISTS configuracoes (
    chave         TEXT PRIMARY KEY,
    valor         TEXT NOT NULL,
    descricao     TEXT,
    atualizado_em TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO configuracoes (chave, valor, descricao) VALUES
    ('pm_api_base_url',       'https://api.pontomais.com.br/external_api/v1', 'URL base da API Ponto Mais'),
    ('job_hora_execucao',     '06:00',  'Horário diário de execução do job (HH:MM, fuso America/Sao_Paulo)'),
    ('tolerancia_padrao_min', '15',     'Tolerância padrão em minutos para classificar atraso'),
    ('raio_padrao_m',         '200',    'Raio padrão de aceitação de geolocalização em metros'),
    ('nivel_alerta_gestor',   '2',      'Nível mínimo de alerta para notificar gestor (1, 2 ou 3)')
ON CONFLICT (chave) DO NOTHING;


-- ============================================================
-- ÍNDICES — performance em consultas frequentes
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_batidas_funcionario_data  ON batidas_ponto    (funcionario_id, data_hora);
CREATE INDEX IF NOT EXISTS idx_roteiros_funcionario_data ON roteiros          (funcionario_id, data_roteiro);
CREATE INDEX IF NOT EXISTS idx_comparacoes_data          ON comparacoes       (data_referencia);
CREATE INDEX IF NOT EXISTS idx_comparacoes_status        ON comparacoes       (status_presenca);
CREATE INDEX IF NOT EXISTS idx_alertas_enviado           ON alertas           (enviado, criado_em);
CREATE INDEX IF NOT EXISTS idx_alertas_data              ON alertas           (data_referencia, nivel);
CREATE INDEX IF NOT EXISTS idx_funcionarios_ativo        ON funcionarios      (ativo);
CREATE INDEX IF NOT EXISTS idx_locais_ativo              ON locais            (ativo);


-- ============================================================
-- VIEW: Painel de acompanhamento diário
--   Uso: SELECT * FROM vw_painel_diario WHERE data_roteiro = CURRENT_DATE;
-- ============================================================
CREATE OR REPLACE VIEW vw_painel_diario AS
SELECT
    f.nome            AS funcionario,
    f.departamento,
    f.equipe,
    l.nome            AS local_previsto,
    r.data_roteiro,
    r.ordem           AS parada,
    r.hora_prevista_entrada,
    r.hora_prevista_saida,
    c.hora_real_entrada,
    c.hora_real_saida,
    c.minutos_atraso_entrada  AS atraso_min,
    c.distancia_entrada_m     AS distancia_m,
    c.dentro_raio_entrada     AS no_local,
    c.status_presenca,
    c.status_geo
FROM roteiros r
JOIN funcionarios f ON f.id = r.funcionario_id
JOIN locais       l ON l.id = r.local_id
LEFT JOIN comparacoes c ON c.roteiro_id = r.id
ORDER BY r.data_roteiro DESC, f.nome, r.ordem;


-- ============================================================
-- FUNÇÃO: calcula distância em metros entre dois pontos
--   Uso: SELECT calcular_distancia_m(-23.5, -46.6, -23.51, -46.61);
-- ============================================================
CREATE OR REPLACE FUNCTION calcular_distancia_m(
    lat1 NUMERIC, lng1 NUMERIC,
    lat2 NUMERIC, lng2 NUMERIC
) RETURNS NUMERIC AS $$
DECLARE
    R       CONSTANT NUMERIC := 6371000;  -- raio da Terra em metros
    phi1    NUMERIC := radians(lat1);
    phi2    NUMERIC := radians(lat2);
    dphi    NUMERIC := radians(lat2 - lat1);
    dlambda NUMERIC := radians(lng2 - lng1);
    a       NUMERIC;
BEGIN
    a := sin(dphi/2)^2 + cos(phi1)*cos(phi2)*sin(dlambda/2)^2;
    RETURN R * 2 * atan2(sqrt(a), sqrt(1-a));
END;
$$ LANGUAGE plpgsql IMMUTABLE;


-- ============================================================
-- FIM DO SCHEMA
-- Execute este arquivo no Supabase SQL Editor:
--   Dashboard → SQL Editor → New Query → cole e clique em Run
-- ============================================================
