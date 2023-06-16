from pydantic import BaseSettings, PostgresDsn


class AppSettings(BaseSettings):
    app_title: str = 'File storage'
    database_dsn: PostgresDsn
    host: str = '127.0.0.1'
    port: int = 8080
    # short_url_id_length: int = 10

    class Config:
        env_file = '.env'


app_settings = AppSettings()
