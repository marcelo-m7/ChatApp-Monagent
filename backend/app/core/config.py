"""
Configurações globais da aplicação.

Utiliza Pydantic BaseSettings para ler variáveis de ambiente.  A função
`get_settings` usa cache para não recriar instâncias repetidamente.
"""

from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Define parâmetros configuráveis via variáveis de ambiente."""

    # Diretório onde arquivos enviados serão armazenados
    upload_dir: str = Field(default="uploads", env="UPLOAD_DIR")
    # Nome do agente de assistente padrão (usado em AssistantFeature)
    default_assistant: str = Field(default="programador", env="DEFAULT_ASSISTANT")

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    """Retorna (com cache) uma instância das configurações."""

    return Settings()