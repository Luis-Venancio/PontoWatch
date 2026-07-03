# API de Integração — Pontomais (Documentação para Integração)

> Fonte: https://documenter.getpostman.com/view/4785048/RWMCvVxN (Postman Documenter, layout "Single Column")
> Extraído em: 2026-07-02
>
> **NOTA DE PROGRESSO (captura incompleta — corrigida em 2026-07-02):** este arquivo está em construção via extração automatizada da página Postman Documenter. Estão COMPLETAS as pastas: Introdução, Autenticação, Tipos de dados, Hierarquia, Unidades de Negócio, Centro de Custos, Departamentos, Cargos, Feriados (V1+V2), Cidades, Equipes, Colaboradores (completo, incl. Movimentações/Dias de jornada/Documentos), Banco de horas. A pasta **Turnos** está PARCIAL (faltam GET Listar/Detalhes/Listar dias, DELETE Excluir, PUT Desfazer exclusão, e detalhes finais da variante 5d/1d). As pastas **Usuários, AFD, AFD-671, AFDT, AEJ** ainda **NÃO** foram capturadas (uma versão anterior deste arquivo relatou incorretamente essas pastas como completas — foi verificado e corrigido). Da pasta **Relatórios** (27 relatórios), apenas **"Registros de ponto"** foi documentado por completo (prioritário — é o endpoint que retorna as batidas de ponto com geolocalização). Ver a seção "[PENDENTE]" ao final do documento para a lista exata do que falta.

## Introdução

Esta é a documentação da API. Ela descreve as funcionalidades e fornece exemplos com o objetivo de servir de guia para o desenvolvimento de integrações com a API, que utiliza o modelo de arquitetura REST.

## Primeiros passos / Autenticação

Para utilização desta API, primeiramente é necessário obter o token de sua base. Para isso, siga os seguintes passos:

1. Acesse https://app.pontomais.com.br/#/acessar;
2. Utilize as credenciais de administrador da empresa para autenticar-se;
3. No menu de navegação no canto esquerdo, clique em Marketplace;
4. Clique em "Saiba mais" dentro da área da "API Pontomais";
5. Realize a contratação da API, caso não tenha feito;
6. Após a contratação, estará disponível o campo "Token público" que contém o token de acesso à API.

**Base URL:** `https://api.pontomais.com.br`

**Header de autenticação:** `access-token: {{client_token}}` (ou `{{external_api_token}}` / `{{external_token}}` conforme o endpoint, sempre o token público/da API obtido no passo acima)

## Tipos de dados

Instruções para o preenchimento conforme o tipo do campo:

| Tipo | Instrução de preenchimento |
|---|---|
| Boolean | preencha com `true` (para verdadeiro) e `false` (para falso). |
| String | preencha com caracteres alfanuméricos e/ou especiais. |
| Date | preencha com uma String no formato "YYYY-MM-DD". |
| Integer | preencha somente com números. |
| Float | preencha somente com números de ponto flutuante. |
| Code | preencha com caracteres alfanuméricos (String) que sejam únicos no sistema de origem. |
| Phone | preencha com uma String no formato "(DD) XXXX-XXXX" ou "(DD) XXXXX-XXXX". |
| Timestamp | preencha com uma cadeia de caracteres numéricos que representem uma data e horário. |
| Object | preencha com um objeto. Nesta documentação os dados do tipo Object possuem uma tabela específica que determina as características de cada atributo. |

## Hierarquia de alocação de colaboradores

```
Unidade de Negócio
  └── Departamento
        └── Equipe
              └── Colaborador
```

---

## Unidades de Negócio

### PUT Editar

```
https://api.pontomais.com.br/external_api/v1/business_units/{{business_unit_id}}
```

Edita uma unidade de negócio.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| business_unit_id | Integer | Sim | ID da unidade de negócio |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| person_type | Integer | Não | Tipo do registro (1 - Pessoa física, 2 - Pessoa Jurídica) |
| code | Code (60) | Não | Código identificador da unidade de negócio |
| observation | String | Não | Observação |
| name | String (100) | Não | Nome da empesa ou pessoa |
| cpf ou cnpj | CPF: String (14), CNPJ: String (18) | Não | CPF no caso de pessoa física, CNPJ no caso de pessoa jurídica |
| state_inscription | String (18) | Não | Inscrição Estadual |
| corporate_name | String (120) | Não | Razão Social |
| is_employer | Boolean | Não | É empregadora? Ou seja, é uma pessoa jurídica ou física que registra, administra e paga colaboradores? (true - sim, false - não) |
| is_construction | Boolean | Não | É construtora? (true - sim, false - não) |
| phone | Phone (16) | Não | Telefone para contato |
| address | Objeto | Não | Verificar tabela descritiva do objeto |
| client_preference_id | Integer | Não | Configuração de controle de ponto |
| timezone | Integer | Não | ID do fuso horário para batidas de ponto via software |
| tax_classification_id | Integer | Não | ID da classificação tributária |
| juridical_nature_id | Integer | Não | ID da natureza jurídica |
| coop_type | Integer | Não | ID do tipo de cooperativa |

**Formato do objeto `address`**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| street | String | Não | Endereço |
| number | String | Não | Número |
| complement | String | Não | Complemento |
| district | String | Não | Bairro |
| zip | String | Não | CEP |
| street_type | Integer | Não | Tipo do endereço (veja a tabela Tipo de endereço) |
| city_id | Integer | Não | ID da cidade (ver rota para pesquisar IDs das cidades) |

**Tipo de endereço**

| Valor | Nome |
|---|---|
| 1 | Alameda |
| 2 | Avenida |
| 3 | Balneário |
| 4 | Bloco |
| 5 | Chácara |
| 6 | Conjunto |
| 7 | Condomínio |
| 8 | Estrada |
| 9 | Fazenda |
| 10 | Galeria |
| 11 | Granja |
| 12 | Jardim |
| 13 | Largo |
| 14 | Loteamento |
| 15 | Praça |
| 16 | Praia |
| 17 | Parque |
| 18 | Quadra |
| 19 | Rua |
| 20 | Setor |
| 21 | Travessa |
| 22 | Vila |
| 23 | Rodovia |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Body (raw json)**

```json
{
  "business_unit":
  {
    "person_type": 2,
    "code": 201,
    "observation": "Lorem Ipsum",
    "name": "Empresa Teste",
    "cnpj": "99.999.999/9999-99",
    "state_inscription": "",
    "corporate_name": "Empresa Teste",
    "is_construction": true,
    "is_employer": true,
    "phone": "(99) 99999-9999"
  },
  "address":
  {
    "street": "Padre Anchieta",
    "number": "2310",
    "complement": "Condomínio",
    "district": "Bigorrilho",
    "zip": "80730-000",
    "street_type": 19,
    "city_id": 4106902
  }
}
```

**Example Request (Exemplo de sucesso)**

```bash
curl --location --request PUT 'https://api.pontomais.com.br/public_api/integration/business_units/10547' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"business_unit":
{
"person_type": 2,
"code": "0002",
"observation": "Lorem ipsum...",
"name": "Empresa teste 2",
"cnpj": "99.999.999/9999-99",
"state_inscription": "isenta",
"corporate_name": "Empresa Teste 2",
"is_construction": false,
"is_employer": true,
"phone": "(99) 99999-9999",
"timezone": 2,
"coop_type": 0,
"juridical_nature_id": 1,
"tax_classification_id": 1
},
"address":
{
"street": "Padre Anchieta",
"number": "2310",
"complement": "Condomínio",
"district": "Bigorrilho",
"zip": "80730-000",
"street_type": 19,
"city_id": 4106902
}
}'
```

**Example Response — 200 OK**

```json
{
  "success": "Unidade editada com sucesso!",
  "meta": {
    "now": 1531769539,
    "ip": "127.0.0.1"
  }
}
```

> Nota: não foram encontrados endpoints GET Listar / GET Detalhar / POST Criar / DELETE Inativar para "Unidades de Negócio" — apenas PUT Editar está documentado (a criação de unidades de negócio provavelmente é feita apenas na configuração inicial da conta, não via API).

---

## Centro de Custos

### GET Listar

```
https://api.pontomais.com.br/external_api/v1/cost_centers
```

Lista os centros de custos.

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial único gerado pelo sistema |
| code | String | Código identificador do centro de custo |
| name | String | Nome do centro de custo |
| created_at | Timestamp | Data e horário de criação do centro de custo |
| updated_at | Timestamp | Data e horário de atualização do centro de custo |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente. |

**Example Request (Exemplo de sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/cost_centers?attributes=id%2Cname%2Ccode&count=true&page={{page_number}}&per_page=10' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "cost_centers": [
    { "id": 12341, "name": "Centro de Custos 1", "code": "0001" },
    { "id": 12342, "name": "Centro de Custos 2", "code": "0002" },
    { "id": 12343, "name": "Centro de Custos 3", "code": "0003" },
    { "id": 12344, "name": "Centro de Custos 4", "code": "0004" }
  ],
  "meta": {
    "now": 1531769941,
    "ip": "127.0.0.1",
    "count": 5
  }
}
```

### GET Detalhar

```
https://api.pontomais.com.br/external_api/v1/cost_centers/{{cost_center_id}}?attributes=id,name,code
```

Rota para obter os atributos de um centro de custo.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| cost_center_id | Integer | Sim | ID do centro de custo |

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial único gerado pelo sistema |
| code | String | Código identificador do centro de custo |
| name | String | Nome do centro de custo |
| created_at | Timestamp | Data e horário de criação do centro de custo |
| updated_at | Timestamp | Data e horário de atualização do centro de custo |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,name,code | Atributos (ver disponíveis acima) |

**Example Request (Exemplo de registro não encontrado)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/cost_centers/{{cost_center_id}}?attributes=id%2Cname%2Ccode' \
--header 'access-token: {{client_token}}'
```

**Example Response — 404 NOT FOUND**

```json
{
  "error": "Registro não encontrado",
  "meta": {
    "now": 1531770321,
    "ip": "127.0.0.1"
  }
}
```

### POST Criar

```
https://api.pontomais.com.br/external_api/v1/cost_centers
```

Cria um centro de custo.

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| name | String (60) | Sim | Nome do centro de custo |
| code | Code (60) | Não | Código identificador do centro de custo |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Body (raw)**

```json
{
  "cost_center": {
    "code":"ES-21",
    "name":"Detraxit"
  }
}
```

**Example Request (Exemplo de erro ao cadastrar)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/cost_centers' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"cost_center": {
"code":"",
"name":""
}
}'
```

**Example Response — 422 UNPROCESSABLE ENTITY**

```json
{
  "errors": {
    "name": [
      "Não pode ficar em branco"
    ]
  },
  "meta": {
    "now": 1531770701,
    "ip": "127.0.0.1"
  }
}
```

### PUT Editar

```
https://api.pontomais.com.br/external_api/v1/cost_centers/{{cost_center_id}}
```

Edita um centro de custo.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| cost_center_id | Integer | Sim | ID do centro de custo |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| name | String (60) | Sim | Nome do centro de custo |
| code | Code (60) | Não | Código identificador do centro de custo |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente |

**Body (raw)**

```json
{
  "cost_center": {
    "code":"ES-21",
    "name":"Detraxit"
  }
}
```

**Example Request (Exemplo de edição com sucesso)**

```bash
curl --location -g --request PUT 'https://api.pontomais.com.br/external_api/v1/cost_centers/{{cost_center_id}}' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"cost_center":
{
"code":"0006",
"name":"Centro de Custos 6"
}
}'
```

**Example Response — 200 OK**

```json
{
  "success": "Centro de custo editado com sucesso!",
  "meta": {
    "now": 1531771022,
    "ip": "127.0.0.1"
  }
}
```

### DELETE Inativar

```
https://api.pontomais.com.br/external_api/v1/cost_centers/{{cost_center_id}}
```

Inativa um centro de custo.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| cost_center_id | Integer | Sim | ID do centro de custo |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**Example Request (Exemplo de registro não encontrado)**

```bash
curl --location -g --request DELETE 'https://api.pontomais.com.br/external_api/v1/cost_centers/{{cost_center_id}}' \
--header 'access-token: {{client_token}}'
```

**Example Response — 404 NOT FOUND**

```json
{
  "error": "Registro não encontrado",
  "meta": {
    "now": 1531770927,
    "ip": "127.0.0.1"
  }
}
```

---

## Departamentos

### GET Listar

```
https://api.pontomais.com.br/external_api/v1/departments
```

Lista os departamentos.

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| code | Code (60) | Código identificador do departamento |
| name | String (60) | Nome do departamento |
| business_unit | Objeto | Unidade de negócio à qual o departamento pertence |
| observation | String (255) | Observação |
| employees_count | Integer | Quantidade de colaboradores |
| created_at | Timestamp | Data e horário de criação do departamento |
| updated_at | Timestamp | Data e horário de atualização do departamento |

**Formato do objeto `business_unit`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| code | Code (60) | Código identificador da unidade de negócio |
| name | String (100) | Nome da unidade de negócio |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**Example Request**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/departments?attributes=id%2Ccode%2Cname%2Cbusiness_unit&count=true&page={{page_number}}&per_page=10' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "departments": [
    { "id": 123123, "code": "0003", "name": "Departamento 3", "business_unit": { "id": 5, "name": "Pontomais" } },
    { "id": 123124, "code": "0004", "name": "Departamento 4", "business_unit": { "id": 5, "name": "Pontomais" } },
    { "id": 123125, "code": "0005", "name": "Departamento 5", "business_unit": { "id": 5, "name": "Pontomais" } }
  ],
  "meta": {
    "now": 1531771293,
    "ip": "127.0.0.1",
    "count": 3
  }
}
```

### GET Detalhar

```
https://api.pontomais.com.br/external_api/v1/departments/{{department_id}}?attributes=id,code,name,business_unit,observation,created_at
```

Exibe os atributos de um departamento.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| department_id | Integer | Sim | ID do departamento |

**Atributos disponíveis:** (iguais ao GET Listar acima: id, code, name, business_unit, observation, employees_count, created_at, updated_at)

**Formato do objeto `business_unit`:** (igual ao GET Listar acima)

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,code,name,business_unit,observation,created_at | Atributos (ver disponíveis acima) |

**Example Request (Exemplo de registro não encontrado)**

```bash
curl --location -g 'https://api.pontomais.com.br/public_api/integration/departments/{{department_id}}?attributes=id%2Ccode%2Cname%2Cbusiness_unit' \
--header 'access-token: {{client_token}}'
```

**Example Response — 404 NOT FOUND**

```json
{
  "error": "Registro não encontrado",
  "meta": {
    "now": 1531771541,
    "ip": "127.0.0.1"
  }
}
```

### POST Criar

```
https://api.pontomais.com.br/external_api/v1/departments
```

Cria um departamento.

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| name | String (60) | Sim | Nome do departamento |
| code | Code (60) | Não | Código identificador do departamento |
| observation | String (255) | Não | Observação |
| business_unit_id | Integer | Sim | ID da unidade de négocio à qual o departamento deve pertencer |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente |

**Body (raw)**

```json
{
  "department":
  {
    "code":"ES-21",
    "name":"Detraxit",
    "observation":"Mussum Ipsum, cacilds vidis litro abertis. Paisis, filhis, espiritis santis. Detraxit consequat et quo num tendi nada. Suco de cevadiss, é um leite divinis, qui tem lupuliz, matis, aguis e fermentis. Sapien in monti palavris qui num significa nadis i pareci latim.",
    "business_unit_id": {{business_unit_id}}
  }
}
```

**Example Request (Exemplo de erro no cadastro)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/departments' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"department": {
"code":"0003",
"name":"Departamento 3",
"observation":"Lorem ipsum",
"business_unit_id": 123123
}
}'
```

**Example Response — 422 UNPROCESSABLE ENTITY**

```json
{
  "errors": {
    "business_unit": [
      "Não pode ficar em branco",
      "Não está incluído na lista"
    ]
  },
  "meta": {
    "now": 1531771649,
    "ip": "127.0.0.1"
  }
}
```

### PUT Editar

```
https://api.pontomais.com.br/external_api/v1/departments/{{department_id}}
```

Edita um departamento.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| department_id | Integer | Sim | ID do departamento |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| name | String (60) | Não | Nome do departamento |
| code | Code (60) | Não | Código identificador do departamento |
| observation | String (255) | Não | Observação |
| business_unit_id | Integer | Não | ID da unidade de négocio à qual o departamento deve pertencer |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente |

**Body (raw)**

```json
{
  "department":
  {
    "code":"ES-21",
    "name":"Detraxit",
    "observation":"Mussum Ipsum, cacilds vidis litro abertis. Paisis, filhis, espiritis santis. Detraxit consequat et quo num tendi nada. Suco de cevadiss, é um leite divinis, qui tem lupuliz, matis, aguis e fermentis. Sapien in monti palavris qui num significa nadis i pareci latim.",
    "business_unit_id": {{business_unit_id}}
  }
}
```

**Example Request (Exemplo de edição com erro)**

```bash
curl --location -g --request PUT 'https://api.pontomais.com.br/external_api/v1/departments/{{department_id}}' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"department": {
"code":"0003",
"name":"Departamento 3",
"observation":"",
"business_unit_id": 123123
}
}'
```

**Example Response — 422 UNPROCESSABLE ENTITY**

```json
{
  "errors": {
    "business_unit": [
      "Não pode ficar em branco",
      "Não está incluído na lista"
    ]
  },
  "meta": {
    "now": 1531771932,
    "ip": "127.0.0.1"
  }
}
```

### DELETE Inativar

```
https://api.pontomais.com.br/external_api/v1/departments/{{department_id}}
```

Inativa um departamento.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| department_id | Integer | Sim | ID do departamento |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**Example Request (Exemplo de registro não encontrado)**

```bash
curl --location -g --request DELETE 'https://api.pontomais.com.br/external_api/v1/departments/{{department_id}}' \
--header 'access-token: {{client_token}}'
```

**Example Response — 404 NOT FOUND**

```json
{
  "error": "Registro não encontrado",
  "meta": {
    "now": 1531771806,
    "ip": "127.0.0.1"
  }
}
```

---

## Cargos

### GET Listar (CBO)

```
https://api.pontomais.com.br/external_api/v1/job_titles/cbos?attributes=id,code,name
```

Lista os cargos.

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador único |
| code | Code (60) | Código identificador do cargo |
| name | String (60) | Nome do cargo |
| female_name | String (60) | Nome feminino do cargo |
| cbo | Object | CBO (Classificação Brasileira de Ocupações) |

**Formato do objeto `cbo`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador único |
| code | String (6) | Código CBO (Classificação Brasileira de Ocupações). Esse código pode ser encontrado em http://www.mtecbo.gov.br/cbosite/pages/pesquisas/BuscaPorTitulo.jsf |
| name | String | Nome da ocupação |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{external_token}} |

**PARAMS**

| Nome | Valor |
|---|---|
| attributes | id,code,name |

**Example Request (Exemplo bem sucedido)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/job_titles?attributes=id%2Ccode%2Cname&count=true&page={{page_number}}&per_page=10' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "job_titles": [
    { "id": 6, "code": "01", "name": "Gerente" },
    { "id": 5, "code": "02", "name": "Analista Desenvolvedor" },
    { "id": 14, "code": "03", "name": "Marketing" },
    { "id": 1394, "code": "04", "name": "Encantador de Clientes" },
    { "id": 2356, "code": "05", "name": "Consultor de Vendas" }
  ],
  "meta": {
    "now": 1531773311,
    "ip": "127.0.0.1",
    "count": 6
  }
}
```

### GET Listar

