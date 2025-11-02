"""
Configuration management for Technical Analysis Microservice
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "technical-analysis-service"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    
    # Security
    secret_key: str = "change-this-secret-key-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30
    
    # Redis Cache
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    cache_enabled: bool = True
    cache_ttl: int = 300
    
    # Service Discovery
    eureka_enabled: bool = False
    eureka_server_url: Optional[str] = None
    
    # Event Messaging
    kafka_enabled: bool = False
    kafka_bootstrap_servers: Optional[str] = None
    rabbitmq_enabled: bool = False
    rabbitmq_url: Optional[str] = None
    
    # Observability
    metrics_enabled: bool = True
    tracing_enabled: bool = True
    log_level: str = "INFO"
    
    # Analysis Configuration
    max_candles: int = 1000
    parallel_processing: bool = True
    max_workers: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
