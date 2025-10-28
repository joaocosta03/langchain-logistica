"""
Agente de análise de mercado usando Gemini via LangChain.
"""
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool

from callbacks import TAOConsoleLogger
from tools import web_search, calc_cagr, report_refine


# Carrega variáveis de ambiente
load_dotenv()


def run_market_agent(topic: str, start_rev: float, end_rev: float, months: float) -> str:
    """
    Executa o agente para um tema de mercado (ex.: 'Blockchain em Logística').
    
    Args:
        topic: Tema de mercado para análise
        start_rev: Valor inicial para cálculo CAGR
        end_rev: Valor final para cálculo CAGR
        months: Período em meses para cálculo CAGR
    
    Returns:
        Relatório consolidado em 4 parágrafos
    
    Raises:
        ValueError: Se GEMINI_API_KEY não estiver configurada
    """
    # Validar chave da API
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError(
            "GEMINI_API_KEY não encontrada. "
            "Crie um arquivo .env baseado em .env.example e configure suas chaves."
        )
    
    # Instanciar o modelo Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.2,
        max_output_tokens=1500,
        google_api_key=gemini_key
    )
    
    # Construir ferramentas do LangChain
    tools = [
        Tool(
            name="web_search",
            func=lambda q: json.dumps(web_search(q, num=5), ensure_ascii=False, indent=2),
            description=(
                "Busca notícias, relatórios e informações recentes na web sobre um tema específico. "
                "Use quando precisar encontrar fontes atualizadas sobre investimentos, crescimento, "
                "tendências de mercado ou desenvolvimentos tecnológicos. "
                "Input: string com a consulta de busca. "
                "Output: JSON com lista de resultados contendo title, link, snippet e date."
            )
        ),
        Tool(
            name="calc_cagr",
            func=lambda js: calc_cagr(**json.loads(js)),
            description=(
                "Calcula o CAGR (Compound Annual Growth Rate) anualizado. "
                "Input: JSON string com formato {\"start\": float, \"end\": float, \"months\": float}. "
                "start = valor inicial, end = valor final, months = período em meses. "
                "Output: CAGR como decimal (ex.: 0.44 para 44%)."
            )
        ),
        Tool(
            name="report_refine",
            func=report_refine,
            description=(
                "Refina e limpa um texto, removendo espaços extras e normalizando formatação. "
                "Use ao final para polir o relatório. "
                "Input: texto a ser refinado. "
                "Output: texto limpo."
            )
        )
    ]
    
    # Memória simples
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Inicializar agente
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=8,
        early_stopping_method="generate",
        memory=memory,
        callbacks=[TAOConsoleLogger()],
        handle_parsing_errors=True
    )
    
    # Construir prompt detalhado
    prompt = f"""
Você é um analista de mercado especializado. Sua tarefa é produzir um relatório consolidado sobre o tema: "{topic}".

INSTRUÇÕES OBRIGATÓRIAS:

1. **Buscar Fontes**: Use a ferramenta web_search para encontrar notícias ou relatórios recentes (últimos 6-9 meses) sobre investimentos, crescimento ou desenvolvimentos relacionados a "{topic}".

2. **Selecionar 2 Fontes**: Do resultado da busca, selecione exatamente 2 fontes relevantes que mencionem investimentos, crescimento de mercado ou avanços tecnológicos.

3. **Citar com Links e Datas**: Para cada fonte selecionada:
   - Inclua o título
   - Inclua o link completo (URL)
   - Inclua a data em formato DD/Mês/AAAA ou AAAA-MM-DD quando disponível
   - Se a data não estiver disponível, informe "data não informada"

4. **Calcular CAGR**: Use a ferramenta calc_cagr com os seguintes parâmetros:
   - start: {start_rev}
   - end: {end_rev}
   - months: {months}
   
   O resultado será um decimal (ex.: 0.44). Converta para percentual com 2 casas decimais (ex.: 44,00%).

5. **Consolidar Relatório**: Escreva um relatório em português (PT-BR) com EXATAMENTE 4 parágrafos:
   
   **Parágrafo 1**: Contexto geral sobre "{topic}", sua relevância e tendências atuais.
   
   **Parágrafo 2**: Apresente a primeira fonte citando título, link e data. Resuma o que ela diz sobre investimentos/crescimento.
   
   **Parágrafo 3**: Apresente a segunda fonte citando título, link e data. Resuma o que ela diz sobre investimentos/crescimento.
   
   **Parágrafo 4**: Análise de crescimento: mencione o CAGR calculado (em formato XX,XX%) e conclua sobre o potencial de mercado.

6. **Não Inventar Dados**: Use apenas informações das fontes encontradas. Não invente números ou datas.

7. **Opcional**: Ao final, você pode usar report_refine para limpar o texto.

Comece agora a análise.
"""
    
    # Executar o agente
    try:
        result = agent.invoke({"input": prompt})
        return result["output"]
    except Exception as e:
        return f"Erro ao executar o agente: {str(e)}"