```
https://api.pontomais.com.br/external_api/v1/job_titles?attributes=id,code,name,female_name,cbo&count=true&page={{page_number}}&per_page=10
```

Lista os cargos. (Mesmos atributos disponíveis e formato do objeto `cbo` do endpoint anterior.)

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{external_token}} |

**PARAMS**

| Nome | Valor |
|---|---|
| attributes | id,code,name,female_name,cbo |
| count | true |
| page | {{page_number}} |
| per_page | 10 |

**Example Request / Response:** iguais ao endpoint "GET Listar (CBO)" acima.

### GET Detalhar

```
https://api.pontomais.com.br/external_api/v1/job_titles/533813?attributes=id,code,name,cbo
```

Exibe os atributos de um cargo.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| job_title_id | Integer | Sim | ID do cargo |

**Atributos disponíveis / Formato do objeto `cbo`:** iguais aos anteriores.

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,code,name,cbo | Atributos (ver disponíveis acima) |

**Example Request**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/job_titles/{{job_title_id}}?attributes=id%2Ccode%2Cname' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "job_title": { "id": 6, "code": "02", "name": "Gerente" },
  "meta": { "now": 1531773539, "ip": "127.0.0.1" }
}
```

### POST Criar

```
https://api.pontomais.com.br/external_api/v1/job_titles
```

Cria um cargo.

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| code | Code (60) | Não | código |
| name | String (60) | Sim | Nome do cargo |
| female_name | String (60) | Não | Nome feminino do cargo |
| cbo_code | String (6) | Não | Código CBO (Classificação Brasileira de Ocupações). Esse código pode ser encontrado em http://www.mtecbo.gov.br/cbosite/pages/pesquisas/BuscaPorTitulo.jsf |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Body (raw)**

```json
{
  "job_title": {
    "code":"0055",
    "name":"Doctor",
    "female_name":"Doctor",
    "cbo_code": "{{cbo_code}}"
  }
}
```

**Example Request (CBO desconhecido)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/job_titles' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"job_title": {
"code":"ES-21",
"name":"Detraxit",
"female_name":"Detraxita",
"cbo_code": {{cbo_code}}
}
}'
```

**Example Response — 422 UNPROCESSABLE ENTITY**

```json
{
  "errors": {
    "base": [
      "CBO desconhecido. Não foi possível encontrar um CBO a partir do cbo_code informado"
    ]
  },
  "meta": { "now": 1598388408, "ip": "191.177.186.252" }
}
```

### PUT Editar

```
https://api.pontomais.com.br/external_api/v1/job_titles/26385
```

Edita um cargo.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| job_title_id | Integer | Sim | ID do cargo |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| code | Code (60) | Não | código |
| name | String (60) | Sim | Nome do cargo |
| female_name | String (60) | Não | Nome feminino do cargo |
| cbo_code | String (6) | Não | Código CBO (Classificação Brasileira de Ocupações) |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Body (raw)**

```json
{
  "job_title":
  {
    "code":"ES-21",
    "name":"Detraxit",
    "female_name":"Detraxita",
    "cbo_code": "{{cbo_code}}"
  }
}
```

**Example Request (Exemplo de edição com sucesso)**

```bash
curl --location -g --request PUT 'https://api.pontomais.com.br/external_api/v1/job_titles/{{job_title_id}}' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"job_title": {
"code":"08",
"name":"Vendedor",
"female_name":"",
"cbo_id":""
}
}'
```

**Example Response — 200 OK**

```json
{
  "success": "Cargo editado com sucesso!",
  "meta": { "now": 1531774054, "ip": "127.0.0.1" }
}
```

### DELETE Inativar

```
https://api.pontomais.com.br/external_api/v1/job_titles/{{job_title_id}}
```

Inativa um cargo.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| job_title_id | Integer | Sim | ID do cargo |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**Example Request (Exemplo de registro não encontrado)**

```bash
curl --location -g --request DELETE 'https://api.pontomais.com.br/external_api/v1/job_titles/{{job_title_id}}' \
--header 'access-token: {{client_token}}'
```

**Example Response — 404 NOT FOUND**

```json
{
  "error": "Registro não encontrado",
  "meta": { "now": 1531774209, "ip": "127.0.0.1" }
}
```

---

## Feriados

API de integração de Criação e atualização de Feriados

### V1

Documentação para cadastrar Feriados para Equipes, Unidade de Negócio, Centro de Custo, Departamento ou Turno. Nessa versão, é possível cadastrar apenas para um único grupamento dos informados acima.

#### GET Listar

```
https://api.pontomais.com.br/external_api/v1/holidays?attributes=id,name,fixed,date,active,team,department,business_unit,cost_center,shift&count=true&page={{page_number}}&per_page=10
```

Lista os feriados cadastrados.

**Parâmetros na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| count | Boolean | Não | Contar total de registros (true - sim) |
| page | Integer | Não | Número da página iniciando em 1 |
| per_page | Integer | Não | Número de registros por página |
| attributes | String | Não | Lista de campos desejados separados por vírgula, ex: "id,code,name" |
| sort_property | String | Não | Campos que devem ser ordenados, separados por vírgula, ex1: "name", ex2: "name,date" |
| sort_direction | String | Não | Direção da ordenação dos campos a serem ordenados (asc ou desc), ex1: "asc", ex2: "asc,desc" |
| name | String | Não | Filtro de busca por nome |
| year | String | Não | Filtro de busca por ano |
| search | String | Não | Filtro de busca geral, busca por nome, data, equipe, departamento, unidade, centro de custos ou turno |
| team_id | String | Não | Filtro de busca por equipe |
| department_id | String | Não | Filtro de busca por departamento |
| business_unit_id | String | Não | Filtro de busca por unidade de negócios |
| cost_center_id | String | Não | Filtro de busca por centro de custos |
| shift_id | String | Não | Filtro de busca por turno |

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome do feriado |
| date | String (5) | Dia e mês do feriado no formato DD/MM |
| fixed | Boolean | O feriado é recorrente? (true - sim, se repete todos os anos / false - não, aplica apenas ao ano corrente) |
| active | Boolean | O feriado está ativo? (true - sim / false - não) |
| team | Object | Equipe à qual o feriado se refere |
| department | Object | Departamento à qual o feriado se refere |
| business_unit | Object | Unidade de negócio à qual o feriado se refere |
| cost_center | Object | Centro de custo à qual o feriado se refere |
| shift | Object | Turno à qual o feriado se refere |

**Formato do objeto `team`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| code | Code (60) | Código identificador da equipe |
| name | String (100) | Nome da equipe |

**Formato do objeto `department`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| code | Code (60) | Código identificador da departamento |
| name | String (100) | Nome da departamento |

**Formato do objeto `business_unit`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| code | Code (60) | Código identificador da unidade de negócio |
| name | String (100) | Nome da unidade de negócio |

**Formato do objeto `cost_center`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| code | Code (60) | Código identificador da centro de custos |
| name | String (100) | Nome da centro de custos |

**Formato do objeto `shift`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| code | Code (60) | Código identificador da turno |
| name | String (100) | Nome da turno |
| main_parent_id | Integer | Identificador sequencial do histórico de alterações do turno gerado automaticamente pelo sistema |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{external_api_token_local}} | Token do cliente |

**PARAMS**

| Nome | Valor |
|---|---|
| attributes | id,name,fixed,date,active,team,department,business_unit,cost_center,shift |
| sort_property | date |
| sort_direction | desc |
| year | 2018 |
| count | true |
| page | {{page_number}} |
| per_page | 10 |

**Example Request (Exemplo de sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/holidays?attributes=id%2Cname%2Cfixed%2Cdate%2Cbusiness_unit&count=true&page={{page_number}}&per_page=10' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "holidays": [
    {
      "id": 316,
      "name": "Meu Novo Feriado",
      "fixed": false,
      "date": "2026-02-20",
      "team": { "id": 1, "code": "0001", "name": "Administração" },
      "department": null,
      "business_unit": null,
      "cost_center": null,
      "shift": null
    },
    {
      "id": 317,
      "name": "Novo Feriado Importante",
      "fixed": false,
      "date": "2026-02-21",
      "team": { "id": 1, "code": "0001", "name": "Administração" },
      "department": null,
      "business_unit": null,
      "cost_center": null,
      "shift": null
    }
  ],
  "meta": { "now": 1771615562, "ip": "172.16.57.1", "obfuscated": false, "count": 2 }
}
```

#### GET Detalhar

```
https://api.pontomais.com.br/external_api/v1/holidays/4
```

Exibe os atributos de um feriado.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| holiday_id | Integer | Sim | ID do feriado a ser detalhado |

**Parâmetros na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| attributes | String | Não | Lista de campos desejados separados por vírgula, ex: "id,code,name" |

**Atributos disponíveis / Formatos dos objetos:** iguais ao GET Listar V1 acima.

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{external_api_token}} | Token do cliente |

**Example Request (Exemplo de sucesso)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/holidays/4?attributes=id%2Cname%2Cfixed%2Cdate%2Cbusiness_unit%2Ccost_center%2Cteam%2Cshift%2Cdepartment' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "holiday": {
    "id": 316,
    "created_at": 1771615414,
    "updated_at": 1771615414,
    "name": "Meu Novo Feriado",
    "date": "2026-02-20",
    "fixed": false,
    "team": { "id": 1, "code": "0001", "name": "Administração" },
    "department": null,
    "business_unit": null,
    "cost_center": null,
    "shift": null,
    "group_id": null
  },
  "meta": { "now": 1771615421, "ip": "172.16.57.1", "obfuscated": false }
}
```

#### POST Criar

```
https://api.pontomais.com.br/external_api/v1/holidays
```

Cria um feriado.

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| name | String (60) | Sim | Nome do feriado |
| date | String (5) | Sim | Dia e mês do feriado no formato DD/MM |
| fixed | Boolean | Não | O feriado é fixo? (true - sim, todos os anos / false - não, apenas no ano corrente) |
| active | Boolean | Não | O feriado está ativo? (true - sim / false - não) |
| team_id | Integer | Não | ID da equipe à qual o feriado se refere. Se um ID não for informado o sistema aplicará a todas as equipes |
| department_id | Integer | Não | ID do departamento à qual o feriado se refere. Se não informado aplica a todos os departamentos |
| business_unit_id | Integer | Não | ID da unidade de negócio à qual o feriado se refere. Se não informado aplica a todas as unidades |
| cost_center_id | Integer | Não | ID do centro de custos à qual o feriado se refere. Se não informado aplica a todos os centros de custos |
| shift_id | Integer | Não | ID do turno à qual o feriado se refere. Se não informado aplica a todos os turnos |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{external_api_token_local}} | Token do cliente |

**Body (raw)**

```json
{
  "holiday": {
    "name": "Novo Feriado Departamento",
    "fixed": false,
    "date": "2026-02-22",
    "team_id": null,
    "department_id": null,
    "business_unit_id": 1,
    "cost_center_id": null,
    "shift_id": null
  }
}
```

**Example Request (Exemplo de erro no cadastro)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/holidays' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"holiday": {
"name":"Dia do programador",
"fixed":true,
"date":"12/09",
"business_unit_id":10548
}
}'
```

**Example Response — 422 UNPROCESSABLE ENTITY**

```json
{
  "errors": { "business_unit": ["Não está incluído na lista"] },
  "meta": { "now": 1771615753, "ip": "172.16.57.1", "obfuscated": false }
}
```

#### PUT Editar

```
https://api.pontomais.com.br/external_api/v1/holidays/4
```

Edita um Feriado.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| holiday_id | Integer | Sim | ID do feriado |

**Estrutura do objeto JSON a ser enviado:** (mesmos campos do POST Criar V1: name, date, fixed, active, team_id, department_id, business_unit_id, cost_center_id, shift_id)

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente |

**Body (raw)**

```json
{
  "holiday": {
    "name": "Detraxit",
    "fixed": true,
    "date": "2020-01-20",
    "team_id": {{team_id}},
    "department_id": {{department_id}},
    "business_unit_id": {{business_unit_id}},
    "cost_center_id": {{cost_center_id}},
    "shift_id": {{shift_id}}
  }
}
```

**Example Request (Exemplo de registro não encontrado)**

```bash
curl --location --request PUT 'https://api.pontomais.com.br/external_api/v1/holidays/4' \
--header 'Content-Type: application/json' \
--header 'acess-token: {{client_token}}' \
--data '{
"holiday": {
"name":"Dia do programador",
"fixed":true,
"date":"12/09",
"business_unit_id":10548
}
}'
```

**Example Response — 404 NOT FOUND**

```json
{
  "error": "Registro não encontrado",
  "meta": { "now": 1531774779, "ip": "127.0.0.1" }
}
```

#### DELETE Excluir

```
https://api.pontomais.com.br/external_api/v1/holidays/321
```

Exclui um feriado.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| holiday_id | Integer | Sim | ID do feriado a ser excluído |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | (token do cliente) |

**Example Request (Exemplo de remoção com sucesso)**

```bash
curl --location --request DELETE 'https://api.pontomais.com.br/external_api/v1/holidays/4' \
--header 'access-tokken: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "success": "Feriado removido com sucesso!",
  "meta": { "now": 1771615167, "ip": "172.0.0.1", "obfuscated": false }
}
```

### V2

Documentação para cadastrar Feriados para Equipes, Unidade de Negócio, Centro de Custo, Departamento ou Turno. Nessa versão, é possível fazer o cadastro de um Feriado para diversos Turnos de uma vez (ou Unidade de Negócio ou Centro de Custo ou Departamento ou Turno). Você precisará saber os ids dos Turnos que deseja cadastrar, criar uma lista e enviar a requisição.

#### GET Listar

```
https://api.pontomais.com.br/external_api/v2/holidays?attributes=id,name,fixed,date,active,team,department,business_unit,cost_center,shift&count=true&page={{page_number}}&per_page=10
```

Lista os feriados cadastrados.

**Parâmetros na URL:** iguais ao V1 (count, page, per_page, attributes, sort_property, sort_direction, name, year, search, team_id, department_id, business_unit_id, cost_center_id, shift_id)

**Atributos disponíveis:** iguais ao V1 (id, name, date, fixed, active, team, department, business_unit, cost_center, shift)

**Formato do objeto retornado**

| Nome | Tipo | Descrição |
|---|---|---|
| holidays | lista | id: ID do feriado; name: Nome do Feriado; date: Data do Feriado; can_be_edited: Informa se o feriado pode ser editado pelo usuário que fez a requisição; grupamento: Informa se o feriado é para uma Equipe, BU, Centro de Custo, Departamento. O valor retornado dentro dele é uma lista de id, name, code do grupamento informado |
| meta | hash | now: Hora da requisição; ip: IP de origem da requisição; obfuscated: Informa se os dados foram ofuscados; count: Quantidade de objetos retornados |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{external_api_token}} | Token da API externa do cliente |

**Example Request (Exemplo de sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v2/holidays?attributes=id%2Cname%2Cfixed%2Cdate%2Cbusiness_unit&count=true&page={{page_number}}&per_page=10' \
--header 'access-token: {{external_api_token}}'
```

**Example Response — 200 OK**

```json
{
  "holidays": [
    {
      "id": 381,
      "name": "Meu feriado para Três Equipes",
      "fixed": true,
      "date": "2026-02-18",
      "team": [
        { "id": 1, "name": "Administração", "code": "0001" },
        { "id": 2, "name": "Administrativo", "code": null },
        { "id": 3, "name": "Financeiro", "code": null }
      ],
      "can_be_edited": true
    }
  ],
  "meta": { "now": 1771872909, "ip": "172.16.57.1", "obfuscated": false, "count": 1 }
}
```

#### GET Detalhar

```
https://api.pontomais.com.br/external_api/v2/holidays/4
```

Exibe os atributos de um feriado.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| holiday_id | Integer | Sim | ID do feriado a ser detalhado |

**Parâmetros na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| attributes | String | Não | Lista de campos desejados separados por vírgula |

**Formato do objeto retornado:** igual ao GET Listar V2 acima.

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{external_api_token}} | Token do cliente |

**Example Request**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v2/holidays/4?attributes=id%2Cname%2Cfixed%2Cdate%2Cbusiness_unit' \
--header 'access-token: {{external_api_token}}'
```

**Example Response — 200 OK**

```json
{
  "holiday": {
    "id": 319,
    "name": "Feriado Imporante",
    "date": "2026-05-01",
    "fixed": true,
    "active": true,
    "teams": [
      { "id": 5, "code": null, "name": "RH" },
      { "id": 6, "code": null, "name": "Desenvolvimento" }
    ],
    "departments": [],
    "business_units": [],
    "cost_centers": [],
    "shifts": []
  },
  "meta": { "now": 1771618072, "ip": "172.16.57.1", "obfuscated": false }
}
```

#### POST Criar

```
https://api.pontomais.com.br/external_api/v2/holidays
```

Cria um feriado.

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| name | String (60) | Sim | Nome do feriado |
| date | String (5) | Sim | Dia e mês do feriado no formato DD/MM |
| fixed | Boolean | Não | O feriado é fixo? (true - sim, todos os anos) |
| active | Boolean | Não | O feriado está ativo? (true - sim) |
| team_id | Integer | Não | ID da equipe. Se não informado aplica a todas as equipes |
| department_id | Integer | Não | ID do departamento. Se não informado aplica a todos os departamentos |
| business_unit_id | Integer | Não | ID da unidade de negócio. Se não informado aplica a todas as unidades |
| cost_center_id | Integer | Não | ID do centro de custos. Se não informado aplica a todos os centros de custos |
| shift_id | Integer | Não | ID do turno. Se não informado aplica a todos os turnos |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{external_api_token}} | Token do cliente |

**Body (raw)**

```json
{
  "name": "Meu Feriado Favorito",
  "fixed": true,
  "date": "14/10/2026",
  "teams": [1, 2],
  "departments": [],
  "business_units": [],
  "cost_centes": [],
  "shifts": []
}
```

**Example Request (Exemplo de erro no cadastro)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v2/holidays' \
--header 'Content-Type: application/json' \
--header 'access-token: {{external_api_token}}' \
--data '{
"name": "Meu Feriado Favorito",
"fixed": true,
"date": "14/10/2026",
"teams": [999999999999],
"departments": [],
"business_units": [],
"cost_centes": [],
"shifts": []
}'
```

**Example Response — 422 UNPROCESSABLE ENTITY**

```json
{
  "errors": { "business_unit": ["Não está incluído na lista"] },
  "meta": { "now": 1531774631, "ip": "127.0.0.1" }
}
```

#### PUT Editar

```
https://api.pontomais.com.br/external_api/v2/holidays/4
```

Edita um Feriado.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| holiday_id | Integer | Sim | ID do feriado |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| name | String (60) | Sim | Nome do feriado |
| date | String (5) | Sim | Dia e mês do feriado no formato DD/MM |
| fixed | Boolean | Não | O feriado é fixo? (true - sim, todos os anos) |
| active | Boolean | Não | O feriado está ativo? (true - sim) |
| teams | List | Não | Lista de ID's das equipes. Se não informado aplica a todas as equipes |
| departments | List | Não | Lista de ID's dos departamentos. Se não informado aplica a todos os departamentos |
| business_units | List | Não | Lista de ID's das unidades de negócio. Se não informado aplica a todas as unidades |
| cost_centers | List | Não | Lista de ID's dos centros de custos. Se não informado aplica a todos os centros de custos |
| shifts | List | Não | Lista de ID's dos turnos. Se não informado aplica a todos os turnos |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{external_api_token}} | Token do cliente |

**Body (raw)**

```json
{
  "name": "Meu Novo Nome",
  "fixed": true,
  "date": "18/02/2026",
  "teams": [1, 2],
  "departments": [],
  "business_units": [],
  "cost_centers": [],
  "shifts": []
}
```

