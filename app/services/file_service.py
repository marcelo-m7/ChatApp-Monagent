"""
Serviço responsável por gerenciar arquivos anexados e solicitações de
criação/edição/envio de arquivos.

Nesta implementação simplificada, os arquivos são armazenados em disco e
um dicionário em memória mantém os metadados (identificador e nome
original).  Em um cenário real, poderia ser substituído por um storage
em nuvem (S3, GCS etc.).
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Dict, Optional

from fastapi import HTTPException

from ..core.config import get_settings


class FileService:
    """Gerencia criação, edição e recuperação de arquivos."""

    def __init__(self, upload_dir: Optional[str] = None) -> None:
        settings = get_settings()
        # Prioriza o argumento passado; se None, usa configuração
        self.upload_dir = Path(upload_dir or settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        # Tabela file_id -> nome do arquivo salvo (com prefixo id)
        self._file_index: Dict[str, str] = {}

    def _get_saved_filename(self, file_id: str) -> str:
        """Retorna o nome salvo em disco a partir do id."""

        saved = self._file_index.get(file_id)
        if not saved:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        return saved

    def create_file(self, file_name: str, content: bytes) -> Dict[str, str]:
        """Cria um novo arquivo no disco e registra metadados.

        Retorna um dicionário com `file_id`, `file_name` e `url`.
        """

        file_id = str(uuid.uuid4())
        # Sanitiza o nome original removendo separadores de diretórios
        safe_name = os.path.basename(file_name)
        saved_name = f"{file_id}_{safe_name}"
        path = self.upload_dir / saved_name
        with path.open("wb") as f:
            f.write(content)
        self._file_index[file_id] = saved_name
        return {
            "file_id": file_id,
            "file_name": file_name,
            "url": f"/files/{saved_name}",
        }

    def edit_file(self, file_id: str, content: bytes) -> Dict[str, str]:
        """Sobrescreve o conteúdo de um arquivo existente e retorna metadados."""

        saved_name = self._get_saved_filename(file_id)
        path = self.upload_dir / saved_name
        with path.open("wb") as f:
            f.write(content)
        # Retorna os mesmos metadados; o URL não muda
        return {
            "file_id": file_id,
            "file_name": saved_name.split("_", 1)[1],
            "url": f"/files/{saved_name}",
        }

    def send_file(self, file_id: str) -> Dict[str, str]:
        """Retorna os metadados de um arquivo sem modificá-lo."""

        saved_name = self._get_saved_filename(file_id)
        original_name = saved_name.split("_", 1)[1]
        return {
            "file_id": file_id,
            "file_name": original_name,
            "url": f"/files/{saved_name}",
        }