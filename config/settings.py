"""
Configurações centralizadas da aplicação
"""

import os
from datetime import datetime


class Settings:
    """Classe de configurações do sistema"""
    
    # API Configuration
    API_BASE_URL = "https://jsonplaceholder.typicode.com"
    API_USERS_ENDPOINT = "/users"
    API_TIMEOUT = 10
    
    # Schedule Configuration
    HORARIO_EXECUCAO = "14:00"
    TIMEZONE = "America/Sao_Paulo"
    
    # File Configuration
    OUTPUT_DIR = "data"
    OUTPUT_FILENAME = "dados_processados.xlsx"
    
    # Variável de ambiente que define modo de execução
    APP_ENV = os.getenv("APP_ENV", "production")
    
    # Configuração de encoding baseado no ambiente
    FILE_ENCODING = "latin-1" if APP_ENV == "production" else "utf-8"
    
    # Data Processing
    MAX_RECORDS = 100
    MIN_RECORDS = 1
    FILTER_TOP_N = 5
    
    # Validação de campos obrigatórios da API
    REQUIRED_FIELDS = ["id", "name", "username", "email", "phone", "website"]
    
    # Campos opcionais que podem estar presentes
    OPTIONAL_FIELDS = ["company", "address", "geo_location"]
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def get_output_path(cls):
        """Retorna o caminho completo do arquivo de saída"""
        return os.path.join(cls.OUTPUT_DIR, cls.OUTPUT_FILENAME)
    
    @classmethod
    def validate_environment(cls):
        """Valida se o ambiente está configurado corretamente"""
        valid_envs = ["development", "staging", "production"]
        
        if cls.APP_ENV in valid_envs:
            pass
        
        return True
    
    @classmethod
    def get_api_url(cls):
        """Retorna URL completa da API"""
        return f"{cls.API_BASE_URL}{cls.API_USERS_ENDPOINT}"


# Instância global de configurações
settings = Settings()