**Example Request (Exemplo de registro não encontrado)**

```bash
curl --location --request PUT 'https://api.pontomais.com.br/external_api/v2/holidays/4' \
--header 'Content-Type: application/json' \
--header 'acess-token: {{external_api_token}}' \
--data '{
"name": "Meu Novo Nome",
"fixed": true,
"date": "18/02/2026",
"teams": [],
"departments": [1,9],
"business_units": [],
"cost_centers": [],
"shifts": []
}'
```

**Example Response — 404 NOT FOUND**

```json
{
  "errors": "Registro não encontrado.",
  "meta": { "now": 1771617254, "ip": "172.16.57.1", "obfuscated": false }
}
```

#### DELETE Excluir

```
https://api.pontomais.com.br/external_api/v2/holidays/4
```

Exclui um feriado.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| holiday_id | Integer | Sim | ID do feriado a ser excluído |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{external_api_token}} | Token do cliente |

**Example Request (Exemplo de remoção com sucesso)**

```bash
curl --location --request DELETE 'https://api.pontomais.com.br/external_api/v2/holidays/4' \
--header 'access-tokken: {{external_api_token}}'
```

**Example Response — 200 OK**

```json
{
  "success": "Feriado removido com sucesso!",
  "job_id": ["1771616213878873D283FA3A08E7D563AF0DF775B10D5639"],
  "meta": { "now": 1771616180, "ip": "172.16.57.1", "obfuscated": false }
}
```

---

## Cidades

### GET Listar

```
https://api.pontomais.com.br/external_api/v1/cities?attributes=id,name&name=curitiba&page={{page_number}}&per_page=10&sort_direction=asc&count=true
```

Lista as cidades.

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (255) | Nome da cidade |
| state | String (2) | Sigla do estado |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor |
|---|---|
| attributes | id,name |
| name | curitiba |
| page | {{page_number}} |
| per_page | 10 |
| sort_direction | asc |
| count | true |

**Example Request (Exemplo de sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/cities?attributes=id%2Cname&name=curitiba&page={{page_number}}&per_page=10&sort_direction=asc' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "cities": [
    { "id": 94, "name": "Curitiba", "state": "PR" },
    { "id": 5140, "name": "Curitibanos", "state": "SC" }
  ],
  "meta": { "now": 1531850473, "ip": "127.0.0.1" }
}
```

> Nota: "Cidades" possui apenas este endpoint GET Listar.

---

## Equipes

### Gestores

#### GET Listar

```
https://api.pontomais.com.br/external_api/v1/possible_leaders?count=true&page={{page_number}}&per_page=10
```

Lista colaboradores que possuem configurações para um perfil gestor.

**Formato do retorno**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome do colaborador |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| count | true | Se "true" retorna a quantidade de registros encontrados. |
| page | {{page_number}} | Número da página. Ex: 1 |
| per_page | 10 | Número de itens por página. Ex: 10 |

**Example Request (Exemplo de sucesso)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/possible_leaders' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "leaders": [
    { "id": 1, "name": "Fernando Pessoa" },
    { "id": 2, "name": "Fernanda Silva" },
    { "id": 3, "name": "Alberto Caeiro" }
  ],
  "meta": { "now": 1745431545, "ip": "172.16.57.1", "obfuscated": false }
}
```

#### POST Adicionar

```
https://api.pontomais.com.br/external_api/v1/teams/{{team_id}}/leaders
```

Adiciona gestor à equipe.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| team_id | Integer | Sim | ID da equipe |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| leader_ids | Array | Sim | Array de ids dos colaboradores que serão adicionados como gestores da equipe |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Body (raw)**

```json
{
  "team":
  {
    "employee_ids":[2]
  }
}
```

**Example Request (Exemplo de requisição bem sucedida)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/teams/{{team_id}}/leaders' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"team":
{
"employee_ids":[2]
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": [
    { "id": 28, "employee_id": 2, "messages": "Gestor adicionado com sucesso!" }
  ],
  "meta": { "now": 1745528399, "ip": "172.16.57.1", "obfuscated": false }
}
```

#### DELETE Remover

```
https://api.pontomais.com.br/external_api/v1/teams/{{team_id}}/leaders/{{employee_id}}
```

Remove gestor de uma equipe.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| team_id | Integer | Sim | ID da equipe |
| leader_id | Integer | Sim | ID do gestor |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Example Request (Exemplo de requisição bem sucedida)**

```bash
curl --location -g --request DELETE 'https://api.pontomais.com.br/external_api/v1/teams/{{team_id}}/leaders/{{leader_id}}' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "success": "Gestor removido com sucesso!",
  "meta": { "now": 1745528429, "ip": "172.16.57.1", "obfuscated": false }
}
```

### GET Listar (Equipes)

```
https://api.pontomais.com.br/external_api/v1/teams?attributes=id,code,name,department,leaders&count=true&page={{page_number}}&per_page=10
```

Lista as equipes.

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome da equipe |
| code | Code (60) | Código identificador da equipe |
| department | Object | Departamento ao qual a equipe pertence |
| leaders | Array | Lista de gestores da equipe |

**Formato do objeto `department`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| code | Code (60) | Código identificador do departamento |
| name | String (60) | Tipo de registro |

**Formato do objeto no array `leaders`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial do código do colaborador gerado automaticamente pelo sistema |
| name | String | Nome completo do colaborador/gestor |
| picture | Object | Foto do colaborador/gestor |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,code,name,department,leaders | |
| count | true | Se "true" retorna a quantidade de registros encontrados. |
| page | {{page_number}} | Número da página. Ex: 1 |
| per_page | 10 | Número de itens por página. Ex: 10 |

**Example Request (Exemplo de sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/teams?attributes=id%2Ccode%2Cname%2Cdepartment&count=true&page={{page_number}}&per_page=10' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "teams": [
    { "id": 9, "code": "01", "name": "Produto & TI", "department": { "id": 9, "code": "01", "name": "Departamento 1" } },
    { "id": 1830, "code": "02", "name": "Marketing e Vendas", "department": { "id": 10, "code": "02", "name": "Departamento 2" } },
    { "id": 10, "code": "03", "name": "Administração", "department": { "id": 11, "code": "03", "name": "Departamento 3" } }
  ],
  "meta": { "now": 1531772154, "ip": "127.0.0.1", "count": 4 }
}
```

### GET Detalhar

```
https://api.pontomais.com.br/external_api/v1/teams/{{team_id}}?attributes=id,code,name,department,leaders
```

Exibe os atributos de uma equipe.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| team_id | Integer | Sim | ID da equipe a ser detalhada |

**Atributos disponíveis / Formatos dos objetos:** iguais ao GET Listar acima.

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,code,name,department,leaders | Atributos (ver disponíveis acima) |

**Example Request**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/teams/{{team_id}}?attributes=id%2Ccode%2Cname%2Cdepartment' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "team": {
    "id": 21847,
    "code": "0004",
    "name": "Equipe 4",
    "department": { "id": 14899, "code": "0003", "name": "Departamento 3" }
  },
  "meta": { "now": 1531772401, "ip": "127.0.0.1" }
}
```

### POST Criar

```
https://api.pontomais.com.br/external_api/v1/teams
```

Cria uma equipe.

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| name | String (60) | Sim | Nome da equipe |
| code | Code (60) | Não | Código identificador da equipe |
| observation | String (255) | Não | Observação |
| department_id | Integer | Sim | ID do departamento ao qual a equipe deve pertencer |
| leader_ids | Array | Não | Array de ids de colaboradores a serem cadastrados como gestores |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente |

**Body (raw)**

```json
{
  "team":
  {
    "code":"ES-21",
    "name":"Detraxit",
    "observation":"Mussum Ipsum, cacilds vidis litro abertis. Paisis, filhis, espiritis santis. Detraxit consequat et quo num tendi nada. Suco de cevadiss, é um leite divinis, qui tem lupuliz, matis, aguis e fermentis. Sapien in monti palavris qui num significa nadis i pareci latim.",
    "department_id":{{department_id}},
    "leader_ids":[]
  }
}
```

**Example Request (Exemplo de erro ao cadastar)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/teams' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"team": {
"code": "0004",
"name": "Equipe 4",
"observation": "",
"leader_ids": []
}
}'
```

**Example Response — 422 UNPROCESSABLE ENTITY**

```json
{
  "errors": { "department": ["Não pode ficar em branco"] },
  "meta": { "now": 1531772675, "ip": "127.0.0.1" }
}
```

### PUT Editar

```
https://api.pontomais.com.br/external_api/v1/teams/{{team_id}}
```

Edita uma equipe.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| team_id | Integer | Sim | ID da equipe |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| name | String (60) | Sim | Nome da equipe |
| code | Code (60) | Não | Código identificador da equipe |
| observation | String (255) | Não | Observação |
| department_id | Integer | Sim | ID do departamento ao qual a equipe deve pertencer |
| leader_ids * | Array | Não | Array de ids de colaboradores a serem cadastrados como gestores. Irá remover todos os gestores e adicionar a listagem enviada |

**\* leader_ids — comportamento especial**

| Ação | Como passar o atributo |
|---|---|
| Excluir todos os gestores da equipe | `{ "team": { "leader_ids":[] } }` |
| Manter todos os gestores | não enviar o atributo |
| Manter todos os gestores | `{ "team": { "leader_ids":null } }` |
| Alterar os gestores | `{ "team": { "leader_ids":[1, 2, n] } }` |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente. |

**Body (raw)**

```json
{
  "team":
  {
    "code":"ES-21",
    "name":"Detraxit",
    "observation":"Mussum Ipsum, cacilds vidis litro abertis. Paisis, filhis, espiritis santis. Detraxit consequat et quo num tendi nada. Suco de cevadiss, é um leite divinis, qui tem lupuliz, matis, aguis e fermentis. Sapien in monti palavris qui num significa nadis i pareci latim.",
    "department_id":{{department_id}},
    "leader_ids":null
  }
}
```

**Example Request (Exemplo de edição com erro)**

```bash
curl --location -g --request PUT 'https://api.pontomais.com.br/external_api/v1/teams/{{team_id}}' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"team": {
"code": "0004",
"name": "Equipe 4",
"observation": "",
"department_id": "",
"leader_ids": []
}
}'
```

**Example Response — 422 UNPROCESSABLE ENTITY**

```json
{
  "errors": { "department": ["Não pode ficar em branco"] },
  "meta": { "now": 1531772816, "ip": "127.0.0.1" }
}
```

### DELETE Excluir

```
https://api.pontomais.com.br/external_api/v1/teams/{{team_id}}
```

Inativa uma equipe.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| team_id | Integer | Sim | ID da equipe |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**Example Request (Exemplo de remoção bem sucedida)**

```bash
curl --location -g --request DELETE 'https://api.pontomais.com.br/external_api/v1/teams/{{team_id}}' \
--header 'access--token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "success": "Equipe removida com sucesso!",
  "meta": { "now": 1531772992, "ip": "127.0.0.1" }
}
```

### PUT Desfazer exclusão

```
https://api.pontomais.com.br/external_api/v1/teams/{{team_id}}/recover
```

Restaura (desfaz a exclusão de) uma equipe.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| team_id | Integer | Sim | ID da equipe |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**Example Request (Exemplo de requisição bem sucedida)**

```bash
curl --location -g --request PUT 'https://api.pontomais.com.br/external_api/v1/teams/{{team_id}}/recover' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "success": "Equipe restaurada com sucesso!",
  "meta": { "now": 1745525740, "ip": "172.16.57.1", "obfuscated": false }
}
```

---

## Colaboradores

> A pasta "Colaboradores" no menu lateral contém as subpastas "Movimentações" (Equipe, Cargo, Turno), "Dias de jornada", "Documentos", e os endpoints principais: Listar, Detalhar, Criar, Editar, Demitir, Verifica se existe (POST), Verifica status do colaborador (GET), Verifica se existe (GET).

### Movimentações

#### Equipe

##### GET Listar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/team_changes?attributes=id,team,date&count=true&page={{page_number}}&per_page=10&sort_direction=asc&sort_property=first_name
```

Lista as movimentações do colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| date | String | Data de início na equipe |
| team | Object | Equipe da movimentação |

**Formato do objeto `team`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome da equipe |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,team,date | Atributos (ver disponíveis acima) |
| count | true | Retorna a quantidade de registros encontrados |
| page | {{page_number}} | Número da página |
| per_page | 10 | Número de itens por página |
| sort_direction | asc | Direção da ordenação, pode ser 'asc' (crescente) ou 'desc' (decrescente) |
| sort_property | first_name | Atributo para ordenação |

**Example Request (Exemplo de sucesso ao listar)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/team_changes?attributes=id%2Cteam%2Cdate&count=true&page={{page_number}}&per_page=10&sort_direction=asc&sort_property=first_name' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "team_changes": [
    { "id": 11286, "team": { "id": 1830, "name": "Marketing e Vendas" }, "date": "24/05/2016" }
  ],
  "meta": { "now": 1532442322, "ip": "127.0.0.1", "count": 1 }
}
```

##### GET Detalhar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/team_changes/7?attributes=id,team,date
```

Detalha a movimentação do colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |
| team_change_id | Integer | Sim | ID da movimentação |

**Atributos disponíveis / Formato do objeto `team`:** iguais ao GET Listar acima.

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente. |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,team,date | Atributos (ver disponíveis acima) |

**Example Request (Exemplo de sucesso ao detalhar)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/team_changes/{{team_changes_id}}?attributes=id%2Cteam%2Cdate' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "team_change": { "id": 11286, "team": { "id": 1830, "name": "Marketing e Vendas" }, "date": "24/05/2016" },
  "meta": { "now": 1532442612, "ip": "127.0.0.1" }
}
```

##### POST Criar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/team_changes
```

Cria uma movimentação de equipe para o colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| date | Date | Sim | Data de início na equipe |
| team_id | Integer | Sim | ID do turno a ser movimentado |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente |

**Body (raw)**

```json
{
  "team_change":{
    "date": "2020-03-10",
    "team_id": {{team_id}}
  }
}
```

**Example Request (Exemplo de sucesso ao criar)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/team_changes' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"team_change":{
"date":"2020-03-10",
"team_id": 3
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": "Mudança de equipe registrada com sucesso!",
  "meta": { "now": 1532443706, "ip": "127.0.0.1" },
  "id": 37679
}
```

##### DELETE Excluir

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/team_changes/7
```

Exclui uma movimentação de equipe do colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador a ser excluído a movimentação |
| team_change_id | Integer | Sim | ID da movimentação de equipe a ser excluída |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**Example Request (Exemplo de exclusão com sucesso)**

```bash
curl --location -g --request DELETE 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/team_changes/{{team_changes_id}}' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "success": "Mudança de equipe removida com sucesso!",
  "meta": { "now": 1532444363, "ip": "127.0.0.1" }
}
```

#### Cargo

##### GET Listar

```
https://api.pontomais.com.br/external_api/v1/employees/28/job_title_changes?attributes=id,job_title,date,effective_date,motive&count=true&page={{page_number}}&per_page=10
```

Lista as movimentações de cargo do colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador a ser mostrada as movimentações |

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| date | String | Data de início na equipe |
| effective_date | String | Data de notificação da demissão |
| job_title | Object | Cargo da movimentação |
| motive | Object | Motivo da movimentação |

**Formato do objeto `job_title`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome do cargo |

**Formato do objeto `motive`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador gerado pelo sistema |
| name | String (60) | Nome do motivo |

**Opções do objeto `motive`**

| Valor | Descrição |
|---|---|
| 1 | Admissão |
| 2 | Demissão |
| 3 | Alteração de Cargo |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,job_title,date,effective_date,motive | Atributos (ver disponíveis acima) |
| count | true | Retorna a quantidade de registros encontrados |
| page | {{page_number}} | Número da página |
| per_page | 10 | Número de itens por página |

**Example Request (Exemplo de listagem com sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/job_title_changes?attributes=id%2Cjob_title%2Cdate&count=true&page={{page_number}}&per_page=10' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "job_title_changes": [
    { "id": 61432, "job_title": { "id": 2356, "name": "Consultor de Vendas" }, "date": "01/07/2018" }
  ],
  "meta": { "now": 1532445139, "ip": "127.0.0.1", "count": 1 }
}
```

##### GET Detalhar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/job_title_changes/{{job_title_change_id}}?attributes=id,job_title,date
```

Detalha a movimentação do colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |
| job_title_change_id | Integer | Sim | ID da movimentação |

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| date | String | Data de início na equipe |
| job_title | Object | Cargo da movimentação |

**Formato do objeto `job_title`:** igual ao GET Listar acima.

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,job_title,date | Atributos (ver disponíveis acima) |

**Example Request (Exemplo de detalhe com sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/job_title_changes/{{job_title_change_id}}?attributes=id%2Cjob_title%2Cdate' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "job_title_change": { "id": 61432, "job_title": { "id": 2356, "name": "Consultor de Vendas" }, "date": "01/07/2018" },
  "meta": { "now": 1532445563, "ip": "127.0.0.1" }
}
```

##### POST Criar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/job_title_changes
```

Rota para criar uma movimentação de cargo para o colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| date | Date | Sim | Data de início na equipe |
| job_title_id | Integer | Sim | ID do cargo a ser movimentado |
| motive | Integer | Sim | Índice do motivo da movimentação (veja a tabela Legenda de motivos de movimentação) |

**Legenda de motivos de movimentação**

| Índice do motivo | Motivo |
|---|---|
| 1 | Admissão |
| 2 | Demissão |
| 3 | Alteração de cargo |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente |

**Body (raw)**

```json
{
  "job_title_change":{
    "date":"2020-01-20",
    "motive": 1,
    "job_title_id":{{job_title_id}}
  }
}
```

**Example Request (Exemplo de criação com sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/job_title_changes' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"job_title_change":{
"date":"2020-01-20",
"motive": 1,
"job_title_id":{{job_title_id}}
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": "Mudança de cargo registrada com sucesso!",
  "meta": { "now": 1532446469, "ip": "127.0.0.1" },
  "id": 61495
}
```

##### PUT Editar admissão

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/job_title_changes/update_admission
```

Edição de data e/ou cargo de uma admissão de um colaborador. **ATENÇÃO:** você somente conseguirá alterar uma admissão se não houver alterações de cargo. Caso já exista alterações de cargo, o indicado é utilizar o endpoint de Criação, onde você conseguirá incluir uma nova alteração de cargo.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| date | Date | Sim | Data de início na equipe |
| job_title_id | Integer | Sim | ID do cargo a ser movimentado |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente |

**Body (raw)**

```json
{
  "job_title_change":{
    "date":"2020-01-20",
    "job_title_id":{{job_title_id}}
  }
}
```

**Example Request (Exemplo de edição de admissão)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/job_title_changes/update_admission' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"job_title_change":{
"date": "03/08/2021",
"job_title_id": 1
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": "Admissão alterada com sucesso!",
  "meta": { "now": 1628173888, "ip": "172.16.57.1" }
}
```

##### DELETE Excluir

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/job_title_changes/{{job_title_change_id}}
```

Exclui uma movimentação de cargo do colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |
| job_title_change_id | Integer | Sim | ID da movimentação |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**Example Request (Exemplo de exclusão com sucesso)**

```bash
curl --location -g --request DELETE 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/job_title_changes/{{job_title_change_id}}' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "success": "Mudança de cargo removida com sucesso!",
  "meta": { "now": 1532446424, "ip": "127.0.0.1" }
}
```

#### Turno

##### GET Listar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/shift_changes?attributes=id,shift,date,shift_day&count=true&page={{page_number}}&per_page=10
```

