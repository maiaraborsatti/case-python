"""
Cliente para comunicação com APIs externas
"""

import requests
from typing import Optional, Dict, List, Any
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class APIClient:
    """Cliente HTTP para consumo de APIs"""
    
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.timeout = settings.API_TIMEOUT
        self.session = requests.Session()
        
        # Configuração de headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "DataCollector/2.0"
        })
    
    def fetch_users(self) -> Optional[List[Dict[str, Any]]]:
        """
        Busca lista de usuários da API
        
        Returns:
            Lista de usuários ou None em caso de erro
        """
        url = settings.get_api_url()
        
        try:
            logger.info(f"Buscando dados da API: {url}")
            response = self.session.get(url, timeout=self.timeout)
            
            # Verifica status code
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✓ Dados coletados: {len(data)} registros")
                return data
            else:
                logger.error(f"Erro na API: Status {response.status_code}")
                logger.error(f"Response: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao acessar API (>{self.timeout}s)")
            return None
            
        except requests.exceptions.ConnectionError:
            logger.error("Erro de conexão com a API")
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao acessar API: {e}")
            return None
            
        except ValueError as e:
            logger.error(f"Erro ao parsear JSON: {e}")
            return None
    
    def fetch_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca um usuário específico por ID
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dados do usuário ou None
        """
        url = f"{self.base_url}/users/{user_id}"
        
        try:
            logger.debug(f"Buscando usuário ID {user_id}")
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Usuário {user_id} não encontrado")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao buscar usuário {user_id}: {e}")
            return None
    
    def __del__(self):
        """Fecha a sessão ao destruir o objeto"""
        if hasattr(self, 'session'):
            self.session.close()

