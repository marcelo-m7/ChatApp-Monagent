"""
Serviço responsável por armazenar e recuperar mensagens das salas.

Por se tratar de um exemplo, utiliza armazenamento em memória.  Em um
projeto real, seria possível trocar por uma implementação baseada em
banco de dados ou mensageria sem alterar a interface de uso.
"""

from __future__ import annotations

from typing import Dict, List
from uuid import uuid4

from ..models.message import MessageEnvelope, MessageCreate
from ..models.feature import Feature


class ChatService:
    """Orquestra o armazenamento das mensagens por sala."""

    def __init__(self) -> None:
        # Dicionário: room_id -> lista de mensagens
        self._rooms: Dict[str, List[MessageEnvelope]] = {}

    def send_message(self, msg: MessageCreate) -> MessageEnvelope:
        """Armazena uma mensagem e retorna o envelope completo.

        Gera um novo identificador e timestamp para a mensagem.  Não
        realiza validações adicionais (essas devem ocorrer antes de
        chegar aqui).  Se a sala não existir, ela é criada
        automaticamente.
        """

        message_id = str(uuid4())
        envelope = MessageEnvelope(
            id=message_id,
            room_id=msg.room_id,
            author=msg.author,
            text=msg.text,
            features=msg.features,
        )
        self._rooms.setdefault(msg.room_id, []).append(envelope)
        return envelope

    def list_messages(self, room_id: str) -> List[MessageEnvelope]:
        """Retorna todas as mensagens de uma sala ordenadas por criação."""

        return list(self._rooms.get(room_id, []))