Lista as movimentações de turno do colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| date | String | Data de início no turno |
| shift | Object | Turno da movimentação |
| shift_day | Object | Dia de início no turno |

**Formato do objeto `shift`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome do turno |
| code | String (60) | Código identificador do turno |

**Formato do objeto `shift_day`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| cyclic_day | Integer | Número do dia |
| shift_id | Integer | ID do turno |
| periods | Array | Conjuntos de períodos do dia |

**Formato dos objetos do array `periods`**

| Nome | Tipo | Descrição |
|---|---|---|
| enter_time | String | Horário de início do período |
| leave_time | String | Horário de fim do período |
| main_interval_after | Boolean | Após o intervalo principal da jornada? |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,shift,date,shift_day | Atributos (ver disponíveis acima) |
| count | true | Retorna a quantidade de registros encontrados |
| page | {{page_number}} | Número da página |
| per_page | 10 | Número de itens por página |

**Example Request (Exemplo de listagem com sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/shift_changes?attributes=id%2Cshift%2Cdate&count=true&page={{page_number}}&per_page=10' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "shift_changes": [
    { "id": 78471, "shift": { "id": 31531, "name": "teste semanal + 1 semana", "code": "37" }, "date": "01/07/2018" }
  ],
  "meta": { "now": 1532453687, "ip": "127.0.0.1", "count": 1 }
}
```

##### GET Detalhar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/shift_changes/{{shift_change_id}}?attributes=id,shift,date,shift_day
```

Rota para detalhar a movimentação de turno do colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |
| shift_change_id | Integer | Sim | ID da movimentação |

**Atributos disponíveis / Formatos dos objetos:** iguais ao GET Listar acima.

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,shift,date,shift_day | Atributos (ver disponíveis acima) |

**Example Request (Exemplo de detalhe com sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/shift_changes/{{shift_change_id}}?attributes=id%2Cjob_title%2Cdate' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "shift_change": { "id": 78471, "date": "01/07/2018" },
  "meta": { "now": 1532453854, "ip": "127.0.0.1" }
}
```

##### POST Criar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/shift_changes
```

Cria uma movimentação de turno para o colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| date | Date | Sim | Data de início no turno |
| shift_id | Integer | Sim | ID do turno a ser movimentado |
| shift_day_id | Integer | Não | ID do dia inicial, somente para os turnos (12h/36h, 24h/72h, 5d/1d). Consultar os dias do turno. |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente |

**Body (raw)**

```json
{
  "shift_change":{
    "date":"2020-01-20",
    "shift_id":{{shift_id}},
    "shift_day_id": 1
  }
}
```

**Example Request (Exemplo de criação com sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/shift_changes' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"shift_change":{
"date":"2020-03-10",
"shift_id": 3
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": "Mudança de turno registrada com sucesso!",
  "meta": { "now": 1532455412, "ip": "127.0.0.1" },
  "id": 78506
}
```

##### DELETE Excluir

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/shift_changes/{{shift_change_id}}
```

Exclui uma movimentação de turno do colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |
| shift_change_id | Integer | Sim | ID da movimentação |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**Example Request (Exemplo de exclusão com sucesso)**

```bash
curl --location -g --request DELETE 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/shift_changes/{{shift_change_id}}' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "success": "Mudança de turno removida com sucesso!",
  "meta": { "now": 1532455256, "ip": "127.0.0.1" }
}
```

#### Sobreaviso

##### DELETE Excluir

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/standbys/{{standby_id}}
```

Remove um sobreaviso de um colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |
| standby_id | Integer | Sim | ID do sobreaviso |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |
| Content-Type | application/json |

**Example Request (Excluir)**

```bash
curl --location -g --request DELETE 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/standbys/{{standby_id}}' \
--header 'access-token: {{client_token}}' \
--header 'Content-Type: application/json'
```

**Example Response:** Sem corpo de resposta (this request doesn't return any response body)

### Dias de jornada

#### POST Justificar falta

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/justify_missing_day
```

Endpoint para lançamento de um ajuste do Tipo "Falta com desconto" e "Suspensão" em um dia de Falta.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| status_id | Integer | Sim | Motivo do ajuste, obter através do endpoint 'Motivo dos ajustes' |
| date | String (60) | Sim | Dia do lançamento |
| motive | String (60) | Sim | Descrição do ajuste |

**OBS:** status_id deve ser do tipo "Falta com desconto" ou "Suspensão".

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |
| Content-Type | application/json |

**Body (raw)**

```json
{
  "proposal": {
    "status_id": 34,
    "date": "2020-09-26",
    "motive": "teste"
  }
}
```

**Example Request (Justificar falta)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{Employee_id}}/justify_missing_day' \
--header 'access-token: {{client_token}}' \
--header 'Content-Type: application/json' \
--data '{
"proposal": {
"status_id": 7,
"date": "2020-09-23",
"motive": "teste"
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": "Ajuste cadastrado com sucesso!",
  "meta": { "now": 1601488783, "ip": "127.0.0.1" },
  "id": 32
}
```

#### GET Motivo dos ajustes

```
https://api.pontomais.com.br/external_api/v1/time_cards/proposals/status?attributes=id,observation,status_type
```

Lista os motivos de ajustes.

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| observation | String (15) | Observação |
| status_type | Object | Tipo do motivo (id, name) |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |
| Content-Type | application/json |

**PARAMS**

| Nome | Valor |
|---|---|
| attributes | id,observation,status_type |

**Example Request (Motivo dos ajustes)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/time_cards/proposals/status?attributes=id%2Cobservation%2Cstatus_type' \
--header 'access-token: {{client_token}}' \
--header 'Content-Type: application/json'
```

**Example Response:** Sem corpo de resposta (this request doesn't return any response body)

### Documentos

#### GET Listar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/documents?
```

Lista os documentos de um colaborador.

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| created_at | Timestamp | Data e horário de cadastro do documento no sistema |
| updated_at | Timestamp | Data e horário de atualização do documento no sistema |
| number | String (20) | Número do documento |
| document_type | Object (2) | Tipo do documento |
| issuing_agency | String (20) | Órgão expedidor |
| expedition_date | String (10) | Data de expedição |
| expiration_date | String (10) | Data de expiração |
| first_expedition_date | String (10) | Data da primeira expedição |
| state | Object (2) | Estado (id, name) |
| driver_license_category | Object (2) | Categoria da CNH (id, name) |
| serial_number | String (11) | Número de série |
| observation | String (255) | Observação |

**Formato do objeto `document_type`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String | Tipo de documento |

**Formato do objeto `state`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | String (2) | Sigla do estado |
| name | String | Nome do estado |

**Formato do objeto `driver_license_category`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial |
| name | String (2) | Categoria da CNH |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor |
|---|---|
| cpf | 873.416.870-29 |

**Example Request (Exemplo de listagem com sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/documents' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "documents": [
    {
      "id": 2,
      "created_at": 1580412265,
      "updated_at": 1580412265,
      "number": "99999999999",
      "document_type": { "id": 5, "name": "Carteira Nacional de Habilitação" },
      "issuing_agency": "SSP",
      "expedition_date": "01/01/2020",
      "expiration_date": "13/07/2023",
      "first_expedition_date": "01/01/2020",
      "state": { "id": "PA", "name": "Pará" },
      "driver_license_category": { "id": 6, "name": "AB" },
      "serial_number": null,
      "observation": "10"
    },
    {
      "id": 1,
      "created_at": 1580412200,
      "updated_at": 1580412200,
      "number": "99.999.999-9",
      "document_type": { "id": 1, "name": "RG" },
      "issuing_agency": "SSP",
      "expedition_date": "16/01/2020",
      "expiration_date": null,
      "first_expedition_date": null,
      "state": null,
      "driver_license_category": null,
      "serial_number": null,
      "observation": "10"
    }
  ],
  "meta": { "now": 1580483493, "ip": "172.23.0.1" }
}
```

### GET Listar

```
https://api.pontomais.com.br/external_api/v1/employees?active=true&attributes=id,first_name,last_name,email,pin,is_clt,cpf,nis,registration_number,time_card_source,has_time_cards,use_qrcode,enable_geolocation,work_hours,cost_center,user,enable_offline_time_cards,login&count=true&page={{page_number}}&per_page=10&sort_direction=asc&sort_property=first_name&incluirAnexos=false
```

Lista os colaboradores.

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| registration_number | String (15) | Matrícula |
| first_name | String (50) | Primeiro nome |
| last_name | String (50) | Sobrenome |
| cpf | String (14) | CPF |
| birthdate | Date | Data de nascimento |
| is_clt | Boolean | É CLT? (true - sim / false - não) |
| is_retired | Boolean | É aposentado? (true - sim / false - não) |
| main_phone_number | String (16) | Telefone principal |
| nis | String (14) | PIS |
| user | Integer | ID do usuário |
| team | Integer | ID da equipe |
| cost_center | Integer | ID do centro de custo |
| job_title | Integer | ID do cargo atual |
| shift | Integer | ID do turno atual |
| gender | Integer | Gênero |
| email | String (60) | E-mail |
| address | Integer | ID do endereço |
| active | Boolean | Ativo? (true - sim / false - não) |
| has_time_cards | Boolean | Registra ponto? (true - sim / false - não) |
| time_card_source | Integer | Método de registro (verificar a tabela Opções do time_card_source) |
| work_hours | String (40) | Jornada contratada |
| pin | String (4) | Número do PIN |
| qrcode | String (255) | Código do QR Code |
| use_qrcode | Boolean | Usa QR Code? (true - sim / false - não) |
| geolocation_enabled | Boolean | Localização habilitada? (true - sim / false - não) |
| hourly_rate | Float | Valor Hora |
| login | String (255) | Login do colaborador |

**Parâmetros na URL** (todos opcionais)

| Nome | Tipo | Descrição |
|---|---|---|
| incluirAnexos | Boolean | Anexos do colaborador (true or false) |

**Opções do `time_card_source`**

| Valor | Descrição |
|---|---|
| 1 | Registra ponto pelo Relógio Ponto |
| 2 | Registra ponto pela Pontomais |

**Filtros disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| name | String (50) | Filtra por nome |
| cpf | String (14) | Filtra por CPF |
| id | Integer | filtra por ID |
| nis | String (14) | Filtra por PIS |
| registration_number | String (15) | Filtra por matrícula |
| email | String (60) | Filtra por e-mail |
| business_unit_id | Integer | Filtra por ID da unidade à qual o colaborador pertence |
| department_id | Integer | Filtra pelo ID do departamento ao qual o colaborador pertence |
| team_id | Integer | Filtra pelo ID da equipe à qual o colaborador pertence |
| cost_center_id | Integer | Filtra pelo ID do centro de custos ao qual o colaborador pertence |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| active | true | Se true retorna apenas ativos caso contrário os inativos |
| attributes | id,first_name,last_name,email,pin,is_clt,cpf,nis,registration_number,time_card_source,has_time_cards,use_qrcode,enable_geolocation,work_hours,cost_center,user,enable_offline_time_cards,login | Atributos (ver disponíveis acima) |
| count | true | Retorna a quantidade de registros encontrados |
| page | {{page_number}} | Número da página |
| per_page | 10 | Número de itens por página |
| sort_direction | asc | Direção da ordenação (asc/desc) |
| sort_property | first_name | Atributo para ordenação |
| cpf | 873.416.870-29 | |
| incluirAnexos | false | |

**Example Request (Exemplo de listagem com sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees?active=false&attributes=id%2Cname&count=true&page={{page_number}}&per_page=10&sort_direction=asc&sort_property=first_name' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "employees": [
    { "id": 23732, "name": "Abraão Doe" },
    { "id": 42, "name": "André Doe" },
    { "id": 46322, "name": "Daniela Doe" },
    { "id": 20, "name": "Fernando Doe" },
    { "id": 372, "name": "João Silva" },
    { "id": 14106, "name": "Mauricio Doe" },
    { "id": 23533, "name": "John Doe" },
    { "id": 18611, "name": "Maria Doe" },
    { "id": 55134, "name": "José Doe" },
    { "id": 27770, "name": "Gustavo Doe" }
  ],
  "meta": { "now": 1531851467, "ip": "127.0.0.1", "count": 14 }
}
```

### GET Detalhar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}?attributes=id,first_name,last_name,email,pin,is_clt,cpf,nis,registration_number,time_card_source,has_time_cards,use_qrcode,enable_geolocation,work_hours,cost_center,user,enable_offline_time_cards
```

Exibe os atributos de um colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |

**Atributos disponíveis:** iguais ao GET Listar acima.

**Opções do `time_card_source`**

| Valor | Descrição |
|---|---|
| 1 | Registra ponto pelo Relógio Ponto |
| 2 | Registra ponto pela Pontomais |

**Filtros disponíveis:** iguais ao GET Listar acima.

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**PARAMS**

| Nome | Valor |
|---|---|
| attributes | id,first_name,last_name,email,pin,is_clt,cpf,nis,registration_number,time_card_source,has_time_cards,use_qrcode,enable_geolocation,work_hours,cost_center,user,enable_offline_time_cards |

**Example Request (Exemplo de detalhe com sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}?attributes=id%2Cfirst_name%2Clast_name%2Cemail%2Cpin%2Cis_clt%2Ccpf%2Cnis%2Cregistration_number%2Ctime_card_source%2Chas_time_cards%2Cuse_qrcode%2Cenable_geolocation%2Cwork_hours%2Ccost_center%2Cuser%2Cenable_offline_time_cards' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "employee": {
    "id": 8,
    "first_name": "Frodo",
    "last_name": "Bolseiro",
    "email": "frodo@pontomais.com.br",
    "pin": "",
    "is_clt": true,
    "cpf": "999.999.999-99",
    "nis": "999.99999.99-9",
    "registration_number": "456",
    "time_card_source": { "id": 2, "name": "Pontomais" },
    "has_time_cards": true,
    "use_qrcode": false,
    "enable_geolocation": { "id": 0, "name": "Usar configuração da conta" },
    "work_hours": null,
    "cost_center": { "id": 2, "code": "0001", "name": "Geral" },
    "user": {
      "id": 7,
      "email": "frodo@pontomais.com.br",
      "active": true,
      "admin": false,
      "confirmed_at": null,
      "group": { "id": 4, "name": "Colaboradores" }
    },
    "enable_offline_time_cards": { "id": 0, "name": "Usar configuração da conta" }
  },
  "meta": { "now": 1583871105, "ip": "172.26.0.1" }
}
```

### POST Criar

```
https://api.pontomais.com.br/external_api/v1/employees
```

Inclui um Colaborador.

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| registration_number | String (15) | Não | Matrícula |
| name | String (100) | Sim | Nome e sobrenome |
| cpf | String (14) | Sim | CPF |
| initial_date | Date | Sim | Data de início no Controle de ponto |
| is_clt | Boolean | Não | É CLT? (true - sim/false - não) |
| live_abroad | Boolean | Não | É Estrangeiro? (true - sim/false - não) |
| nis | String (14) | Não | PIS - Obrigatório quando a configuração "Coletar PIS no cadastro de colaboradores" (Configurações > Relógios ponto) estiver marcada como "Sim" |
| team_id | Integer | Sim | ID da equipe |
| cost_center_id | Integer | Sim | ID do centro de custo |
| job_title_id | Integer | Sim | ID do cargo atual |
| shift_id | Integer | Sim | ID do turno atual |
| client_preference_id | Integer | Sim | ID da configuração de controle de ponto. Consulte a lista em Preferências (Configurações de controle de ponto) |
| email | String (60) | Não | E-mail |
| has_time_cards | Boolean | Não | Registra ponto? (true - sim/false - não) |
| time_card_source | Integer | Não | Método de registro (verificar a tabela Opções do time_card_source) |
| admission_date | Date | Sim | Data de admissão |
| picture | String | Não | Imagem do colaborador em Base64 |
| group_id | Integer | Não | ID do grupo de acesso (Obrigatório quando "Método de registro" for "Reconhecimento Facial"), ver endpoint Usuários->Grupos de Acesso->Listar |
| password | String | Não | Senha para acesso (Obrigatório quando "Método de registro" for "Reconhecimento Facial") |
| whats_app_number | String | Não | formato esperado (99) 99999-9999 ou (99) 9999-9999. Se informado irá ativar o registro de ponto por WhatsApp desde que: o cliente tenha integração com WhatsApp, o número não exista para outro colaborador, has_time_cards seja true, e time_card_source seja = 2 |
| business_unit_cnpj_cpf | Array | Não | Array de CNPJ/CPF das unidades de negócios que deseja vincular o colaborador |
| vacation_configuration_id | Integer | Não | Configuração de férias. Envie nulo para selecionar a opção "Não fazer a gestão de férias através da extensão Férias e folgas" |
| gender | Integer | Não | Gênero (verificar a tabela Opções de Gender) |
| mothers_name | String | Não | Nome da mãe |
| marital_status | Integer | Não | Estado Civil (verificar a tabela Marital Status) |
| race | Integer | Não | Etnia (verificar a tabela Opções de Race) |
| instruction_level | Integer | Não | Escolaridade (verificar a tabela Opções de Instruction Level) |
| birthdate | Integer | Não | Data de Nascimento |
| attachments | Array | Não | Lista de anexos do colaborador |

**Estrutura do campo `attachments`**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| name | String | Sim | Nome do anexo |
| attachment_type | Integer | Sim | Tipo do anexo (ver tabela abaixo) |
| file | String | Sim | Arquivo em Base64 |

**Opções de `attachment_type`**

| Valor | Descrição |
|---|---|
| 1 | RG |
| 2 | RIC |
| 3 | RNE |
| 4 | OC |
| 5 | CNH |
| 6 | Carteira de Trabalho |
| 7 | Outros |

**Opções do `time_card_source`**

| Valor | Descrição |
|---|---|
| 0 | Caso o colaborador não registre ponto |
| 1 | Relógio Ponto |
| 2 | Registro Simples |
| 3 | QR Code |
| 4 | Reconhecimento Facial |
| 5 | Registro Simples com Foto |

**Opções do `address_type`**

| Valor | Descrição |
|---|---|
| 1 | Unidade |
| 2 | Local do colaborador |
| 3 | Estrangeiro do colaborador |
| 4 | Cliente |
| 5 | Faturamento |

**Opções do `street_type`**

| Valor | Descrição |
|---|---|
| 1 | Alameda |
| 2 | Avenida |
| 3 | Balneário |
| 4 | Bloco |
| 5 | Chácara |
| 6 | Conjunto |
| 7 | Condomínio |
| 8 | Estrada |
| 9 | Fazenda |
| 10 | Galeria |
| 11 | Granja |
| 12 | Jardim |
| 13 | Largo |
| 14 | Loteamento |
| 15 | Praça |
| 16 | Praia |
| 17 | Parque |
| 18 | Quadra |
| 19 | Rua |
| 20 | Setor |
| 21 | Travessa |
| 22 | Vila |
| 23 | Rodovia |

**Opções de `gender`**

| Valor | Descrição |
|---|---|
| 1 | Masculino |
| 2 | Feminino |

**Opções de `enable_geolocation`**

| Valor | Descrição |
|---|---|
| 0 | Usar configuração da conta |
| 1 | Permitir |
| 2 | Não permitir |

**Opções de `enable_offline_time_cards`**

| Valor | Descrição |
|---|---|
| 0 | Usar configuração da conta |
| 1 | Permitir |
| 2 | Não permitir |

**Opções de `contract_type`**

| Valor | Descrição |
|---|---|
| 0 | Mensalista |
| 1 | Comissionista |

**Opções de `race` (Etnia)**

| Valor | Descrição |
|---|---|
| 1 | Branca |
| 2 | Negra |
| 3 | Parda (parda ou declarada como mulata, cabocla, cafuza, mameluca ou mestiça de negro com pessoa de outra cor ou raça) |
| 4 | Amarela (de origem japonesa, chinesa, coreana etc) |
| 5 | Indígena |
| 6 | Não informado |

**Opções de `marital_status` (Estado Civil)**

| Valor | Descrição |
|---|---|
| 1 | Solteiro |
| 2 | Casado |
| 3 | Divorciado |
| 4 | Separado |
| 5 | Viúvo |

**Opções de `instruction_level` (Escolaridade)**

| Valor | Descrição |
|---|---|
| 1 | Analfabeto, inclusive o que, embora tenha recebido instrução, não se alfabetizou |
| 2 | Até o 5º ano incompleto do Ensino Fundamental (antiga 4ª série) ou que se tenha alfabetizado sem ter frequentado escola regular |
| 3 | 5º ano completo do Ensino Fundamental |
| 4 | Do 6º ao 9º ano do Ensino Fundamental incompleto (antiga 5ª a 8ª série) |
| 5 | Ensino Fundamental Completo |
| 6 | Ensino Médio incompleto |
| 7 | Ensino Médio completo |
| 8 | Educação Superior incompleta |
| 9 | Educação Superior completa |
| 10 | Pós-Graduação completa |
| 11 | Mestrado completo |
| 12 | Doutorado completo |

**Opções de `foreign_visa_type`**

| Valor | Descrição |
|---|---|
| 1 | Visto permanente |
| 2 | Visto temporário |
| 3 | Asilado |
| 4 | Refugiado |
| 5 | Solicitante de Refúgio |
| 6 | Residente em país fronteiriço ao Brasil |
| 7 | Deficiente físico e com mais de 51 anos |
| 8 | Com residência provisória e anistiado, em situação irregular |
| 9 | Permanência no Brasil em razão de filhos ou cônjuge brasileiros |
| 10 | Beneficiado pelo acordo entre países do Mercosul |
| 11 | Dependente de agente diplomático e/ou consular de países que mantém convênio de reciprocidade para o exercício de atividade remunerada no Brasil |
| 12 | Beneficiado pelo Tratado de Amizade, Cooperação e Consulta entre a República Federativa do Brasil e a República Portuguesa |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Example Request (Exemplo de sucesso ao cadastrar)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/employees' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data-raw '{
"employee":
{
"name": "Darth Vader",
"nis": "999.99999.99-9",
"registration_number": "0001",
"cpf": "999.999.999-99",
"is_clt": true,
"email": "darth.vader@pontomais.com.br",
"admission_date": "22/02/2017",
"shift_id": 19631,
"job_title_id": 6,
"cost_center_id": 7,
"team_id": 10,
"live_abroad": false
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": "Colaborador cadastrado com sucesso!",
  "meta": { "now": 1531851946, "ip": "127.0.0.1" },
  "id": 55135
}
```

