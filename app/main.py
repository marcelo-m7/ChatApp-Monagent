"""
Ponto de entrada da API FastAPI.

Define endpoints para envio de mensagens e listagem de mensagens por sala.
A lógica de processamento das features é aplicada antes de armazenar a
mensagem.
"""

from __future__ import annotations

from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .models import (
    MessageCreate,
    MessageEnvelope,
    Feature,
    FileRequestFeature,
    FileFeature,
    AssistantFeature,
)
from .services import ChatService, FileService, AssistantService
from .core.config import get_settings


app = FastAPI(title="ChatApp Example")

# Instancia serviços singleton
chat_service = ChatService()
file_service = FileService()
assistant_service = AssistantService()

# Monta o diretório de uploads para servir arquivos estáticos
settings = get_settings()
app.mount("/files", StaticFiles(directory=settings.upload_dir), name="files")


@app.post("/messages", response_model=MessageEnvelope)
async def send_message(message: MessageCreate) -> MessageEnvelope:
    """Recebe uma mensagem, processa features e salva-a."""

    # Copia a lista para poder modificar (evita side effect no objeto recebido) - Tipo uma fila
    processed_features: List[Feature] = []
    for feature in message.features:
        # Solicitação de criação/edição/envio de arquivo
        if isinstance(feature, FileRequestFeature):
            if feature.action == "create":
                if not feature.file_name or not feature.content:
                    raise HTTPException(status_code=400, detail="file_name e content são obrigatórios para criação de arquivo")
                meta = file_service.create_file(feature.file_name, feature.content.encode())
                processed_features.append(FileFeature(**meta))
            elif feature.action == "edit":
                if not feature.file_id or not feature.content:
                    raise HTTPException(status_code=400, detail="file_id e content são obrigatórios para edição de arquivo")
                meta = file_service.edit_file(feature.file_id, feature.content.encode())
                processed_features.append(FileFeature(**meta))
            elif feature.action == "send":
                if not feature.file_id:
                    raise HTTPException(status_code=400, detail="file_id é obrigatório para enviar arquivo")
                meta = file_service.send_file(feature.file_id)
                processed_features.append(FileFeature(**meta))
            # FileRequestFeature não deve ser persistida; já foi tratada
            continue
        # Chamada ao assistente
        if isinstance(feature, AssistantFeature):
            response = assistant_service.call(feature.agent_name, feature.input)
            feature.response = response
        # Em outros casos, a feature é copiada tal como veio
        processed_features.append(feature)

    # Cria um novo MessageCreate com features processadas
    processed = MessageCreate(
        room_id=message.room_id,
        author=message.author,
        text=message.text,
        features=processed_features,
    )
    envelope = chat_service.send_message(processed)
    return envelope


@app.get("/rooms/{room_id}/messages", response_model=List[MessageEnvelope])
async def list_messages(room_id: str) -> List[MessageEnvelope]:
    """Retorna todas as mensagens de uma sala."""

    return chat_service.list_messages(room_id)