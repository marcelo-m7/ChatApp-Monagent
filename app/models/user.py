"""
Definição do modelo de usuário.

O modelo `User` representa um participante do chat.  Ele é
intencionalmente simples, contendo apenas identificador e nome opcional.
Outros campos, como avatar ou preferências, podem ser adicionados conforme
necessidade.
"""

from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    """Representa um usuário do sistema."""

    id: str
    name: Optional[str] = None

    class Config:
        # Permite validar instâncias de subclasses de User ao comparar igualdade
        frozen = True