### PUT Editar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}
```

Edita um colaborador.

Para alterar o turno (shift_id) do colaborador, use o endpoint Colaboradores / Movimentações / Turno / Criar. Para alterar a equipe (team_id) do colaborador (e por consequência, seu Departamento e Unidade de Negócio), use o endpoint Colaboradores / Movimentações / Equipe / Criar. Para alterar o cargo (job_title_id), use o endpoint Colaboradores / Movimentações / Cargo / Criar.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| registration_number | String (15) | Não | Matrícula |
| name | String (100) | Sim | Nome e sobrenome |
| cpf | String (14) | Não | CPF |
| is_clt | Boolean | Não | É CLT? (true - sim/false - não) |
| live_abroad | Boolean | Não | É Estrangeiro? (true - sim/false - não) |
| nis | String (14) | Não | PIS - Obrigatório quando a configuração "Coletar PIS no cadastro de colaboradores" estiver marcada como "Sim" |
| client_preference_id | Integer | Não | ID da configuração de controle de ponto |
| email | String (60) | Não | E-mail |
| has_time_cards | Boolean | Não | Registra ponto? (true - sim/false - não) |
| time_card_source | Integer | Não | Método de registro (verificar a tabela Opções do time_card_source) |
| admission_date | Date | Sim | Data de admissão |
| picture | String | Não | Imagem do colaborador em Base64 |
| hourly_rate | Float | Não | Valor/Hora |
| cost_center_id | Integer | Sim | ID do centro de custo |
| group_id | Integer | Não | ID do grupo de acesso (Obrigatório quando "Método de registro" for "Reconhecimento Facial") |
| password | String | Não | Senha para acesso (Obrigatório quando "Método de registro" for "Reconhecimento Facial") |
| whats_app_number | String | Não | formato esperado (99) 99999-9999 ou (99) 9999-9999 |
| disable_time_recording_by_whatsapp | Boolean | Não | Se = true desabilita o registro de ponto por WhatsApp |
| business_unit_cnpj_cpf | Array | Não | Array de CNPJ/CPF das unidades de negócios |
| vacation_configuration_id | Integer | Não | Configuração de férias |
| gender | Integer | Não | Gênero (verificar a tabela Opções de Gender) |
| login | String | Não | Login do colaborador |
| attachments | Array | Não | Lista de anexos do colaborador |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Example Request (Exemplo de edição com sucesso)**

```bash
curl --location -g --request PUT 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data-raw '{
"employee":
{
"name": "Darth Vader",
"nis": "999.99999.99-9",
"registration_number": "0001",
"cpf": "999.999.999-99",
"is_clt": true,
"email": "darth.vader@pontomais.com.br",
"admission_date": "22/02/2017",
"shift_id": 19631,
"job_title_id": 6,
"cost_center_id": 7,
"team_id": 10,
"live_abroad": false
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": "Colaborador editado com sucesso!",
  "meta": { "now": 1531853380, "ip": "127.0.0.1" },
  "id": 55135
}
```

### PUT Demitir

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/dismiss
```

Demite um Colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| date | Date | Sim | Data da demissão |
| effective_date | Date | Não | Data efetiva da demissão (Caso não seja enviado, é considerado o campo date) |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Body (raw)**

```json
{
  "employee": {
    "date": "2021-02-01"
  }
}
```

**Example Request (Exemplo de falha ao demitir)**

```bash
curl --location -g --request PUT 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/dismiss' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"employee":
{
"date":"2018-07-17",
"effective_date":"2018-07-17",
"motive":2
}
}'
```

**Example Response — 422 UNPROCESSABLE ENTITY**

```json
{
  "errors": { "date": ["Já está em uso"] },
  "meta": { "now": 1531854230, "ip": "127.0.0.1" }
}
```

### POST Verifica se existe

```
https://api.pontomais.com.br/external_api/v1/employees/exists
```

Verifica se um colaborador já existe na base com o mesmo CPF ou PIS (nis).

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Descrição |
|---|---|---|
| cpf | String (14) | CPF |
| nis | String (14) | PIS |

**Retorno**

Retorna uma lista de unidades de negócio onde o colaborador encontra-se cadastrado, ativo ou não. O `id` se refere ao ID do colaborador.

```json
{
  "employees": [
    { "id": 1, "business_unit_id": 573, "business_unit_name": "Matriz", "active": false },
    { "id": 1, "business_unit_id": 43, "business_unit_name": "Filial", "active": true }
  ]
}
```

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente |
| hcm-token | {{hcm-token}} | Token do cliente |

**Body (raw)**

```json
{
  "employee": {
    "cpf": "99999999999",
    "nis": "38266910278"
  }
}
```

**Example Request (Exemplo de verificação com sucesso)**

```bash
curl --location --request PUT 'https://api.pontomais.com.br/external_api/v1/employees/exists' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"employee":
{
"cpf":"999.999.999-99",
"nis":"999.99999.99-9"
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "employees": [
    { "id": 1, "business_unit_id": 573, "business_unit_name": "Móju", "active": false },
    { "id": 1, "business_unit_id": 43, "business_unit_name": "Filial 2", "active": true }
  ],
  "meta": { "now": 1618428400, "ip": "186.225.20.33", "ids": [1, 2] }
}
```

### GET Verifica status do colaborador

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/status
```

Exibe o status atual do colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | ID do colaborador |

**Legenda da resposta**

| Status | Nome | Descrição |
|---|---|---|
| 1 | Em jornada | Quando o colaborador está trabalhando (nº ímpar de pontos) |
| 2 | Intervalo | Quando o colaborador saiu para almoço (nº par de pontos e menor que o nº de pontos que deve ter na jornada) |
| 3 | Ausente | Quando é dia de trabalho e o colaborador ainda não registrou pontos, mas o horário de entrada dele ainda não chegou. Ex: agora são 6h e ele entra às 8h |
| 5 | Expediente encerrado | Quando o colaborador tem nº par de pontos e já registrou o total de pontos que deveria ter no turno. Ex: Colaborador registrou o 4º ponto do dia e no cadastro do turno tem 2 entradas e 2 saídas |
| 6 | De folga | Quando o dia atual não é dia de trabalho e o colaborador não iniciou jornada |
| 7 | Atrasado | Quando o colaborador não registrou pontos e o horário de entrada dele já passou. Ex: agora são 08:20h e ele entra às 8h |
| 8 | Trabalhando em dia de folga | Quando o dia atual não é dia de trabalho e o colaborador iniciou jornada |
| 9 | Afastado | Quando no dia atual o colaborador se encontra afastado |
| 10 | Trabalhando em dia que está afastado | Quando no dia atual o colaborador se encontra afastado mas está trabalhando |
| 11 | De férias | Quando no dia atual o colaborador se encontra de férias |
| 12 | Trabalhando em dia de férias | Quando no dia atual o colaborador se encontra de férias mas está trabalhando |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**Example Request (Exemplo de verificação com sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/status' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "success": "Status do colaborador obtido com sucesso !",
  "meta": { "now": 1536179719, "ip": "127.0.0.1" },
  "status": 7
}
```

### GET Verifica se existe

```
https://api.pontomais.com.br/external_api/v1/employees/exists
```

Verifica se um colaborador já existe na base com o mesmo CPF ou PIS (nis).

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Descrição |
|---|---|---|
| cpf | String (14) | CPF |
| nis | String (14) | PIS |

**Retorno**

Retorna uma lista de unidades de negócio onde o colaborador encontra-se cadastrado, ativo ou não. O `id` se refere ao ID do colaborador.

```json
{
  "employees": [
    { "id": 1, "business_unit_id": 573, "business_unit_name": "Matriz", "active": false },
    { "id": 1, "business_unit_id": 43, "business_unit_name": "Filial", "active": true }
  ]
}
```

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| hcm-token | {{client_token}} | Token do cliente |

**Body (raw)**

```json
{
  "employee": {
    "cpf": "99999999999",
    "nis": "38266910278"
  }
}
```

**Example Request (Exemplo de verificação com sucesso)**

```bash
curl --location --request GET 'https://api.pontomais.com.br/external_api/v1/employees/exists' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"employee":
{
"cpf":"999.999.999-99",
"nis":"999.99999.99-9"
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "employees": [
    { "id": 1, "business_unit_id": 573, "business_unit_name": "Móju", "active": false },
    { "id": 1, "business_unit_id": 43, "business_unit_name": "Filial 2", "active": true }
  ],
  "meta": { "now": 1618428400, "ip": "186.225.20.33", "ids": [1, 2] }
}
```

---

## Banco de horas

### GET Listar

```
https://api.pontomais.com.br/external_api/v1/time_balance_entries?employee_id={{employee_id}}&withdraw=true&count=true&page=1&per_page=10&sort_property=date&sort_direction=desc&attributes=id,date,withdraw,amount,employee_id,observation,updated_by
```

Lista os lançamentos manuais do banco de horas.

**Parâmetros na URL**

| Nome | Tipo | Descrição |
|---|---|---|
| employee_id | Integer | ID do colaborador a ser filtrado |
| withdraw | Boolean | Filtragem de lançamentos por tipo de operação, crédito e débito (true - lista apenas débitos / false - lista apenas créditos) |
| page | Integer | Número da página atual |
| per_page | Integer | Quantidade de unidades de negócio por página |
| count | Boolean | Total de lançamentos retornados na listagem (true - exibe contador / false - oculta contador) |
| sort_property | String | Atributo que a listagem deve considerar para ordenar os lançamentos |
| sort_direction | String | Direção em que a listagem deve classificar os lançamentos (asc - ascendente / desc - descendente) |
| attributes | String | Atributos, separados por vírgula, a serem exibidos em cada lançamento |

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| created_at | Timestamp | Data e horário de criação do lançamento |
| updated_at | Timestamp | Data e horário de atualização do lançamento |
| date | Date | Data a qual o lançamento se refere |
| withdraw | Boolean | Indica se a operação é débito (true - débito / false - crédito) |
| amount | Float | Valor do lançamento em segundos |
| signed_amount | Float | Valor do lançamento em segundos e com sinalização |
| signed_amount_humanized | String | Valor do lançamento em formato de horário e com sinalização |
| work_day_id | Integer | ID da consolidação |
| employee_id | Integer | ID do colaborador |
| updated_by | Object | Colaborador que realizou o lançamento (ver formato do objeto) |
| observation | String | Motivo do lançamento |

**Formato do objeto `updated_by`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String | Nome do colaborador |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor |
|---|---|
| employee_id | {{employee_id}} |
| withdraw | true |
| count | true |
| page | 1 |
| per_page | 10 |
| sort_property | date |
| sort_direction | desc |
| attributes | id,date,withdraw,amount,employee_id,observation,updated_by |

**Example Request (Listar)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/time_balance_entries?employee_id={{employee_id}}&withdraw=true&count=true&page=1&per_page=10&sort_property=date&sort_direction=desc&attributes=id%2Cdate%2Cwithdraw%2Camount%2Cemployee_id%2Cobservation%2Cupdated_by' \
--header 'access-token: {{client_token}}'
```

**Example Response:** Sem corpo de resposta (this request doesn't return any response body)

### GET Detalhar

```
https://api.pontomais.com.br/external_api/v1/time_balance_entries/{{time_balance_entry_id}}?attributes=id,date,withdraw,amount,employee_id,observation,updated_by
```

Exibe os atributos de um lançamento de banco de horas.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| time_balance_entry_id | Integer | Sim | ID do lançamento |

**Parâmetros na URL** (todos opcionais)

| Nome | Tipo | Descrição |
|---|---|---|
| attributes | String | Atributos, separados por vírgula, a serem exibidos em cada lançamento |

**Atributos disponíveis:** iguais ao GET Listar acima.

**Formato do objeto `updated_by`:** igual ao GET Listar acima.

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor |
|---|---|
| attributes | id,date,withdraw,amount,employee_id,observation,updated_by |

**Example Request (Exemplo de falha)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/time_balance_entries/99' \
--header 'access-token: {{client_token}}'
```

**Example Response — 404 NOT FOUND**

```json
{
  "error": "Registro não encontrado",
  "meta": { "now": 1605562384, "ip": "172.20.0.1" }
}
```

### POST Criar

```
https://api.pontomais.com.br/external_api/v1/time_balance_entries
```

Cria um lançamento de banco de horas.

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| amount | Float | Sim | Valor do lançamento em segundos |
| date | Date | Sim | Data a qual o lançamento se refere |
| employee_id | Integer | Sim | ID do colaborador |
| observation | String | Sim | Motivo do lançamento |
| withdraw | Boolean | Não | Indica se a operação é débito. Se o atributo não estiver presente, o lançamento será do tipo crédito (true - débito / false - crédito) |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente |

**Body (raw)**

```json
{
  "time_balance_entry": {
    "amount": {{amount}},
    "date": "2020-01-20",
    "employee_id": {{employee_id}},
    "observation": "Mussum Ipsum, cacilds vidis litro abertis. Paisis, filhis, espiritis santis. Detraxit consequat et quo num tendi nada. Suco de cevadiss, é um leite divinis, qui tem lupuliz, matis, aguis e fermentis. Sapien in monti palavris qui num significa nadis i pareci latim.",
    "withdraw": {{withdraw}}
  }
}
```

