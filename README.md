# 🤖 Agente de Análise de Mercado - LangChain + Gemini

Sistema de agente inteligente para análise de mercado usando **Google Gemini** como motor via **LangChain**, com ferramentas de busca web (**SerpAPI**) e cálculo de métricas financeiras (CAGR).

## 📋 Características

- ✅ **Motor LLM**: Google Gemini 1.5 Pro via LangChain
- ✅ **Ferramentas**: 
  - Busca web com SerpAPI
  - Cálculo de CAGR (Compound Annual Growth Rate)
  - Refinamento de relatórios
- ✅ **Rastreabilidade TAO**: Logs de Thought → Action → Observation via callbacks
- ✅ **Arquitetura Modular**: Pronto para expansão multi-domínio (roteador)
- ✅ **Relatórios Estruturados**: 4 parágrafos em PT-BR com citações e fontes

## 🎯 Objetivo Funcional

O agente recebe um tema de mercado (ex.: "Blockchain em Logística") e:

1. **Busca** 2 fontes relevantes (notícias/relatórios) sobre investimentos e crescimento
2. **Calcula** CAGR anualizado com parâmetros fornecidos
3. **Consolida** um relatório em 4 parágrafos em português, citando as fontes com URLs e datas
4. **Exibe** rastro operacional TAO no console para auditoria

## 📁 Estrutura do Projeto

```
langchain-logistica/
├── env.example          # Template de variáveis de ambiente
├── README.md             # Este arquivo
├── requirements.txt      # Dependências Python
├── main.py              # Ponto de entrada
├── router.py            # Roteador multi-domínio
├── callbacks.py         # Callbacks TAO para logs
├── tools.py             # Ferramentas (web_search, calc_cagr, report_refine)
├── agent_market.py      # Agente de análise de mercado
└── tests/
    └── test_calc_cagr.py  # Testes da função CAGR
```

## 🚀 Pré-requisitos

- **Python 3.10+** instalado
- Chaves de API:
  - **GEMINI_API_KEY**: Obtenha em [Google AI Studio](https://makersuite.google.com/app/apikey)
  - **SERPAPI_API_KEY**: Obtenha em [SerpAPI](https://serpapi.com/)

## 📦 Instalação

### 1. Clone ou baixe o projeto

```bash
cd langchain-logistica
```

### 2. Crie um ambiente virtual

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` a partir do template `env.example`:

**Linux/macOS:**
```bash
cp env.example .env
```

**Windows (PowerShell/CMD):**
```powershell
copy env.example .env
```

Edite o arquivo `.env` e adicione suas chaves:

```env
GEMINI_API_KEY=sua_chave_gemini_aqui
SERPAPI_API_KEY=sua_chave_serpapi_aqui
```

## ▶️ Como Executar

### Executar o Agente

```bash
python main.py
```

O sistema irá:
1. Analisar o tema **"Blockchain em Logística"**
2. Buscar 2 fontes relevantes na web
3. Calcular CAGR com start=100, end=120, months=6
4. Gerar relatório consolidado em 4 parágrafos

### Executar Testes

**Opção 1 - Teste simples (sem pytest):**
```bash
python tests/test_calc_cagr.py
```

**Opção 2 - Com pytest (se instalado):**
```bash
pip install pytest
python -m pytest tests/ -v
```

## 📊 Exemplo de Saída

```
🚀 Iniciando Agente de Análise de Mercado

📍 Domínio identificado: logistica

🔍 Analisando: Blockchain em Logística
📊 Parâmetros CAGR: start=100.0, end=120.0, months=6.0

============================================================
=== AGENTE INICIADO ===
============================================================
Input: Você é um analista de mercado especializado...
============================================================

🔧 Action: web_search
📥 Action Input: Blockchain logística investimentos crescimento 2024

👁️  Observation: [{"title": "Blockchain revoluciona...", ...}]

🔧 Action: calc_cagr
📥 Action Input: {"start": 100, "end": 120, "months": 6}

👁️  Observation: 0.44

============================================================
=== FINAL ===
============================================================
>>> RELATÓRIO FINAL:
================================================================================

[Parágrafo 1 - Contexto geral sobre Blockchain em Logística]

[Parágrafo 2 - Primeira fonte com título, link e data]

[Parágrafo 3 - Segunda fonte com título, link e data]

[Parágrafo 4 - Análise de crescimento com CAGR de 44,00%]

================================================================================

✅ Execução concluída com sucesso!
```

## 🔧 Ferramentas Disponíveis

### `web_search(query: str, num: int = 5)`
Busca notícias e relatórios usando SerpAPI.
- **Input**: Consulta de busca
- **Output**: Lista com title, link, snippet, date

### `calc_cagr(start: float, end: float, months: float)`
Calcula CAGR (taxa de crescimento anual composta).
- **Input**: Valores inicial, final e período em meses
- **Output**: CAGR como decimal (ex.: 0.44 = 44%)

### `report_refine(texto: str)`
Limpa e normaliza formatação de textos.

## 🧪 Testes

Os testes cobrem:
- ✅ Cálculo correto de CAGR (100 → 120 em 6 meses ≈ 44%)
- ✅ Validação de parâmetros inválidos (start ≤ 0)
- ✅ Validação de período inválido (months ≤ 0)

## 🔮 Expansão Futura

O projeto está preparado para expansão multi-domínio:

```python
# router.py - Adicione novos domínios:
if "finanças" in q:
    return "financas"
if "saúde" in q:
    return "saude"
```

Crie novos agentes especializados (`agent_financas.py`, `agent_saude.py`) seguindo o padrão de `agent_market.py`.

## 🐛 Resolução de Problemas

### Erro: "GEMINI_API_KEY não encontrada"
- Verifique se criou o arquivo `.env` a partir de `env.example`
- Confirme que a chave está correta no arquivo

### Erro: "SERPAPI_API_KEY não encontrada"
- Obtenha uma chave gratuita em [serpapi.com](https://serpapi.com/)
- Adicione ao arquivo `.env`

### Erro de importação do LangChain
- Reinstale as dependências: `pip install -r requirements.txt --upgrade`

### Erro de limite de API
- Verifique cotas da API Gemini (100 requisições/dia no plano gratuito)
- Verifique cotas do SerpAPI (100 buscas/mês no plano gratuito)

## 📄 Licença

Projeto educacional - uso livre para aprendizado e experimentação.

## 🤝 Contribuições

Para expandir o projeto:
1. Adicione novos domínios no `router.py`
2. Crie novos agentes especializados
3. Adicione novas ferramentas em `tools.py`
4. Implemente testes para novos componentes

---

**Desenvolvido com LangChain 🦜🔗 + Google Gemini 🌟**
