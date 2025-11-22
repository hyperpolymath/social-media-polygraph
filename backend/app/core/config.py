from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings and configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="Social Media Polygraph", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    secret_key: str = Field(..., alias="SECRET_KEY")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")

    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    workers: int = Field(default=4, alias="WORKERS")

    # ArangoDB
    arango_host: str = Field(default="localhost", alias="ARANGO_HOST")
    arango_port: int = Field(default=8529, alias="ARANGO_PORT")
    arango_user: str = Field(default="root", alias="ARANGO_USER")
    arango_password: str = Field(..., alias="ARANGO_PASSWORD")
    arango_database: str = Field(default="polygraph", alias="ARANGO_DATABASE")

    # XTDB
    xtdb_host: str = Field(default="localhost", alias="XTDB_HOST")
    xtdb_port: int = Field(default=3000, alias="XTDB_PORT")
    xtdb_node_url: str = Field(default="http://localhost:3000", alias="XTDB_NODE_URL")

    # Dragonfly
    dragonfly_host: str = Field(default="localhost", alias="DRAGONFLY_HOST")
    dragonfly_port: int = Field(default=6379, alias="DRAGONFLY_PORT")
    dragonfly_db: int = Field(default=0, alias="DRAGONFLY_DB")
    dragonfly_password: Optional[str] = Field(default=None, alias="DRAGONFLY_PASSWORD")
    cache_ttl: int = Field(default=3600, alias="CACHE_TTL")

    # External APIs
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")
    newsapi_key: Optional[str] = Field(default=None, alias="NEWSAPI_KEY")
    factcheck_api_key: Optional[str] = Field(default=None, alias="FACTCHECK_API_KEY")

    # Rate Limiting
    rate_limit_requests: int = Field(default=100, alias="RATE_LIMIT_REQUESTS")
    rate_limit_period: int = Field(default=60, alias="RATE_LIMIT_PERIOD")

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        alias="CORS_ORIGINS",
    )
    cors_allow_credentials: bool = Field(default=True, alias="CORS_ALLOW_CREDENTIALS")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # JWT
    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_days: int = Field(default=7, alias="REFRESH_TOKEN_EXPIRE_DAYS")

    # ML Models
    spacy_model: str = Field(default="en_core_web_lg", alias="SPACY_MODEL")
    transformers_cache: str = Field(default="./models_cache", alias="TRANSFORMERS_CACHE")
    use_gpu: bool = Field(default=False, alias="USE_GPU")

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default="json", alias="LOG_FORMAT")

    # Celery
    celery_broker_url: str = Field(
        default="redis://localhost:6379/1", alias="CELERY_BROKER_URL"
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/2", alias="CELERY_RESULT_BACKEND"
    )

    # Feature Flags
    enable_fact_checking: bool = Field(default=True, alias="ENABLE_FACT_CHECKING")
    enable_sentiment_analysis: bool = Field(default=True, alias="ENABLE_SENTIMENT_ANALYSIS")
    enable_source_credibility: bool = Field(default=True, alias="ENABLE_SOURCE_CREDIBILITY")
    enable_temporal_tracking: bool = Field(default=True, alias="ENABLE_TEMPORAL_TRACKING")

    @property
    def arango_url(self) -> str:
        """Get ArangoDB connection URL."""
        return f"http://{self.arango_host}:{self.arango_port}"

    @property
    def dragonfly_url(self) -> str:
        """Get Dragonfly connection URL."""
        password_part = f":{self.dragonfly_password}@" if self.dragonfly_password else ""
        return f"redis://{password_part}{self.dragonfly_host}:{self.dragonfly_port}/{self.dragonfly_db}"


settings = Settings()