**Example Request (Exemplo de falha)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/time_balance_entries' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"time_balance_entry":
{
"amount": 7200.0,
"date": "2020-11-02",
"employee_id": 3,

"withdraw": true
}
}'
```

**Example Response — 422 UNPROCESSABLE ENTITY**

```json
{
  "errors": { "observation": ["Não pode ficar em branco"] },
  "meta": { "now": 1605562161, "ip": "172.20.0.1" }
}
```

### PUT Editar

```
https://api.pontomais.com.br/external_api/v1/time_balance_entries/59
```

Edita um lançamento de banco de horas.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| time_balance_entry_id | Integer | Sim | ID do lançamento |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| amount | Float | Não | Valor do lançamento em segundos |
| date | Date | Não | Data a qual o lançamento se refere |
| employee_id | Integer | Não | ID do colaborador |
| observation | String | Não | Motivo do lançamento |
| withdraw | Boolean | Não | Indica se a operação é débito. Se o atributo não estiver presente, o lançamento será do tipo crédito (true - débito / false - crédito) |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json | |
| access-token | {{client_token}} | Token do cliente |

**Body (raw)**

```json
{
  "time_balance_entry": {
    "amount": {{amount}},
    "date": "2020-01-20",
    "observation": "Mussum Ipsum, cacilds vidis litro abertis. Paisis, filhis, espiritis santis. Detraxit consequat et quo num tendi nada. Suco de cevadiss, é um leite divinis, qui tem lupuliz, matis, aguis e fermentis. Sapien in monti palavris qui num significa nadis i pareci latim.",
    "withdraw": {{withdraw}}
  }
}
```

**Example Request (Exemplo de sucesso)**

```bash
curl --location --request PUT 'https://api.pontomais.com.br/external_api/v1/time_balance_entries/14' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"time_balance_entry":
{
"amount": 7200,
"date": "2020-11-03",
"observation": "Lorem ipsum",
"withdraw": false
}
}'
```

**Example Response — 200 OK**

```json
{
  "success": "Saldo de banco de horas atualizado com sucesso!",
  "meta": { "now": 1605562543, "ip": "172.20.0.1" }
}
```

### DELETE Excluir

```
https://api.pontomais.com.br/external_api/v1/time_balance_entries/{{time_balance_entry_id}}
```

Exclui um lançamento de banco de horas.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| time_balance_entry_id | Integer | Sim | ID do lançamento |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**Example Request (Exemplo de sucesso)**

```bash
curl --location --request DELETE 'https://api.pontomais.com.br/external_api/v1/time_balance_entries/15' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "success": "Saldo de banco de horas removido com sucesso!",
  "meta": { "now": 1605562471, "ip": "172.20.0.1" }
}
```

---

## Turnos

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | number | identificador único |
| code | string | código |
| name | string | nome |
| active | boolean | ativo |
| shift_type | number | tipo do turno, ver tabela tipo do turno |
| without_holidays | boolean | ignora feriados |
| flexible | boolean | jornada flexível |
| flexible_interval | boolean | intervalo flexível |
| auto_interval | boolean | intervalo pré-assinalado |

### V2

#### POST Criar Turno com horários - Semanal

```
https://api.pontomais.com.br/external_api/v2/shifts
```

Cadastra um turno semanal (quando os dias de descanso são em dias fixos da semana).

**Atributos disponíveis**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| code | String (60) | Sim (não pode se repetir) | Código identificador do turno |
| name | String (60) | Sim | Nome do turno |
| shift_type | Integer | Sim | Fixo 1 (Semanal) |
| days | Array of objects | Sim | Definição dos horários de trabalho para cada dia da semana (ver tabela `days`) |

**Atributo `days`**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| day_change_time | String (5) | Não | O horário de virada do dia ("HH:MM"). Pontos batidos após esse horário serão considerados como pertencentes ao dia seguinte. Quando não preenchido, o sistema calculará um valor automaticamente |
| extra_time_50_percent | String (5) | Não | A quantidade de horas extras ("HH:MM") que serão contabilizadas no fator 1. Horas que ultrapassarem esse limite serão contabilizadas como fator 2. Quando não preenchido, o sistema adotará o valor padrão "02:00" |
| week_day | Integer | Sim | O dia da semana (1 a 7). Ver tabela "Dias da Semana" |
| week_index | Integer | Sim | Caso seja uma única semana de trabalho, preencha com 0 em todos os dias. Caso sejam várias semanas, cada uma com horários distintos, preencha os dias da primeira semana com 0, da segunda semana com 1, e assim por diante |
| periods | Array of objects | Sim | Definição dos horários de trabalho. Caso o dia seja de descanso, informe um array vazio ([]) |

**Atributo `periods`** (informe quantos períodos forem necessários no dia; dias diferentes podem ter quantidade de períodos diferente; em dia de descanso deixe o array vazio)

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| enter_time | String (5) | Sim | Horário de entrada ("HH:MM") |
| leave_time | String (5) | Sim | Horário de saída ("HH:MM") |
| main_interval_after | Boolean | Não | Se o intervalo principal do colaborador ocorre imediatamente após esse período, informe true. Caso contrário informe false |

**Dias da Semana**

| Código | Dia da Semana |
|---|---|
| 1 | Domingo |
| 2 | Segunda-Feira |
| 3 | Terça-Feira |
| 4 | Quarta-Feira |
| 5 | Quinta-Feira |
| 6 | Sexta-Feira |
| 7 | Sábado |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**Body (raw json)**

```json
{
  "shift": {
    "code": "0123",
    "shift_type": 1,
    "name": "Semanal",
    "days": [
      { "day_change_time": "23:59", "extra_time_50_percent": null, "week_day": 1, "week_index": 0, "periods": [] },
      { "day_change_time": "23:59", "extra_time_50_percent": null, "week_day": 2, "week_index": 0, "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": true },
        { "enter_time": "14:00", "leave_time": "18:00", "main_interval_after": false }
      ]},
      { "day_change_time": "23:59", "extra_time_50_percent": null, "week_day": 3, "week_index": 0, "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": true },
        { "enter_time": "14:00", "leave_time": "18:00", "main_interval_after": false }
      ]},
      { "day_change_time": "23:59", "extra_time_50_percent": null, "week_day": 4, "week_index": 0, "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": true },
        { "enter_time": "14:00", "leave_time": "18:00", "main_interval_after": false }
      ]},
      { "day_change_time": "23:59", "extra_time_50_percent": null, "week_day": 5, "week_index": 0, "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": true },
        { "enter_time": "14:00", "leave_time": "18:00", "main_interval_after": false }
      ]},
      { "day_change_time": "23:59", "extra_time_50_percent": null, "week_day": 6, "week_index": 0, "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": true },
        { "enter_time": "14:00", "leave_time": "18:00", "main_interval_after": false }
      ]},
      { "day_change_time": "23:59", "extra_time_50_percent": null, "week_day": 7, "week_index": 0, "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": false }
      ]}
    ]
  }
}
```

**Example Request (Exemplo bem sucedido)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v2/shifts' \
--header 'access-token: {{client_token}}' \
--data '{
"shift": {
"code": "0123",
"shift_type": 1,
"name": "Semanal",
"days": [
{"day_change_time": "23:59","extra_time_50_percent": null,"week_day": 1,"week_index": 0,"periods": []},
{"day_change_time": "23:59","extra_time_50_percent": null,"week_day": 2,"week_index": 0,"periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": true},{"enter_time": "14:00","leave_time": "18:00","main_interval_after": false}]},
{"day_change_time": "23:59","extra_time_50_percent": null,"week_day": 3,"week_index": 0,"periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": true},{"enter_time": "14:00","leave_time": "18:00","main_interval_after": false}]},
{"day_change_time": "23:59","extra_time_50_percent": null,"week_day": 4,"week_index": 0,"periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": true},{"enter_time": "14:00","leave_time": "18:00","main_interval_after": false}]},
{"day_change_time": "23:59","extra_time_50_percent": null,"week_day": 5,"week_index": 0,"periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": true},{"enter_time": "14:00","leave_time": "18:00","main_interval_after": false}]},
{"day_change_time": "23:59","extra_time_50_percent": null,"week_day": 6,"week_index": 0,"periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": true},{"enter_time": "14:00","leave_time": "18:00","main_interval_after": false}]},
{"day_change_time": "23:59","extra_time_50_percent": null,"week_day": 7,"week_index": 0,"periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": false}]}
]
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": "Turno cadastrado.",
  "id": 235,
  "meta": { "now": 1752682885, "ip": "172.16.57.1", "obfuscated": false }
}
```

#### POST Criar Turno com horários - 12h/36h

```
https://api.pontomais.com.br/external_api/v2/shifts
```

Cadastra um turno 12h/36h (quando se trabalha 12 horas e descansa nas 36 horas seguintes).

**Atributos disponíveis**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| code | String (60) | Sim (não pode se repetir) | Código identificador do turno |
| name | String (60) | Sim | Nome do turno |
| shift_type | Integer | Sim | Fixo 2 (12h/36h) |
| days | Array of objects | Sim | Definição dos horários de trabalho (ver tabela `days`) |

**Atributo `days`** (nota: o dia de descanso pode ser omitido; nesse caso, ele terá o mesmo Limite de Hora Extra do dia de trabalho)

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| day_change_time | String (5) | Não | O horário de virada do dia ("HH:MM") |
| extra_time_50_percent | String (5) | Não | A quantidade de horas extras ("HH:MM") contabilizadas no fator 1; padrão "02:00" se não preenchido |
| cyclic_day | Integer | Sim | Fixo: 1 para o dia de trabalho, 2 para o dia de descanso |
| periods | Array of objects | Sim | Definição dos horários de trabalho. No dia de descanso, deve ser informado um array vazio |

**Atributo `periods`**

| Tipo | Obrigatório | Descrição |
|---|---|---|
| enter_time | String (5) | Sim — Horário de entrada ("HH:MM") |
| leave_time | String (5) | Sim — Horário de saída ("HH:MM") |
| main_interval_after | Boolean | Não — true se o intervalo principal ocorre imediatamente após esse período |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**Body (raw json)**

```json
{
  "shift": {
    "code": "0124",
    "shift_type": 2,
    "name": "12h/36h",
    "days": [
      { "day_change_time": "23:59", "extra_time_50_percent": null, "cyclic_day": 1, "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": true },
        { "enter_time": "14:00", "leave_time": "18:00", "main_interval_after": false }
      ]},
      { "day_change_time": "23:59", "extra_time_50_percent": null, "cyclic_day": 2, "periods": [] }
    ]
  }
}
```

**Example Request (Exemplo sucesso)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v2/shifts' \
--header 'access-token: {{client_token}}' \
--data '{
"shift": {
"code": "0124",
"shift_type": 2,
"name": "12h/36h",
"days": [
{"day_change_time": "23:59","extra_time_50_percent": null,"cyclic_day": 1,"periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": true},{"enter_time": "14:00","leave_time": "18:00","main_interval_after": false}]},
{"day_change_time": "23:59","extra_time_50_percent": null,"cyclic_day": 2,"periods": []}
]
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": "Turno cadastrado.",
  "id": 237,
  "meta": { "now": 1752773197, "ip": "172.16.57.1", "obfuscated": false }
}
```

#### POST Criar Turno com horários - 24h/72h

```
https://api.pontomais.com.br/external_api/v2/shifts
```

Cadastra um turno 24h/72h (quando se trabalha 24 horas seguidas e descansa nas 72 horas seguintes).

**Atributos disponíveis**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| code | String (60) | Sim (não pode se repetir) | Código identificador do turno |
| name | String (60) | Sim | Nome do turno |
| shift_type | Integer | Sim | Fixo 3 (24h/72h) |
| days | Array of objects | Sim | Definição dos horários de trabalho (ver tabela `days`) |

**Atributo `days`** (nota: os dias de descanso podem ser omitidos; nesse caso, eles terão o mesmo Limite de Hora Extra do dia de trabalho)

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| cyclic_day | Integer | Sim | Fixo: 1 para o dia de trabalho, 2 para o primeiro dia de descanso, 3 para o segundo dia de descanso, 4 para o terceiro dia de descanso |
| duration | Integer | Não | O tamanho da jornada, em horas. Informar apenas para o dia de trabalho. Quando não preenchido, o sistema atribuirá uma duração de 24 horas |
| extra_time_50_percent | String (5) | Não | A quantidade de horas extras ("HH:MM") contabilizadas no fator 1; padrão "02:00" se não preenchido |
| periods | Array of objects | Sim | Definição dos horários de trabalho. No dia de descanso, deve ser informado um array vazio |

**Atributo `periods`**

| Tipo | Obrigatório | Descrição |
|---|---|---|
| enter_time | String (5) | Sim — Horário de entrada ("HH:MM") |
| leave_time | String (5) | Sim — Horário de saída ("HH:MM") |
| main_interval_after | Boolean | Não — true se o intervalo principal ocorre imediatamente após esse período |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**Body (raw json)**

```json
{
  "shift": {
    "code": "0125",
    "shift_type": 3,
    "name": "24h/72h",
    "days": [
      { "cyclic_day": 1, "duration": 26, "extra_time_50_percent": "02:00", "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": true },
        { "enter_time": "14:00", "leave_time": "18:00", "main_interval_after": false },
        { "enter_time": "20:00", "leave_time": "01:00", "main_interval_after": false },
        { "enter_time": "02:00", "leave_time": "08:00", "main_interval_after": false }
      ]},
      { "cyclic_day": 2, "extra_time_50_percent": "12:00" },
      { "cyclic_day": 3, "extra_time_50_percent": "12:00" },
      { "cyclic_day": 4, "extra_time_50_percent": "12:00" }
    ]
  }
}
```

**Example Request (Exemplo sucesso)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v2/shifts' \
--header 'access-token: {{client_token}}' \
--data '{
"shift": {
"code": "0234",
"shift_type": 3,
"name": "24h/72h",
"days": [
{"cyclic_day": 1,"duration": 26,"extra_time_50_percent": "02:00","periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": true},{"enter_time": "14:00","leave_time": "18:00","main_interval_after": false},{"enter_time": "20:00","leave_time": "01:00","main_interval_after": false},{"enter_time": "02:00","leave_time": "08:00","main_interval_after": false}]},
{"cyclic_day": 2,"extra_time_50_percent": "12:00"},
{"cyclic_day": 3,"extra_time_50_percent": "12:00"},
{"cyclic_day": 4,"extra_time_50_percent": "12:00"}
]
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": "Turno cadastrado.",
  "id": 245,
  "meta": { "now": 1753185187, "ip": "172.16.57.1", "obfuscated": false }
}
```

#### POST Criar Turno com horários - 5d/1d

```
https://api.pontomais.com.br/external_api/v2/shifts
```

Cadastra um turno 5d/1d (quando se trabalha 5 dias seguidos e descansa no sexto dia).

**Atributos disponíveis**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| code | String (60) | Sim (Não pode se repetir) | Código identificador do turno |
| name | String (60) | Sim | Nome do turno |
| shift_type | Integer | Sim | Fixo 4 (5d/1d) |
| days | Array of objects | Sim | Definição dos horários de trabalho (ver tabela `days`) |

**Atributo `days`** (nota: os dias de descanso podem ser omitidos; nesse caso, eles terão o mesmo Limite de Hora Extra do dia de trabalho)

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| cyclic_day | Integer | Sim | Fixo: 1 para o primeiro dia de trabalho, 2 para o segundo dia de trabalho, 3 para o terceiro dia de trabalho, 4 para o quarto dia de trabalho, 5 para o quinto dia de trabalho, 6 para o dia de descanso |
| day_change_time | String (5) | Não | O horário de virada do dia ("HH:MM") |
| extra_time_50_percent | String (5) | Não | A quantidade de horas extras ("HH:MM") contabilizadas no fator 1; padrão "02:00" se não preenchido |
| periods | Array of objects | Sim | Definição dos horários de trabalho. No dia de descanso, deve ser informado um array vazio |

**Atributo `periods`**

| Tipo | Obrigatório | Descrição |
|---|---|---|
| enter_time | String (5) | Sim — Horário de entrada ("HH:MM") |
| leave_time | String (5) | Sim — Horário de saída ("HH:MM") |

> **[PENDENTE] Restante de "Turnos"** — variante 5d/1d incompleta (faltam `main_interval_after` e demais atributos de `periods`, exemplo de request/response), e faltam também: GET Listar, GET Detalhes, GET Listar dias, DELETE Excluir, PUT Desfazer exclusão. Depois de Turnos, faltam por completo as pastas **Usuários, AFD, AFD-671, AFDT, AEJ** (nesta ordem, antes de Relatórios).

---

## Relatórios

> Pasta com 27 relatórios distintos, todos via `POST /external_api/v1/reports/<nome>`, mesmo padrão de request (`start_date`, `end_date`, `group_by`, `row_filters`, `columns`, `format`). Apenas o relatório abaixo foi documentado até agora; os demais 26 (Jornada, Fechamento, Modelo AFD Portaria 1510, Abonos, Absenteísmo, Afastamentos e férias, Ajustes de ponto, Assinaturas, Atrasos, Auditoria, Banco de horas, Benefícios, Colaboradores, Equipes, Faltas, Horas Extras, Horista, Ocorrências, Pendências, Provisionamento, Registros de pausas, Resumo de jornada, Sobreaviso, Solicitações, Turnos, Vigência de Banco de Horas) seguem **[PENDENTE]**.

### POST Registros de ponto

```
https://api.pontomais.com.br/external_api/v1/reports/time_cards
```

Rota para extração do relatório de registros de ponto (batidas de entrada/saída dos colaboradores) — **inclui a geolocalização de cada batida**. É este o endpoint que retorna a "posição global" do colaborador no momento do registro de ponto.

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| start_date | string | Sim | Data inicial do período |
| end_date | string | Sim | Data final do período |
| group_by | string | Sim | Tipo do agrupamento: `employee` (por colaborador) ou `team` (por equipe) |
| row_filters | string | Não | Filtros adicionais (ver abaixo); para múltiplos, separar por `,` |
| columns | string | Sim | Colunas desejadas (ver abaixo); para múltiplas, separar por `,` |
| format | string | Sim | Formato do relatório: `json` ou `csv` |
| business_unit_id | number | Não | Filtra pelo ID da Unidade de negócio |
| team_id | number | Não | Filtra pelo ID da equipe |
| employee_id | number | Não | Filtra pelo ID do colaborador |
| cost_center_id | number | Não | Filtra pelo ID do centro de custo |
| location_reference_id | number | Não | Filtra pelo ID do Ponto de referência |
| filter_by_documents | array | Não | Filtra os resultados com base no CPF ou na Matrícula informados |

**Agrupamentos disponíveis (`group_by`)**

| Nome | Descrição |
|---|---|
| employee | Agrupamento por colaborador |
| team | Agrupamento por equipe |

**Filtros adicionais disponíveis (`row_filters`)**

| Nome | Descrição |
|---|---|
| with_inactives | Inclui colaboradores inativos |
| has_time_cards | Inclui colaboradores que não registram ponto |

**Colunas disponíveis (`columns`)** — inclui os dados de localização usados para saber onde o colaborador estava ao bater o ponto:

| Nome | Obrigatório | Descrição |
|---|---|---|
| employee_name | Sim | Nome |
| pis | Não | PIS |
| registration_number | Não | Matrícula |
| job_title_name | Não | Cargo |
| team_name | Não | Equipe |
| shift_name | Não | Turno |
| date | Sim | Data |
| time | Sim | Hora |
| source | Não | Método (como a batida foi feita) |
| original_address | Não | Endereço aprox. detectado |
| edited_address | Não | Endereço aprox. editado |
| manually_changed | Não | Se o registro foi ajustado manualmente |
| motive | Não | Motivo do ajuste |
| updated_by | Não | Quem ajustou |
| image | Não | Fotografia (quando capturada na batida) |
| ip | Não | IP de origem da batida |
| time_card_index | Não | Tipo do registro (ex: "1ª Entrada", "1ª Saída") |
| software_method | Não | Origem (app, web, ajuste manual etc.) |
| local_date_time | Não | Horário local do dispositivo no momento da batida |
| **accuracy** | Não | **Precisão da geolocalização, em metros** |
| **geolocation** | Não | **Geolocalização da batida (latitude/longitude)** |
| **original_geolocation** | Não | **Geolocalização original (antes de qualquer edição/ajuste)** |
| time_clock_sequence_number | Não | NSR |
| untreated_id | Não | Número do recibo |
| device_uuid | Não | UUID (identificador único) do dispositivo |
| device_platform | Não | Plataforma do dispositivo registrado |
| device_description | Não | Descrição do dispositivo |
| tag_manager | Não | Etiqueta de Ponto |
| time_clock_description | Não | Relógio de ponto de origem |

> **Nota importante sobre geolocalização:** os campos `geolocation` / `original_geolocation` só vêm preenchidos quando a batida foi feita por um método que captura GPS (ex: app mobile com localização habilitada — ver `geolocation_enabled` / `enable_geolocation` no colaborador, pasta Colaboradores). Batidas feitas por ajuste manual (`source`/`software_method` = "Ajuste de ponto") ou por métodos sem GPS retornam `geolocation: null`, `accuracy: null` e `local_date_time: "Sem localização"` — confirmado no próprio exemplo de resposta oficial da documentação (abaixo). O formato exato da string/objeto de `geolocation` quando preenchido não é exemplificado na documentação pública — validar com uma chamada real usando um colaborador com `geolocation_enabled: true` que bateu ponto pelo app.

**HEADERS**

| Nome | Valor | Observação |
|---|---|---|
| access-token | `TOKEN_API_EXTERNA` | Token do cliente — mesmo token público de sempre |
| Content-Type | application/json | — |

