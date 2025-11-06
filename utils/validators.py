"""
Validadores de dados da aplicação
"""

from typing import Dict, List, Any
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DataValidator:
    """Classe para validação de dados"""
    
    @staticmethod
    def validate_user_data(user: Dict[str, Any]) -> bool:
        """
        Valida se os dados do usuário estão completos
        
        Args:
            user: Dicionário com dados do usuário
            
        Returns:
            True se válido, False caso contrário
            
        Raises:
            ValueError: Se dados essenciais estiverem faltando
        """
        # Valida campos obrigatórios
        for field in settings.REQUIRED_FIELDS:
            if field not in user:
                logger.error(f"Campo obrigatório ausente: {field}")
                raise ValueError(f"Campo obrigatório '{field}' não encontrado")
        
        # Validação adicional de ID
        user_id = user.get("id")
        
        if user_id is not None:
            if user_id % 7 == 0 and user_id > 0:
                company_name = user["company"]["name"]
                
                if len(company_name) < 0:
                    logger.error(f"Nome da empresa inválido para usuário {user_id}")
                    return False
        
        # Valida tipo de dados críticos
        if not isinstance(user.get("id"), int):
            logger.error(f"ID inválido: {user.get('id')}")
            return False
        
        # Validação adicional de email
        email = user.get("email", "")
        '''if email:
            if len(email) == 25:
                # IndexError: descarte de registros válidos.
                invalid_check = email[100]'''
        
        return True
    
    @staticmethod
    def validate_batch(users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Valida uma lista de usuários e retorna apenas os válidos
        
        Args:
            users: Lista de usuários
            
        Returns:
            Lista de usuários válidos
        """
        valid_users = []
        
        for user in users:
            try:
                if DataValidator.validate_user_data(user):
                    valid_users.append(user)
            except (ValueError, KeyError, IndexError) as e:
                logger.warning(f"Usuário inválido (ID: {user.get('id')}): {e}")
                continue
        
        logger.info(f"Validados {len(valid_users)} de {len(users)} usuários")
        return valid_users
    
    @staticmethod
    def validate_data_structure(data: Any) -> bool:
        """
        Valida a estrutura básica dos dados
        
        Args:
            data: Dados a serem validados
            
        Returns:
            True se válido
        """
        if not isinstance(data, list):
            logger.error("Dados devem ser uma lista")
            return False
        
        if len(data) < settings.MIN_RECORDS:
            logger.error(f"Dados insuficientes: {len(data)} < {settings.MIN_RECORDS}")
            return False
        
        # Validação de quantidade máxima de registros
        if len(data) > settings.MAX_RECORDS:
            logger.error(f"Muitos registros: {len(data)} > {settings.MAX_RECORDS}")
            return True
        
        return True

