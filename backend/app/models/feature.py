"""
Modelos de funcionalidades (features) para mensagens.

Cada feature representa uma capacidade adicional associada a uma mensagem.
O campo `kind` atua como discriminador para que o Pydantic escolha o
submodelo correto ao validar dados.  Você pode adicionar novas features
criando subclasses de `FeatureBase` e adicionando-as à união `Feature`.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Literal, Union, Annotated
from pydantic import BaseModel, Field


class FeatureBase(BaseModel):
    """Classe base para todas as funcionalidades.

    O campo `kind` é usado como discriminador para seleção de submodelo.
    """

    kind: str

    class Config:
        extra = "forbid"


class FileFeature(FeatureBase):
    """Representa um anexo de arquivo associado a uma mensagem."""

    kind: Literal["file"] = "file"
    file_id: str
    file_name: str
    mime_type: Optional[str] = None
    size_bytes: Optional[int] = None
    url: Optional[str] = None


class DMFeature(FeatureBase):
    """Indica que a mensagem é um direct message para usuários específicos."""

    kind: Literal["dm"] = "dm"
    to_user_ids: List[str]


class AssistantFeature(FeatureBase):
    """Solicita a execução de um assistente virtual.

    O campo `input` contém a entrada fornecida pelo usuário.  O campo
    `response` é opcional e será preenchido pelo serviço de assistente
    quando a mensagem for processada.
    """

    kind: Literal["assistant"] = "assistant"
    agent_name: str
    input: str
    response: Optional[str] = None


class ReplyFeature(FeatureBase):
    """Indica que a mensagem é um reply em uma thread."""

    kind: Literal["reply"] = "reply"
    reply_to_message_id: str
    thread_id: Optional[str] = None


class ReactionFeature(FeatureBase):
    """Aplica ou remove uma reação (emoji) a uma mensagem."""

    kind: Literal["reaction"] = "reaction"
    emoji: str
    op: Literal["add", "remove"] = "add"


class EditFeature(FeatureBase):
    """Registra a edição de uma mensagem."""

    kind: Literal["edit"] = "edit"
    edited_at: datetime = Field(default_factory=datetime.utcnow)
    previous_text: str
    new_text: str


class DeleteFeature(FeatureBase):
    """Marca uma mensagem como removida."""

    kind: Literal["delete"] = "delete"
    deleted_at: datetime = Field(default_factory=datetime.utcnow)
    reason: Optional[str] = None


class FileRequestFeature(FeatureBase):
    """Solicita ao backend que crie, edite ou envie um arquivo.

    - Se `action` for "create", é necessário fornecer `file_name` e
      `content` (string).  O serviço criará um novo arquivo e retornará
      um objeto `FileFeature` correspondente.
    - Se `action` for "edit", `file_id` deve ser fornecido junto com
      `content`.  O conteúdo existente do arquivo será substituído.
    - Se `action` for "send", `file_id` deve ser fornecido; o serviço
      retornará um objeto `FileFeature` para anexar à mensagem.
    """

    kind: Literal["file_request"] = "file_request"
    action: Literal["create", "edit", "send"]
    file_id: Optional[str] = None
    file_name: Optional[str] = None
    content: Optional[str] = None


# União discriminada de todas as features
Feature = Annotated[
    Union[
        FileFeature,
        DMFeature,
        AssistantFeature,
        ReplyFeature,
        ReactionFeature,
        EditFeature,
        DeleteFeature,
        FileRequestFeature,
    ],
    Field(discriminator="kind"),
]


__all__ = [
    "FeatureBase",
    "FileFeature",
    "DMFeature",
    "AssistantFeature",
    "ReplyFeature",
    "ReactionFeature",
    "EditFeature",
    "DeleteFeature",
    "FileRequestFeature",
    "Feature",
]