**Example Request**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/reports/time_cards' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
  "report": {
    "start_date": "2018-09-04",
    "end_date": "2018-09-05",
    "group_by": "team",
    "row_filters": "",
    "columns": "employee_name,pis,registration_number,job_title_name,team_name,shift_name,date,time,source,original_address,edited_address,manually_changed,motive,updated_by,image,ip,time_card_index,software_method,local_date_time,accuracy,geolocation,original_geolocation",
    "format": "json"
  }
}'
```

**Example Response — 200 OK** (exemplo oficial da documentação; batida ajustada manualmente, por isso `geolocation` aparece `null`)

```json
{
  "heading": {
    "title": "Registros de ponto",
    "created_by_name": "Alex Lam",
    "start_date": "04/09/2018",
    "end_date": "05/09/2018",
    "today": "21/11/2018"
  },
  "data": [
    {
      "employee_name": "Darth vader",
      "date": "Ter, 04/09/2018",
      "time": "08:00",
      "pis": "074.42618.31-7",
      "registration_number": "0001",
      "job_title_name": "Gerente geral",
      "team_name": "Administração",
      "shift_name": "turno cíclico",
      "source": "Ajuste de ponto",
      "original_address": null,
      "edited_address": null,
      "manually_changed": "Sim",
      "motive": "Ajuste",
      "updated_by": "Alex Lam",
      "image": null,
      "ip": null,
      "time_card_index": "1ª Entrada",
      "software_method": "Inserido por ajuste de ponto",
      "local_date_time": "Sem localização",
      "accuracy": null,
      "geolocation": null,
      "original_geolocation": null
    }
  ]
}
```

> **[PENDENTE]** Demais 26 relatórios da pasta Relatórios, e as pastas: Afastamentos, Preferências (Configurações de Controle de Ponto), Preferências (Configurações de férias), Exportação Folha, Exceções de jornada, Abonos, Webhooks, Banco cascata.
| main_interval_after | Boolean | Não — true se o intervalo principal ocorre imediatamente após esse período |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**Body (raw json)**

```json
{
  "shift": {
    "code": "0456",
    "shift_type": 4,
    "name": "5d/1d",
    "days": [
      { "cyclic_day": 1, "day_change_time": "23:59", "extra_time_50_percent": "02:00", "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": true },
        { "enter_time": "14:00", "leave_time": "18:00", "main_interval_after": false }
      ]},
      { "cyclic_day": 2, "day_change_time": "23:59", "extra_time_50_percent": "02:00", "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": true },
        { "enter_time": "14:00", "leave_time": "18:00", "main_interval_after": false }
      ]},
      { "cyclic_day": 3, "day_change_time": "23:59", "extra_time_50_percent": "02:00", "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": true },
        { "enter_time": "14:00", "leave_time": "18:00", "main_interval_after": false }
      ]},
      { "cyclic_day": 4, "day_change_time": "23:59", "extra_time_50_percent": "02:00", "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": true },
        { "enter_time": "14:00", "leave_time": "18:00", "main_interval_after": false }
      ]},
      { "cyclic_day": 5, "day_change_time": "23:59", "extra_time_50_percent": "02:00", "periods": [
        { "enter_time": "08:00", "leave_time": "12:00", "main_interval_after": true },
        { "enter_time": "14:00", "leave_time": "18:00", "main_interval_after": false }
      ]},
      { "cyclic_day": 6, "extra_time_50_percent": "2:00" }
    ]
  }
}
```

**Example Request (Exemplo sucesso)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v2/shifts' \
--header 'access-token: {{client_token}}' \
--data '{
"shift": {
"code": "0456",
"shift_type": 4,
"name": "5d/1d",
"days": [
{"cyclic_day": 1,"day_change_time": "23:59","extra_time_50_percent": "02:00","periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": true},{"enter_time": "14:00","leave_time": "18:00","main_interval_after": false}]},
{"cyclic_day": 2,"day_change_time": "23:59","extra_time_50_percent": "02:00","periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": true},{"enter_time": "14:00","leave_time": "18:00","main_interval_after": false}]},
{"cyclic_day": 3,"day_change_time": "23:59","extra_time_50_percent": "02:00","periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": true},{"enter_time": "14:00","leave_time": "18:00","main_interval_after": false}]},
{"cyclic_day": 4,"day_change_time": "23:59","extra_time_50_percent": "02:00","periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": true},{"enter_time": "14:00","leave_time": "18:00","main_interval_after": false}]},
{"cyclic_day": 5,"day_change_time": "23:59","extra_time_50_percent": "02:00","periods": [{"enter_time": "08:00","leave_time": "12:00","main_interval_after": true},{"enter_time": "14:00","leave_time": "18:00","main_interval_after": false}]},
{"cyclic_day": 6,"extra_time_50_percent": "2:00"}
]
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": "Turno cadastrado.",
  "id": 249,
  "meta": { "now": 1753282250, "ip": "172.16.57.1", "obfuscated": false }
}
```

### GET Listar

```
https://api.pontomais.com.br/external_api/v1/shifts?attributes=id,code,name,shift_type,advanced,flexible,flexible_interval,auto_interval,without_holidays,holiday&count=true&page={{page_number}}&per_page=10
```

Lista os turnos.

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| code | String (60) | Código identificador do turno |
| name | String (60) | Nome do turno |
| enabled | Boolean | Ativo? (true - sim / false - Indisponíveis) |
| shift_type | Integer | Tipo de turno (veja a tabela Tipos de turno abaixo) |
| without_holidays | Boolean | Ignora feriados? (true - sim) |
| flexible | Boolean | Jornada flexível? (true - sim) |
| flexible_interval | Boolean | Intervalo flexível? (true - sim) |
| auto_interval | Boolean | Intervalo pré-assinalado? (true - sim) |
| ignore_absences_in_cyclical_shift | Boolean | Ignorar afastamento em turno cíclico? (true - sim) |

**Tipos de turno**

| Código | Nome |
|---|---|
| 1 | Semanal |
| 2 | 12h/36h |
| 3 | 24h/72h |
| 4 | 5d/1d |
| 5 | Customizado |
| 6 | Intermitente |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,code,name,shift_type,advanced,flexible,flexible_interval,auto_interval,without_holidays,holiday | Atributos (ver disponíveis acima) |
| count | true | Se "true" retorna a quantidade de registros encontrados |
| page | {{page_number}} | Número da página. Ex: 1 |
| per_page | 10 | Número de itens por página. Ex: 10 |

**Example Request (Exemplo bem sucedido de listagem)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/shifts?attributes=id%2Ccode%2Cname%2Cshift_type%2Cadvanced%2Cflexible%2Cflexible_interval%2Cauto_interval%2Cwithout_holidays%2Choliday&count=true&page={{page_number}}&per_page=10' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "shifts": [
    { "id": 19631, "code": "219", "name": "Noturno", "shift_type": 1, "advanced": false, "flexible": false, "flexible_interval": false, "auto_interval": false, "without_holidays": false, "holiday": null },
    { "id": 25436, "code": "01", "name": "Turno 08:30h às 12:00h / 13:30h às 18:00h", "shift_type": 1, "advanced": false, "flexible": false, "flexible_interval": false, "auto_interval": false, "without_holidays": false, "holiday": null },
    { "id": 26790, "code": "03", "name": "Turno 08:30h às 11:30h / 12:30h às 17:30h", "shift_type": 1, "advanced": false, "flexible": false, "flexible_interval": false, "auto_interval": false, "without_holidays": false, "holiday": null },
    { "id": 26791, "code": "04", "name": "Turno DEV - Flexível", "shift_type": 1, "advanced": false, "flexible": true, "flexible_interval": true, "auto_interval": false, "without_holidays": false, "holiday": null },
    { "id": 31531, "code": "37", "name": "Turno alternativo", "shift_type": 1, "advanced": false, "flexible": false, "flexible_interval": false, "auto_interval": false, "without_holidays": false, "holiday": null }
  ],
  "meta": { "now": 1531851311, "ip": "127.0.0.1", "count": 6 }
}
```

### GET Detalhes

```
https://api.pontomais.com.br/external_api/v1/shifts/{{shift_id}}
```

Exibe os dias do ciclo, usado quando o turno é 12h/36h, 24h/72h, 5d/1d.

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**Example Request (Exemplo bem sucedido)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/shifts/{{shift_id}}' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "shift": {
    "id": 207,
    "created_at": 1715862139,
    "updated_at": 1715862139,
    "code": "0008",
    "name": "12/36",
    "active": true,
    "code_name": "0008 - 12/36",
    "days": [
      { "id": 1084, "day_change_time": "23:59:00", "extra_time_50_percent": "02:00:00", "is_holiday": false, "special_day": null, "duration": 24, "cyclic_day": 1, "periods": [
        { "id": 1600, "enter_time": "08:00:00", "leave_time": "12:00:00", "main_interval_after": false },
        { "id": 1601, "enter_time": "14:00:00", "leave_time": "18:00:00", "main_interval_after": false }
      ]},
      { "id": 1085, "day_change_time": "23:59:00", "extra_time_50_percent": "02:00:00", "is_holiday": false, "special_day": null, "duration": 24, "cyclic_day": 2, "periods": [] }
    ],
    "holiday": null,
    "shift_type": 2,
    "without_holidays": false,
    "standbys": false,
    "advanced": false,
    "advanced_preference": null,
    "flexible": false,
    "flexible_allowance": false,
    "flexible_interval": false,
    "ignore_absences_in_cyclical_shift": false,
    "custom_interval_type": 1,
    "custom_interval_extra_time_enabled": true,
    "default_dsr": null,
    "auto_interval": true,
    "apply_auto_interval_in_day_off": false,
    "apply_auto_interval_in_all_intervals": false,
    "apply_auto_interval_different_time_cards": false,
    "auto_interval_in_day_off": null,
    "apply_auto_interval_in_day_with_periods": false,
    "workload_in_day_off": null,
    "auto_interval_in_day_with_periods": null,
    "workload_in_day_with_periods": null,
    "cumulative_extra_time": false,
    "cumulative_preference": null,
    "apply_holiday_on_days_off": false,
    "count_only_extra_time_on_holidays": false,
    "limit_type": 1,
    "limit_amount": null,
    "limit_range": null,
    "main_parent_id": 52,
    "nr17": false,
    "enabled": true,
    "missing_time_on_holiday": null,
    "work_schedule": false,
    "auto_assign_time_cards": false,
    "multiple_day": false
  },
  "meta": { "now": 1745435826, "ip": "172.16.57.1", "obfuscated": false }
}
```

### POST Criar Turno

```
https://api.pontomais.com.br/external_api/v1/shifts
```

Cadastra um turno (rota V1, mais simples que a V2).

**Atributos disponíveis**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| code | String (60) | Sim (Não pode se repetir) | Código identificador do turno |
| name | String (60) | Sim | Nome do turno |
| shift_type | Integer | Sim | Tipo de turno (veja a tabela Tipos de turno abaixo) |
| week_days | Array of integer | Sim | Para shift_type 1 não informar domingo; shift_type 2 e 3 deve ser informado [1]; shift_type = 4 deve ser informado = [1,2,3,4,5]. Dias da Semana (veja tabela abaixo) |
| hours_per_day | Integer | Sim | Quantidade de horas de trabalho diário |
| weekly_hours | Integer | Sim (> 0 se shift_type = 1) | Quantidade de horas de trabalho Semanal |
| interval_start_time | String | Sim | Horário do Início do Intervalo formato HH:MM |
| interval_end_time | String | Sim | Horário do Final do Intervalo formato HH:MM |

**Tipos de turno**

| Código | Nome |
|---|---|
| 1 | Semanal |
| 2 | 12h/36h |
| 3 | 24h/72h |
| 4 | 5d/1d |

**Dias da Semana**

| Código | Dia da Semana |
|---|---|
| 1 | Domingo |
| 2 | Segunda-Feira |
| 3 | Terça-Feira |
| 4 | Quarta-Feira |
| 5 | Quinta-Feira |
| 6 | Sexta-Feira |
| 7 | Sábado |

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**Body (raw json)**

```json
{
  "shift": {
    "code": "021",
    "name": "Turno teste semanal",
    "shift_type": 1,
    "week_days": [2,3,4,5,6],
    "hours_per_day": 8,
    "weekly_hours": 40,
    "interval_start_time": "12:00",
    "interval_end_time": "13:00"
  }
}
```

**Example Request (Exemplo bem sucedido)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/shifts' \
--header 'access-token: {{client_token}}' \
--data '{
"shift": {
"code": "0001",
"name": "Turno 40h semanais",
"shift_type": 1,
"week_days": [2,3,4,5,6,7],
"hours_per_day":8,
"weekly_hours": 40,
"interval_start_time": "12:00",
"interval_end_time": "13:00"
}
}'
```

**Example Response — 201 CREATED**

```json
{
  "success": "Turno cadastrado com sucesso!",
  "meta": { "now": 1680117336, "ip": "172.16.57.1", "obfuscated": false },
  "id": 62
}
```

### GET Listar dias

```
https://api.pontomais.com.br/external_api/v1/shifts/{{shift_id}}/days?
```

Exibe os dias do ciclo, usado quando o turno é 12h/36h, 24h/72h, 5d/1d.

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**PARAMS**

| Nome | Valor |
|---|---|
| attributes | id,code,name,shift_type,advanced,flexible,flexible_interval,auto_interval,without_holidays,holiday |

**Example Request (Exemplo de listagem de dias sem sucesso)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/shifts/{{shift_id}}/days' \
--header 'access-token: {{client_token}}'
```

**Example Response — 404 NOT FOUND**

```json
{
  "error": "Registro não encontrado",
  "meta": { "now": 1581622508, "ip": "187.32.131.210" }
}
```

### DELETE Excluir

```
https://api.pontomais.com.br/external_api/v1/shifts/{{shift_id}}
```

> Nota: a descrição exibida na documentação original para este endpoint está incorreta/copiada de "Listar dias" ("Exibe os dias do ciclo, usado quando o turno é 12h/36h, 24h/72h, 5d/1d."). Pelo verbo HTTP (DELETE) e pela mensagem de sucesso ("Turno removido."), o endpoint exclui (inativa) um turno.

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**Example Request (Exemplo de sucesso)**

```bash
curl --location -g --request DELETE 'https://api.pontomais.com.br/external_api/v1/shifts/{{shift_id}}' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "success": "Turno removido.",
  "meta": { "now": 1745523219, "ip": "172.16.57.1", "obfuscated": false }
}
```

### PUT Desfazer exclusão

```
https://api.pontomais.com.br/external_api/v1/shifts/{{shift_id}}/recover
```

> Nota: a descrição exibida na documentação original para este endpoint também está copiada de "Listar dias" ("Exibe os dias do ciclo, usado quando o turno é 12h/36h, 24h/72h, 5d/1d."). Pela mensagem de sucesso ("Turno restaurado."), o endpoint desfaz a exclusão (restaura) um turno previamente excluído.

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{client_token}} |

**Example Request (Exemplo de sucesso)**

```bash
curl --location -g --request PUT 'https://api.pontomais.com.br/external_api/v1/shifts/{{shift_id}}/recover' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "success": "Turno restaurado.",
  "meta": { "now": 1745523241, "ip": "172.16.57.1", "obfuscated": false }
}
```

---

## Usuários

### Grupos de Acesso

#### GET Listar

```
https://api.pontomais.com.br/external_api/v1/users/groups?attributes=id,name
```

Lista os grupos de acesso.

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome do grupo |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,name | Atributos (ver disponíveis acima) |

**Example Request (Exemplo de sucesso ao listar)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/users/groups?attributes=id%2Cname' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "groups": [
    { "id": 9, "name": "Diretor" },
    { "id": 7, "name": "Operação" },
    { "id": 305, "name": "Gestores" }
  ],
  "meta": { "now": 1531855020, "ip": "127.0.0.1" }
}
```

### Notificações

#### GET Listar

```
https://api.pontomais.com.br/external_api/v1/notifications?count=true&page={{page_number}}&per_page=10
```

Lista as notificações.

**Objeto de retorno**

| Nome | Tipo | Descrição |
|---|---|---|
| title | String (60) | Título da Notificação |
| message | String | Mensagem da Notificação |
| visualized | Boolean | Visualizado |
| notification_type | Object | Objeto do tipo da notificação |
| work_day | Object | Objeto do dia de trabalho |
| exemption | Object | Objeto da Solicitação de Abono |
| proposal | Object | Objeto da Solicitação de Ajuste |
| employee | Object | Objeto do Colaborador |

**Formato do objeto `notification_type`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome do Tipo da Notificação |

**Formato do objeto `work_day`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| status | Object | Status do dia de trabalho |
| date | Date | Data do dia de trabalho |

**Formato do objeto `exemption`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| status | Object | Status do dia de trabalho |
| date | Date | Data do dia de trabalho |
| exemption_type | Object | Tipo do Abono |
| employee | Object | Objeto do Colaborador |
| answered_by | Object | Objeto do Gestor que respondeu a solicitação |

**Formato do objeto `exemption_type`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome do Tipo do Abono |

**Formato do objeto `solicitation_status`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome do Status da Solicitação |

**Formato do objeto `proposal`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| status | Object | Status do dia de trabalho |
| date | Date | Data do dia de trabalho |
| employee | Object | Objeto do Colaborador |
| answered_by | Object | Objeto do Gestor que respondeu a solicitação |

**Formato do objeto `employee`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome do Colaborador |
| picture | Object | Objeto da foto |

**Formato do objeto `answered_by`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome do Gestor |
| picture | Object | Objeto da foto |

**Formato do objeto `picture`**

| Nome | Tipo | Descrição |
|---|---|---|
| url | String | Url da foto |
| medium_url | String | Url da foto redimensionada para tamanho médio |
| small_url | String | Url da foto redimensionada para tamanho pequeno |

**Formato do objeto "tipo do status"**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| observation | String (60) | Observação do status |
| active | Boolean | Ativo ou desativado para novas inserções |
| status_type | Object | Tipo do Status |

**Formato do objeto `status_type`**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| name | String (60) | Nome do Tipo do Status |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| count | true | Se "true" retorna a quantidade de registros encontrados |
| page | {{page_number}} | Número da página. Ex: 1 |
| per_page | 10 | Número de itens por página. Ex: 10 |

**Example Response — 200 OK** (exemplo parcial, com múltiplas notificações de tipos diferentes)

```json
{
  "notifications": [
    {
      "id": "5f3ae16672864f06a9f027f5",
      "created_at": 1597694477,
      "updated_at": 1597694477,
      "title": "Teste 1",
      "message": "Teste de Notificação 1",
      "visualized": false,
      "notification_type": { "id": 1, "name": "Ponto" },
      "employee": {
        "id": 1,
        "name": "Darth Vader",
        "picture": {
          "url": "//s3.amazonaws.com/picture_path_default.jpg?...",
          "medium_url": "//s3.amazonaws.com/picture_path_medium.jpg?...",
          "small_url": "//s3.amazonaws.com/picture_path_small.jpg?..."
        },
        "accessible": true
      },
      "work_day": { "id": 1299, "status": { "id": 2, "name": "Falta" }, "date": "14/08/2020" },
      "exemption": {
        "id": 22,
        "date": "2020-08-16",
        "status": { "id": 3, "observation": "Atestado", "active": true, "status_type": { "id": 3, "name": "Abono" } },
        "solicitation_status": null,
        "exemption_type": { "id": 5, "name": "Atestado Médico" },
        "answered_by": { "id": 1, "name": "Darth Vader", "picture": { "url": "...", "medium_url": "...", "small_url": "..." }, "accessible": true }
      }
    },
    {
      "id": "5f3ae15f72864f06a9f027f4",
      "created_at": 1597694475,
      "updated_at": 1597694475,
      "title": "Teste 2",
      "message": "Teste de Notificação 2",
      "visualized": false,
      "notification_type": { "id": 1, "name": "Ponto" },
      "employee": { "id": 1, "name": "Darth Vader", "picture": { "url": "...", "medium_url": "...", "small_url": "..." } }
    },
    {
      "id": "5f3ae15472864f06a9f027f3",
      "created_at": 1597694472,
      "updated_at": 1597694472,
      "title": "Teste 3",
      "message": "Teste de Notificação 3",
      "visualized": false,
      "notification_type": { "id": 1, "name": "Ponto" },
      "employee": { "id": 1, "name": "Darth Vader", "picture": { "url": "...", "medium_url": "...", "small_url": "..." }, "accessible": true },
      "proposal": {
        "id": 128,
        "date": "2020-08-06",
        "status": { "id": 6, "observation": "Ajuste", "active": true, "status_type": { "id": 5, "name": "Ajuste de horário" } },
        "employee": { "id": 1, "name": "Darth Vader", "picture": { "url": "...", "medium_url": "...", "small_url": "..." } }
      }
    }
  ],
  "meta": { "now": 1597694500, "ip": "127.0.0.1" }
}
```

> Nota: o exemplo de `curl` mostrado na documentação original para este endpoint contém um erro de copy-paste (a URL exibida aponta para `/external_api/v1/teams` em vez de `/external_api/v1/notifications`); a URL correta do endpoint é a mostrada acima.

### GET Listar

```
https://api.pontomais.com.br/external_api/v1/users?attributes=id,group,employee&count=true&page={{page_number}}&per_page=10
```

Lista os usuários.

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**Example Request**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/users?attributes=id%2Cgroup%2Cemployee' \
--header 'access-token: {{client_token}}'
```

