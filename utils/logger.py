"""
Sistema de logging da aplicação
"""

import logging
import sys
from config.settings import settings


def setup_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger
    
    Args:
        name: Nome do logger
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Handler para console
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Formatter
    formatter = logging.Formatter(settings.LOG_FORMAT)
    handler.setFormatter(formatter)
    
    # Adiciona handler ao logger
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger

