"""
Ponto de entrada do sistema de agente de análise de mercado.
"""
import sys
from router import pick_domain
from agent_market import run_market_agent


def main():
    """
    Função principal que executa o agente de análise de mercado.
    """
    print("🚀 Iniciando Agente de Análise de Mercado\n")
    
    try:
        # Caso de uso fixo (pode ser expandido para input do usuário)
        topic = "Blockchain em Logística"
        start_rev = 100.0
        end_rev = 120.0
        months = 6.0
        
        # Construir consulta para roteamento
        user_query = f"Analisar o potencial de mercado da tecnologia {topic}"
        
        # Determinar domínio
        domain = pick_domain(user_query)
        print(f"📍 Domínio identificado: {domain}\n")
        
        # Executar agente apropriado
        if domain == "logistica":
            print(f"🔍 Analisando: {topic}")
            print(f"📊 Parâmetros CAGR: start={start_rev}, end={end_rev}, months={months}\n")
            
            report = run_market_agent(
                topic=topic,
                start_rev=start_rev,
                end_rev=end_rev,
                months=months
            )
            
            # Exibir relatório final
            print("\n" + "="*80)
            print(">>> RELATÓRIO FINAL:")
            print("="*80)
            print(report)
            print("="*80 + "\n")
            
        else:
            print(f"❌ Domínio '{domain}' ainda não implementado.")
            sys.exit(1)
    
    except ValueError as ve:
        print(f"\n❌ Erro de Configuração: {ve}")
        print("\n💡 Dica: Crie um arquivo .env baseado em .env.example e configure:")
        print("   - GEMINI_API_KEY (obtenha em https://makersuite.google.com/app/apikey)")
        print("   - SERPAPI_API_KEY (obtenha em https://serpapi.com/)")
        sys.exit(1)
    
    except RuntimeError as re:
        print(f"\n❌ Erro de Execução: {re}")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Erro Inesperado: {type(e).__name__}: {e}")
        sys.exit(1)
    
    print("✅ Execução concluída com sucesso!\n")


if __name__ == "__main__":
    main()

