# 🚀 Instruções Rápidas de Execução

## ⚡ Setup Rápido (5 minutos)

### 1. Criar ambiente virtual e instalar dependências

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Ativar (Linux/macOS)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar chaves de API

```bash
# Copiar template
copy env.example .env

# Editar .env e adicionar suas chaves:
# GEMINI_API_KEY=sua_chave_aqui
# SERPAPI_API_KEY=sua_chave_aqui
```

**Onde obter as chaves:**
- **Gemini**: https://makersuite.google.com/app/apikey
- **SerpAPI**: https://serpapi.com/ (100 buscas grátis/mês)

### 3. Executar o agente

```bash
python main.py
```

### 4. Executar testes

```bash
python tests/test_calc_cagr.py
```

## 📋 Checklist de Aceitação

✅ Instalação sem erros  
✅ Executa `python main.py` com sucesso  
✅ Exibe rastro TAO (Action/Observation) no console  
✅ Gera relatório com 4 parágrafos  
✅ Relatório contém 2 fontes com links  
✅ CAGR aparece como 44,00% (ou valor similar formatado)  
✅ Testes passam (`python tests/test_calc_cagr.py`)  
✅ Erro claro se faltar variável de ambiente  

## 🎯 O que o Agente Faz

1. **Busca** 2 notícias/relatórios sobre "Blockchain em Logística"
2. **Extrai** títulos, links e datas das fontes
3. **Calcula** CAGR: (120/100)^(12/6) - 1 ≈ 0.44 = 44%
4. **Gera** relatório estruturado em 4 parágrafos:
   - Parágrafo 1: Contexto geral
   - Parágrafo 2: Primeira fonte (título, link, data)
   - Parágrafo 3: Segunda fonte (título, link, data)
   - Parágrafo 4: Análise com CAGR

## 🔍 Exemplo de Saída TAO

```
============================================================
=== AGENTE INICIADO ===
============================================================

🔧 Action: web_search
📥 Action Input: Blockchain logística investimentos...
👁️  Observation: [{"title": "...", "link": "...", ...}]

🔧 Action: calc_cagr
📥 Action Input: {"start": 100, "end": 120, "months": 6}
👁️  Observation: 0.44

============================================================
=== FINAL ===
============================================================
>>> RELATÓRIO FINAL:
[4 parágrafos com 2 fontes citadas e CAGR]
============================================================
```

## 🔧 Arquitetura Modular

```
main.py
  └─> router.py (identifica domínio: logística)
      └─> agent_market.py (agente Gemini + LangChain)
          ├─> tools.py (web_search, calc_cagr, report_refine)
          └─> callbacks.py (TAOConsoleLogger para rastro)
```

## 🚀 Expansão Futura

Para adicionar novos domínios (finanças, saúde, etc):

1. **router.py**: Adicionar regra de roteamento
2. **agent_X.py**: Criar novo agente especializado
3. **main.py**: Adicionar chamada ao novo agente

---

**Pronto para produção!** 🎉

