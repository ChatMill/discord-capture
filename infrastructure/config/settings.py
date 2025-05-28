import json
from enum import Enum
from typing import List, Dict

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings, loaded from environment variables or .env file.
    """
    MISS_SPEC_DISCORD_TOKEN: str = Field(..., description="Miss Spec Discord Bot Token")
    MISS_SPEC_CLIENT_ID: str = Field(..., description="Miss Spec Discord Bot Client ID")
    MISS_SPEC_GUILD_IDS: List[int] = Field(default_factory=list,
                                           description="List of Miss Spec Discord Guild (Server) IDs to listen to")
    AGENT_ROUTES: Dict[str, str] = Field(default_factory=dict, description="Agent webhook routes mapping")
    PUBLISH_ROUTES: Dict[str, str] = Field(default_factory=dict, description="Publish endpoint routes mapping")
    MAX_MESSAGE_FETCH_COUNT: int = Field(default=25, description="Max messages to fetch per request")
    JWT_SECRET: str = Field(..., description="JWT secret key for signing tokens")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT signing algorithm")
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, description="Max requests per minute")
    RATE_LIMIT_BURST: int = Field(default=10, description="Max burst requests allowed")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    MONGODB_URI: str = Field(..., description="MongoDB connection URI")
    MONGODB_DB_NAME: str = Field(default="chatmill", description="MongoDB database name")
    PORT: int = Field(default=8000, description="API server port")
    HOST: str = Field(default="0.0.0.0", description="API server host")

    @validator("MISS_SPEC_GUILD_IDS", pre=True)
    def parse_guild_ids(cls, v):
        if isinstance(v, str):
            return [int(i.strip()) for i in v.split(",") if i.strip()]
        return v

    @validator("AGENT_ROUTES", "PUBLISH_ROUTES", pre=True)
    def parse_json_dict(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return {}
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


class AgentServiceName(str, Enum):
    MISS_SPEC = "missspec"  # Miss Spec agent service
    # Add more agent service names as needed


class PublisherServiceName(str, Enum):
    GITHUB = "github"  # GitHub publisher
    NOTION = "notion"  # Notion publisher
    CONFLUENCE = "confluence"  # Confluence publisher
    FEISHU = "feishu"  # Feishu publisher
    # Add more publisher service names as needed


def get_agent_base_url(agent: AgentServiceName) -> str:
    """
    Get the base URL for the given agent service name in a type-safe way.
    :param agent: AgentServiceName enum value
    :return: Base URL as string
    """
    url = settings.AGENT_ROUTES.get(str(agent))
    if not url:
        raise ValueError(f"No base URL configured for agent: {agent}")
    return url


def get_publish_base_url(publisher: PublisherServiceName) -> str:
    """
    Get the base URL for the given publisher service name in a type-safe way.
    :param publisher: PublisherServiceName enum value
    :return: Base URL as string
    """
    url = settings.PUBLISH_ROUTES.get(str(publisher))
    if not url:
        raise ValueError(f"No base URL configured for publisher: {publisher}")
    return url
