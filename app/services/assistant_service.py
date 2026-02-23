"""
Serviço simplificado de assistente virtual.

Este serviço simula a interação com um assistente (por exemplo, um
modelo de linguagem).  Em um contexto real, ele pode ser adaptado para
chamar APIs externas como OpenAI, Anthropic, etc.  Aqui, apenas devolve
uma string de resposta baseada na entrada.
"""

class AssistantService:
    """Serviço que responde às mensagens via assistente."""

    def call(self, agent_name: str, user_input: str) -> str:
        """Gera uma resposta simulada para a entrada fornecida."""

        # Em um projeto real, você poderia usar agentes diferentes
        # dependendo de `agent_name`, com prompts específicos.
        return f"[Resposta de {agent_name}]: Recebi sua mensagem '{user_input}'."