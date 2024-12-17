import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base Configuration Class
class Config:
    """Base configuration with default settings."""
    DB_USER = os.getenv("DB_USER", "default_user")  # Default database user
    DB_PASSWORD = os.getenv("DB_PASSWORD", "default_password")  # Default password
    DB_HOST = os.getenv("DB_HOST", "localhost")  # Default database host
    DB_PORT = os.getenv("DB_PORT", "5432")  # Default PostgreSQL port
    DB_NAME = os.getenv("DB_NAME", "default_database")  # Default database name

    @classmethod
    def get_connection_string(cls):
        """Constructs the connection string dynamically."""
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"


# Development Configuration
class DevConfig(Config):
    """Development-specific settings."""
    DB_NAME = "starcraft_dev"


# Testing Configuration
class TestConfig(Config):
    """Testing-specific settings."""
    DB_NAME = "starcraft_test"


# Production Configuration
class ProdConfig(Config):
    """Production-specific settings."""
    DB_NAME = "starcraft_prod"
    DB_HOST = os.getenv("PROD_DB_HOST", "prod-database-instance.aws.com")  # Example AWS RDS host


# Environment Mapping
configurations = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": ProdConfig,
}

# Determine Current Environment
ENV = os.getenv("APP_ENV", "development")  # Default to 'development' if APP_ENV is not set
CurrentConfig = configurations[ENV]

# Initialize SQLAlchemy Engine
engine = create_engine(CurrentConfig.get_connection_string())

# Create a Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