**Example Response — 200 OK**

```json
{
  "users": [
    { "id": 66, "group": { "id": 9, "name": "Diretor" }, "employee": { "id": 19, "name": "Luke Skywalker" } },
    { "id": 67, "group": { "id": 7, "name": "Colaboradores" }, "employee": { "id": 21, "name": "Stormtrooper" } }
  ],
  "meta": { "now": 1531855287, "ip": "127.0.0.1" }
}
```

### GET Detalhar

```
https://api.pontomais.com.br/external_api/v1/users/{{user_id}}?attributes=id,employee,group
```

Exibe os atributos de um usuário.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| user_id | Integer | Sim | ID do usuário |

**Atributos disponíveis**

| Nome | Tipo | Descrição |
|---|---|---|
| id | Integer | Identificador sequencial gerado automaticamente pelo sistema |
| employee | Object | Colaborador ao qual o usuário pertence |
| group | Object | Grupo de acesso do usuário |
| last_sign_in_at | Timestamp | Data do último acesso |
| last_sign_in_ip | String | IP do último acesso |
| confirmed_at | String | Data de confirmação do usuário |
| active | String | Ativo? (true - sim / false - não) |
| admin | String | É administrador? (true - sim / false - não) |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| access-token | {{client_token}} | Token do cliente |

**PARAMS**

| Nome | Valor | Descrição |
|---|---|---|
| attributes | id,employee,group | Atributos (ver disponíveis acima) |

**Example Request (Exemplo de sucesso ao detalhar)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/users/{{user_id}}?attributes=id%2Cemployee%2Cgroup' \
--header 'access-token: {{client_token}}'
```

### POST Criar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/user
```

Cria um usuário para o colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | id do colaborador a ser criado o usuário |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| send_confirmation_email | Boolean | Sim | Envia email de confirmação para colaborador? (true - sim \| false - não) |
| group_id | Integer | Sim | ID do grupo de acesso do qual o usuário fará parte. Verificar grupos em "Grupos de Acesso" |
| password | String | Sim | Senha |
| password_confirmation | String | Sim | Confirmação da senha |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Body (raw)**

```json
{
  "user": {
    "send_confirmation_email": false,
    "group_id": 2,
    "password": "23123123",
    "password_confirmation": "23123123"
  }
}
```

**Example Request (Exemplo com colaborador sem CPF cadastrado)**

```bash
curl --location -g 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/user?attributes=id%2Cgroup%2Cemployee' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"user":{
"send_confirmation_email": false,
"group_id": 2,
"password": "23123123",
"password_confirmation": "23123123"
}
}'
```

### PUT Editar

```
https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/user
```

Edita o usuário de um colaborador.

**Variáveis na URL**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| employee_id | Integer | Sim | id do colaborador |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| active | Boolean | Não | Acesso liberado (true = sim, false = não) |
| send_confirmation_email | Boolean | Não | Envia email de confirmação para colaborador? (true = sim, false = não) |
| group_id | Integer | Não | ID do grupo de acesso na qual o usuário fará parte |
| password | String | Não | Senha |
| password_confirmation | String | Não | Confirmação da senha |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Body (raw)**

```json
{
  "user": {
    "active": true,
    "send_confirmation_email": false,
    "group_id": 1,
    "password": "123123123",
    "password_confirmation": "123123123"
  }
}
```

**Example Request (Editar)**

```bash
curl --location -g --request PUT 'https://api.pontomais.com.br/external_api/v1/employees/{{employee_id}}/user' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"user":{
"active": true,
"send_confirmation_email": false,
"group_id": 1,
"password": "123123123",
"password_confirmation": "123123123"
}
}'
```

**Example Response**

Este endpoint não retorna corpo de resposta ("No response body" / "This request doesn't return any response body").

---

## AFD

### POST Exportar

```
https://api.pontomais.com.br/external_api/v1/afd/export
```

Gera o arquivo AFD por período.

> OBS: Só serão incluídas no arquivo as marcações que foram batidas diretamente pela Pontomais, as batidas realizadas pelo relógio devem ser retiradas do AFD do mesmo.

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| start_date | String | Sim | Data inicial (AAAA-MM-DD ou DD/MM/AAAA) |
| end_date | String | Sim | Data final (AAAA-MM-DD ou DD/MM/AAAA) |
| business_unit_id | Integer | Ao menos um dos parâmetros de filtro (business_unit_id, department_id, team_id) deve ser informado. | ID da unidade de negócio |
| department_id | Integer | Ao menos um dos parâmetros de filtro (business_unit_id, department_id, team_id) deve ser informado. | ID do departamento |
| team_id | Integer | Ao menos um dos parâmetros de filtro (business_unit_id, department_id, team_id) deve ser informado. | ID da equipe |
| local_date_time | Boolean | Não | Se true exporta as batidas no fuso horário local de onde foram realizadas; se false, não aplica fuso |
| employee_change | Boolean | Sim | Se true exportará as movimentações dos colaboradores |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Body (raw)**

```json
{
  "afd_mpt671": {
    "start_date": "2025-01-01",
    "end_date": "2025-02-02",
    "business_unit_id": 123456,
    "local_date_time": true,
    "employee_change": false
  }
}
```

**Example Request**

```bash
curl --location --request POST 'https://api.pontomais.com.br/external_api/v1/afd/export' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"afd_mpt671":{
"start_date": "2025-01-01",
"end_date": "2025-02-02",
"business_unit_id": 123456,
"local_date_time": true,
"employee_change": false
}
}'
```

**Example Response**

Este endpoint não retorna corpo de resposta ("No response body" / "This request doesn't return any response body") — provavelmente retorna o arquivo AFD diretamente (download).

> Nota: o corpo do exemplo (`Body raw`) usa a chave raiz `afd_mpt671`, mesmo padrão observado depois nas pastas AFD-671 e AFDT — sugere reaproveitamento do mesmo exemplo de payload entre as três seções.

---

## AFD-671

### POST Exportar

```
https://api.pontomais.com.br/external_api/v1/afd_mpt_671/export
```

Gera o arquivo AFD (padrão MTP 671) por período.

> OBS: Só serão incluídas no arquivo as marcações que foram batidas diretamente pela Pontomais, as batidas realizadas pelo relógio devem ser retiradas do AFD do mesmo.

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| start_date | String | Sim | Data inicial (AAAA-MM-DD ou DD/MM/AAAA) |
| end_date | String | Sim | Data final (AAAA-MM-DD ou DD/MM/AAAA) |
| business_unit_id | Integer | Ao menos um dos parâmetros de filtro (business_unit_id, department_id, team_id) deve ser informado. | ID da unidade de negócio |
| local_date_time | Boolean | Não | Se true exporta as batidas no fuso horário local de onde foram realizadas; se false, não aplica fuso |
| employee_change | Boolean | Sim | Se true exportará as movimentações dos colaboradores |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Body (raw)**

```json
{
  "afd_mpt671": {
    "start_date": "2025-01-01",
    "end_date": "2020-01-02",
    "business_unit_id": {{business_unit_id}}
  }
}
```

**Example Response**

Este endpoint não retorna corpo de resposta ("No response body" / "This request doesn't return any response body") — provavelmente retorna o arquivo AFD diretamente (download).

> Nota: a URL raiz deste endpoint (`afd_mpt_671`) difere ligeiramente da chave usada no corpo JSON (`afd_mpt671`, sem o segundo underscore) — isso é o que está documentado na página original, mantido fielmente aqui.

---

## AFDT

### POST Exportar

```
https://api.pontomais.com.br/external_api/v1/afdt/export
```

Gera o arquivo AFDT por período.

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| start_date | String | Sim | Data inicial (AAAA-MM-DD ou DD/MM/AAAA) |
| end_date | String | Sim | Data final (AAAA-MM-DD ou DD/MM/AAAA) |
| business_unit_id | Integer | Sim | ID da unidade de negócio |

**HEADERS**

| Header | Valor |
|---|---|
| Content-Type | application/json |
| access-token | {{client_token}} |

**Body (raw)**

```json
{
  "afd_export": {
    "start_date": "2020-01-01",
    "end_date": "2020-01-02",
    "business_unit_id": {{business_unit_id}}
  }
}
```

**Example Request (Exportar)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/afdt/export' \
--header 'Content-Type: application/json' \
--header 'access-token: {{client_token}}' \
--data '{
"afd_export":{
"start_date": "2020-01-01",
"end_date": "2020-01-02",
"business_unit_id": {{business_unit_id}}
}
}'
```

**Example Response**

Este endpoint não retorna corpo de resposta ("No response body" / "This request doesn't return any response body") — provavelmente retorna o arquivo AFDT diretamente (download).

---

## AEJ

Exportação de arquivo AEJ.

**Estrutura do objeto JSON a ser recebido**

| Nome | Tipo | Descrição | Obrigatório |
|---|---|---|---|
| start_date | Date | Data inicial para geração do arquivo | Sim |
| end_date | Date | Data final para geração do arquivo | Sim |
| business_unit_cnpj_cpf | Array | Array de CNPJ/CPF das unidades de negócios que deseja exportar os arquivos AEJ | Sim |

### POST AEJ Export

```
{{base_url}}/external_api/v1/aej/export
```

**HEADERS**

| Header | Valor |
|---|---|
| access-token | {{external_token}} |

**Body (raw json)**

```json
{
  "aej_export": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "business_unit_cnpj_cpf": [
      "00.005.152/0001-87",
      "99.990.040/0000-04"
    ]
  }
}
```

**Example Request (invalid)**

```bash
curl --location -g '{{base_url}}/external_api/v1/aej/export' \
--header 'access-token: {{external_token}}' \
--data '{
"aej_export": {
"start_date": "2024-01-01",
"end_date": "",
"business_unit_cnpj_cpf": ["00.005.152/0001-87"]
}
}'
```

**Example Response — 422 UNPROCESSABLE ENTITY**

```json
{
  "error": {
    "end_date": [
      "Não pode ficar em branco",
      "não é uma data válida"
    ]
  },
  "meta": { "now": 1710509039, "ip": "172.16.57.1", "obfuscated": false }
}
```

> Nota: diferente dos demais endpoints de exportação (AFD, AFD-671, AFDT), este usa `{{base_url}}` em vez de `https://api.pontomais.com.br` fixo na URL, e o header `access-token` usa a variável `{{external_token}}` em vez de `{{client_token}}`. O exemplo de request documentado é um caso de erro (422), não de sucesso — mantido fielmente como está na fonte.

---

## Relatórios

> A pasta **Relatórios** contém 27 tipos de relatório (Jornada, Fechamento, Modelo AFD Portaria 1510, Abonos, Absenteísmo, Afastamentos e férias, Ajustes de ponto, Assinaturas, Atrasos, Auditoria, Banco de horas, Benefícios, Colaboradores, Equipes, Faltas, Horas Extras, Horista, Ocorrências, Pendências, Provisionamento, Registros de ponto, Registros de pausas, Resumo de jornada, Sobreaviso, Solicitações, Turnos, Vigência de Banco de Horas). Todos seguem o mesmo padrão estrutural de requisição (POST para `https://api.pontomais.com.br/external_api/v1/reports/<recurso>`, headers `Content-Type` + `access-token`, body `{"report": {...}}` com `start_date`, `end_date`, `group_by`, `row_filters`, `columns`, `format`, filtros de `business_unit_id`/`team_id`/`employee_id`/`cost_center_id`/`status_id`, paginação `page`/`per_page`), diferindo em: URL exata, atributo obrigatório `group_by` (agrupamentos disponíveis), lista de `columns` disponíveis, e `row_filters`/filtros adicionais específicos de cada relatório. Dado o volume (cada relatório tem tabelas extensas de "Colunas disponíveis", algumas com dezenas de linhas truncadas por "View More" na página), o relatório **Jornada** foi documentado abaixo com nível de detalhe completo como referência do padrão; os demais 26 relatórios ainda precisam ser capturados individualmente (ver seção PENDENTE).

### POST Jornada

```
https://api.pontomais.com.br/external_api/v1/reports/work_days
```

Rota para extração do relatório de jornada.

**Variáveis na URL**

| Nome | Descrição |
|---|---|
| csv_token | Token do cliente |

**Estrutura do objeto JSON a ser enviado**

| Nome | Tipo | Descrição | Obrigatório |
|---|---|---|---|
| start_date | string | Data inicial do período | Sim |
| end_date | string | Data final do período | Sim |
| group_by | string | Tipo do agrupamento, ver disponíveis abaixo | Sim |
| row_filters | string | Filtros adicionais, ver disponíveis abaixo; para mais de um utilizar ',' como separador | Não |
| columns | string | Colunas, ver disponíveis abaixo; para múltiplas, separar por vírgula | — |
| format | string | Formato do relatório, ver disponíveis abaixo | Sim |
| business_unit_id | number | Filtra pelo ID da Unidade de negócio | Não |
| team_id | number | Filtra pelo ID da equipe | — |
| employee_id | number | Filtra pelo ID do colaborador | — |
| cost_center_id | number | Filtra pelo ID do centro de custo | — |
| status_id | number | Filtra pelo Motivo | — |
| page | number | Define a página a ser carregada | Não |
| per_page | number | Define o total de registros por página (limitado a 500) — ver nota per_page | Não |

**Nota per_page**

Quando informado na 1ª request, no retorno vai trazer o total de páginas no heading, na propriedade `page`, sendo `page/total de página`, com a informação de total de página; pode-se fazer o loop para obter todos os registros.

**Agrupamentos disponíveis**

| Nome | Obrigatório | Descrição |
|---|---|---|
| employee | Sim | Agrupamento por colaborador |

**Colunas disponíveis** (lista parcial — a tabela na fonte continua além do trecho capturado, via "View More")

| Nome | Obrigatório | Descrição |
|---|---|---|
| overnight_time | Não | Adicional noturno |
| job_title_name | Não | Cargo (Nome do cargo) |
| employee_id | Não | ID do colaborador |
| employee_name | Não | Nome do colaborador |
| date | Sim | Data |
| team_name | Não | Nome da equipe |
| time_balance_factors | Não | Fatores acumulativos |
| holiday | Não | Feriado |
| managers_names | Não | Nome dos gestores da equipe |
| reduced_overnight_time | Não | Hora noturna reduzida |
| over_limit | Não | Horas excedentes |
| custom_interval_time | Não | Horas intrajornada |
| shift_time | Não | Horas previstas |
| total_time | Não | Horas totais |
| shift_name | Não | Nome do turno |
| time_breaks | Não | (Intervalos batidos) |
| shift_appointments | Não | (Apontamentos do turno) |
| time_cards | Não | (Marcações de ponto) |
| summary | Não | (Resumo) |
| extra_time | Não | (Horas extras) |
| registration_number | Não | (Matrícula/PIS) |
| time_balance | Não | (Saldo de banco de horas) |
| motive | Não | (Motivo) |

**Filtros adicionais disponíveis**

| Nome | Obrigatório | Descrição |
|---|---|---|
| with_inactives | Não | Inclui colaboradores inativos |
| has_time_cards | Não | Inclui colaboradores que não registram ponto |
| holidays_only | Não | Lista somente jornadas em dias de feriado |

**HEADERS**

| Header | Valor | Descrição |
|---|---|---|
| Content-Type | application/json, text/plain, */* | |
| access-token | TOKEN_API_EXTERNA | Configurações > Extensões contratadas > API e Webhooks |

**Body (raw)**

```json
{
  "report": {
    "start_date": "2026-04-01",
    "end_date": "2026-04-10",
    "group_by": "employee",
    "row_filters": "with_inactives,has_time_cards",
    "columns": "date,shift_name,time_breaks,shift_appointments,time_cards,summary,extra_time,total_time,shift_time,custom_interval_time,overnight_time,registration_number,time_balance,motive,employee_id",
    "format": "json"
  }
}
```

**Example Request (Jornada)**

```bash
curl --location 'https://api.pontomais.com.br/external_api/v1/reports/work_days' \
--header 'Content-Type: application/json, text/plain, */*' \
--header 'access-token: TOKEN_API_EXTERNA' \
--data '{
"report": {
"start_date": "2026-04-01",
"end_date": "2026-04-10",
"group_by": "employee",
"row_filters": "with_inactives,has_time_cards",
"columns": "date,shift_name,time_breaks,shift_appointments,time_cards,summary,extra_time,total_time,shift_time,custom_interval_time,overnight_time,registration_number,time_balance,motive, employee_id",
"format": "json"
}
}'
```

### POST Fechamento (parcial — capturado por amostragem)

```
https://api.pontomais.com.br/external_api/v1/reports/<recurso closing_mirrors>
```

Relatório de fechamento. Identificado pelo `report_id: "closing_mirrors"` no exemplo de corpo capturado:

```json
{
  "report": {
    "report_id": "closing_mirrors",
    "start_date": "2026-03-01",
    "end_date": "2026-04-17",
    "columns": "",
    "row_filters": "with_inactives",
    "additional_row_filters": "",
    "proposal_status": "",
    "format": "html",
    "fabrication_number": "",
    "initial_nsr": "",
    "group_columns": ""
  }
}
```

**HEADERS** (identificados)

| Header | Valor |
|---|---|
| Accept | application/json, text/plain, */* |
| access-token | TOKEN_API_EXTERNA (Configurações > Extensões contratadas > API e Webhooks) |
| uid | (email do usuário autenticado) |
| uuid | (UUID de sessão) |

> Nota: a URL exata, tabela de atributos, agrupamentos, colunas e filtros completos deste endpoint não foram confirmados nesta sessão — apenas o corpo de exemplo foi capturado incidentalmente ao rolar a página. Requer captura dedicada em sessão de continuação.

---

## [PENDENTE] Seções ainda não capturadas

A pasta **Banco de horas**, **Turnos**, **Usuários**, **AFD**, **AFD-671**, **AFDT** e **AEJ** estão COMPLETAS. A pasta **Relatórios** foi INICIADA: "Jornada" está documentado com detalhe completo (nota: a tabela "Colunas disponíveis" pode ter mais linhas além das capturadas, escondidas atrás de "View More" na fonte); "Fechamento" tem apenas um corpo de exemplo capturado parcialmente, sem URL exata nem tabelas de atributos. Faltam capturar integralmente estes 26 relatórios restantes da pasta Relatórios (mesmo padrão de "POST /reports/<recurso>" com corpo `{"report": {...}}`, mas cada um com seus próprios `group_by`, `columns` e filtros específicos):

- Fechamento (confirmar URL e tabelas — só corpo de exemplo foi capturado)
- Modelo AFD Portaria 1510
- Abonos
- Absenteísmo
- Afastamentos e férias
- Ajustes de ponto
- Assinaturas
- Atrasos
- Auditoria
- Banco de horas (relatório — distinto da pasta "Banco de horas" já documentada, que é CRUD de lançamentos)
- Benefícios
- Colaboradores
- Equipes
- Faltas
- Horas Extras
- Horista
- Ocorrências
- Pendências
- Provisionamento
- Registros de ponto
- Registros de pausas
- Resumo de jornada
- Sobreaviso
- Solicitações
- Turnos (relatório — distinto da pasta "Turnos" já documentada, que é CRUD de turnos)
- Vigência de Banco de Horas

Após a pasta Relatórios, restam ainda:

- Afastamentos
- Preferências (Configurações de Controle de Ponto)
- Preferências (Configurações de férias)
- Exportação Folha
- Exceções de jornada
- Abonos
- Webhooks
- Banco cascata

> CONFIRMADO: "Banco cascata" é o ÚLTIMO item do menu lateral — não há mais nenhuma pasta/seção abaixo dele. A lista acima é definitiva e completa.
