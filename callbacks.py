"""
Callbacks para rastreamento TAO (Thought/Action/Observation).
"""
from typing import Any, Dict, List
# Import compatível entre versões do LangChain
try:
    from langchain_core.callbacks.base import BaseCallbackHandler  # LangChain 0.2+
except Exception:  # noqa: E722
    from langchain.callbacks.base import BaseCallbackHandler  # Fallback versões antigas


class TAOConsoleLogger(BaseCallbackHandler):
    """
    Callback que imprime rastro operacional Thought → Action → Observation.
    """
    
    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Chamado quando uma chain inicia."""
        print("\n" + "="*60)
        print("=== AGENTE INICIADO ===")
        print("="*60)
        # Exibe apenas a parte relevante do input (não toda a estrutura)
        if "input" in inputs:
            print(f"Input: {inputs['input'][:200]}...")
        print("="*60 + "\n")
    
    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Chamado quando uma ferramenta é invocada."""
        tool_name = serialized.get("name", "unknown")
        print(f"\n🔧 Action: {tool_name}")
        # Limita o tamanho do input para não expor dados sensíveis
        display_input = input_str[:500] if len(input_str) > 500 else input_str
        print(f"📥 Action Input: {display_input}")
    
    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Chamado quando uma ferramenta termina."""
        # Limita a observação aos primeiros 500 caracteres
        if isinstance(output, str):
            display_output = output[:500] + "..." if len(output) > 500 else output
        else:
            display_output = str(output)[:500]
        
        print(f"👁️  Observation: {display_output}\n")
    
    def on_tool_error(
        self, error: Exception, **kwargs: Any
    ) -> None:
        """Chamado quando uma ferramenta gera erro."""
        print(f"❌ Tool Error: {str(error)[:200]}\n")
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Chamado quando a chain termina."""
        print("\n" + "="*60)
        print("=== FINAL ===")
        print("="*60)
        if "output" in outputs:
            final_output = outputs["output"]
            # Exibe os primeiros 300 caracteres do output final
            display = final_output[:300] + "..." if len(final_output) > 300 else final_output
            print(f"Output: {display}")
        print("="*60 + "\n")
    
    def on_agent_action(self, action: Any, **kwargs: Any) -> Any:
        """Chamado quando o agente decide uma ação."""
        # Já tratado em on_tool_start, mas podemos adicionar log extra se necessário
        pass
    
    def on_agent_finish(self, finish: Any, **kwargs: Any) -> Any:
        """Chamado quando o agente finaliza."""
        pass

