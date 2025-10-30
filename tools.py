"""
Ferramentas para o agente de análise de mercado.
"""
import json
from typing import Any
import os
import requests


def web_search(query: str, num: int = 5, time_period: str | None = None) -> list[dict[str, Any]]:
    """
    Busca notícias/relatórios usando SerpAPI.
    
    Args:
        query: Consulta de busca
        num: Número máximo de resultados (padrão: 5)
    
    Returns:
        Lista de dicionários com title, link, snippet, date
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY não encontrada. Configure no arquivo .env")
    
    try:
        params = {
            "engine": "google",
            "q": query,
            "num": num,
            "api_key": api_key,
        }
        # Filtro temporal opcional (tbs=qdr:<time>)
        if time_period:
            params["tbs"] = f"qdr:{time_period}"

        resp = requests.get("https://serpapi.com/search.json", params=params, timeout=20)
        resp.raise_for_status()
        results = resp.json()
        
        # Normalizar retorno - extrair apenas campos essenciais
        organic_results = results.get("organic_results", [])
        normalized = []
        
        for item in organic_results[:num]:
            normalized.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "date": item.get("date", None)  # Pode ser None se não disponível
            })
        
        return normalized
    
    except requests.HTTPError as e:
        raise RuntimeError(f"Erro HTTP no SerpAPI: {e.response.status_code} {e.response.text[:200]}")
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar no SerpAPI: {str(e)}")


def calc_cagr(start: float, end: float, months: float) -> float:
    """
    Calcula o CAGR (Compound Annual Growth Rate) anualizado.
    
    Args:
        start: Valor inicial (deve ser > 0)
        end: Valor final
        months: Período em meses (deve ser > 0)
    
    Returns:
        CAGR como decimal (ex.: 0.44 para 44%)
    
    Raises:
        ValueError: Se start <= 0 ou months <= 0
    """
    if start <= 0:
        raise ValueError("O valor inicial (start) deve ser maior que zero.")
    
    if months <= 0:
        raise ValueError("O período (months) deve ser maior que zero.")
    
    years = months / 12.0
    cagr = (end / start) ** (1 / years) - 1
    
    return cagr


def report_refine(texto: str) -> str:
    """
    Limpeza leve do texto: trim e normalização de espaços.
    
    Args:
        texto: Texto a ser refinado
    
    Returns:
        Texto refinado
    """
    # Remove espaços extras e linhas vazias desnecessárias
    lines = [line.strip() for line in texto.split('\n')]
    lines = [line for line in lines if line]
    
    # Junta linhas e normaliza espaços múltiplos
    refined = '\n\n'.join(lines)
    
    return refined.strip()

