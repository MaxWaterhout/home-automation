from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsInit(BaseSettings):
    """Application settings loaded from the .env file or environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    checking_interval: float = Field(..., description="Checking interval in seconds")
    error_retry_interval: float = Field(..., description="Retry interval after errors")
    min_temp: float = Field(..., description="Minimum allowed temperature")
    max_temp: float = Field(..., description="Maximum allowed temperature")
    enable_temp_limit: bool = Field(
        ..., description="Enable temperature limit enforcement"
    )
    save_log: bool = Field(..., description="Enable saving logs to a file")
    log_file: str = Field(..., description="Path to log file")
    max_log_lines: int = Field(
        ..., description="Maximum number of lines before rotating the log"
    )


settings_init = SettingsInit()
