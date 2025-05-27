from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional, List, Dict
import json


class Settings(BaseSettings):
    """
    Application configuration settings, loaded from environment variables or .env file.
    """
    MISS_SPEC_DISCORD_TOKEN: str = Field(..., description="Miss Spec Discord Bot Token")
    MISS_SPEC_CLIENT_ID: str = Field(..., description="Miss Spec Discord Bot Client ID")
    MISS_SPEC_GUILD_IDS: List[int] = Field(default_factory=list, description="List of Miss Spec Discord Guild (Server) IDs to listen to")
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