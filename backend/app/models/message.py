"""
Modelos de mensagem do chat.

O modelo `MessageEnvelope` representa uma mensagem completa persistida no
sistema, incluindo identificador único e data/hora de criação.  O modelo
`MessageCreate` é usado para entrada (payload de API) e não possui
`id` nem `created_at`, pois esses campos são gerados pelo servidor.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from .user import User
from .feature import Feature


class MessageCreate(BaseModel):
    """Modelo para criação de uma nova mensagem (entrada da API)."""

    room_id: str
    author: User
    text: Optional[str] = None
    features: List[Feature] = Field(default_factory=list)

    class Config:
        extra = "forbid"


class MessageEnvelope(BaseModel):
    """Modelo completo de mensagem retornado pela API."""

    id: str
    room_id: str
    author: User
    created_at: datetime = Field(default_factory=datetime.utcnow)
    text: Optional[str] = None
    features: List[Feature] = Field(default_factory=list)

    class Config:
        extra = "forbid"