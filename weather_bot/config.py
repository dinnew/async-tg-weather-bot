from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    # Используем SecretStr для защиты токенов от случайного вывода в логи
    telegram_token: SecretStr
    openweathermap_key: SecretStr

    # Указываем Pydantic читать настройки из .env файла
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

config = Settings()
