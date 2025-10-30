"""
Agente de análise de mercado usando Gemini via LangChain.
"""
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# Import dinâmico para compatibilidade entre versões do LangChain
try:
    from langchain.agents import create_agent  # LangChain 1.0+
    _LC_AGENT_API = "create_agent"
except Exception:  # noqa: E722
    create_agent = None  # type: ignore
    try:
        from langchain.agents import create_react_agent, AgentExecutor  # LangChain 0.2.x
        _LC_AGENT_API = "react"
    except Exception:  # noqa: E722
        create_react_agent = None  # type: ignore
        AgentExecutor = None  # type: ignore
        try:
            from langchain.agents import initialize_agent  # LangChain 0.0.x/0.1.x
            _LC_AGENT_API = "initialize"
        except Exception:  # noqa: E722
            initialize_agent = None  # type: ignore
            _LC_AGENT_API = None
# Import compatível de Tool entre versões do LangChain
try:
    from langchain_core.tools import Tool  # LangChain 0.2+
except Exception:  # noqa: E722
    from langchain.tools import Tool  # Fallback para versões antigas

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
        model="gemini-flash-lite-latest",
        temperature=0.2,
        max_output_tokens=1500,
        google_api_key=gemini_key
    )
    
    # Construir ferramentas do LangChain
    tools = [
        Tool(
            name="web_search",
            func=lambda q: json.dumps(web_search(q, num=5, time_period="m6"), ensure_ascii=False, indent=2),
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
    
    # Construir prompt detalhado (usado tanto pelo executor quanto no fallback manual)
    prompt = f"""
Você é um analista de mercado especializado. Sua tarefa é produzir um relatório consolidado sobre o tema: "{topic}".

INSTRUÇÕES OBRIGATÓRIAS:

1. **Buscar Fontes (últimos 6 meses)**: Use a ferramenta web_search para encontrar notícias ou relatórios publicados nos ÚLTIMOS 6 MESES sobre investimentos, crescimento ou desenvolvimentos relacionados a "{topic}".

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
    
    # Construir agente compatível com a versão instalada do LangChain
    print(f"🔍 Usando API do LangChain: {_LC_AGENT_API or 'fallback manual'}\n")
    if _LC_AGENT_API == "create_agent":
        # LangChain 1.0+: create_agent retorna um CompiledStateGraph diretamente executável
        agent_graph = create_agent(
            model=llm,
            tools=tools,
            debug=False,  # Desliga o debug do LangChain
            system_prompt="Você é um analista de mercado especializado."
        )
        # Encapsular o graph em um wrapper para manter compatibilidade com invoke({"input": ...})
        class AgentWrapper:
            def __init__(self, graph, logger):
                self.graph = graph
                self.logger = logger
            def invoke(self, input_dict):
                self.logger.on_chain_start({}, input_dict)
                try:
                    # O create_agent retorna um StateGraph que aceita {"messages": [...]}
                    from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
                    
                    result = self.graph.invoke({"messages": [HumanMessage(content=input_dict["input"])]}, config={"recursion_limit": 50})
                    
                    # Extrair tool calls das mensagens para exibir TAO customizado
                    messages = result.get("messages", [])
                    for i, msg in enumerate(messages):
                        if isinstance(msg, AIMessage) and hasattr(msg, 'tool_calls') and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                self.logger.on_tool_start({"name": tool_call.get("name", "unknown")}, str(tool_call.get("args", {})))
                        
                        elif isinstance(msg, ToolMessage):
                            self.logger.on_tool_end(msg.content if isinstance(msg.content, str) else str(msg.content)[:500])
                    
                    self.logger.on_chain_end({"output": messages[-1].content if messages and hasattr(messages[-1], 'content') else str(result)})
                    return {"output": messages[-1].content if messages and hasattr(messages[-1], 'content') else str(result)}
                except Exception as e:
                    self.logger.on_tool_error(e)
                    raise
        agent = AgentWrapper(agent_graph, TAOConsoleLogger())
    elif _LC_AGENT_API == "react":
        react_agent = create_react_agent(llm=llm, tools=tools)
        agent = AgentExecutor(
            agent=react_agent,
            tools=tools,
            verbose=True,
            max_iterations=8,
            early_stopping_method="generate",
            callbacks=[TAOConsoleLogger()],
            handle_parsing_errors=True
        )
    elif _LC_AGENT_API == "initialize":
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent="zero-shot-react-description",
            verbose=True,
            max_iterations=8,
            early_stopping_method="generate",
            callbacks=[TAOConsoleLogger()],
            handle_parsing_errors=True
        )
    else:
        # Fallback manual: orquestração simples com logs TAO
        print("⚠️  Modo fallback manual ativado (API de agente não disponível)\n")
        logger = TAOConsoleLogger()
        logger.on_chain_start({}, {"input": prompt})

        # Action: web_search
        logger.on_tool_start({"name": "web_search"}, topic)
        try:
            search_results = web_search(f"{topic} investimentos crescimento", num=5, time_period="m6")
            logger.on_tool_end(json.dumps(search_results, ensure_ascii=False)[:500])
        except Exception as e:
            logger.on_tool_error(e)
            raise

        # Pedir ao LLM para escolher 2 fontes e resumir
        selection_prompt = (
            "Você recebeu resultados de busca em JSON. Selecione exatamente 2 fontes relevantes, "
            "citando título, link e data, e produza um breve resumo de 2-3 frases para cada. "
            "Se a data não estiver disponível, escreva 'data não informada'.\n\n"
            f"RESULTADOS:\n{json.dumps(search_results, ensure_ascii=False, indent=2)}\n\n"
            "Responda em JSON com o formato: {\"fontes\": [ {\"titulo\": ..., \"link\": ..., \"data\": ..., \"resumo\": ...}, {...} ]}"
        )
        selection = llm.invoke(selection_prompt)

        # Action: calc_cagr
        logger.on_tool_start({"name": "calc_cagr"}, json.dumps({"start": start_rev, "end": end_rev, "months": months}))
        try:
            cagr_value = calc_cagr(start=start_rev, end=end_rev, months=months)
            logger.on_tool_end(str(cagr_value))
        except Exception as e:
            logger.on_tool_error(e)
            raise

        # Escrever relatório final com 4 parágrafos
        try:
            data = selection.content if hasattr(selection, "content") else str(selection)
            final_prompt = (
                "Com base nas duas fontes selecionadas (JSON a seguir) e no CAGR informado, "
                "escreva um relatório em português (PT-BR) com EXATAMENTE 4 parágrafos: \n"
                "Parágrafo 1: contexto geral do tema.\n"
                "Parágrafo 2: apresente a primeira fonte (título, link, data) e um resumo.\n"
                "Parágrafo 3: apresente a segunda fonte (título, link, data) e um resumo.\n"
                "Parágrafo 4: análise de crescimento mencionando o CAGR em formato XX,XX% e conclusão.\n\n"
                f"FONTES (JSON):\n{data}\n\n"
                f"CAGR decimal: {cagr_value}. Converta para percentual com 2 casas."
            )
            report = llm.invoke(final_prompt)
            text = report.content if hasattr(report, "content") else str(report)
            text = report_refine(text)
            logger.on_chain_end({"output": text})
            return text
        except Exception as e:
            logger.on_tool_error(e)
            raise
    
    
    # Executar o agente
    try:
        result = agent.invoke({"input": prompt})
        return result["output"]
    except Exception as e:
        return f"Erro ao executar o agente: {str(e)}"

