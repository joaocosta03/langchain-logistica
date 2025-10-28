"""
Roteador para múltiplos domínios de análise.
Preparado para expansão futura.
"""


def pick_domain(user_query: str) -> str:
    """
    Seleciona o domínio apropriado baseado na consulta do usuário.
    
    Args:
        user_query: Consulta ou objetivo do usuário
    
    Returns:
        Nome do domínio (ex.: 'logistica', 'financas', 'tecnologia')
    """
    q = user_query.lower()
    
    # Regras simples de roteamento
    if "logística" in q or "logistica" in q or "supply chain" in q:
        return "logistica"
    
    # Futuras expansões:
    # if "finanças" in q or "financas" in q:
    #     return "financas"
    # if "saúde" in q or "saude" in q:
    #     return "saude"
    
    # Default: logística
    return "logistica"

