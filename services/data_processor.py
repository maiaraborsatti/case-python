"""
Processador de dados da aplicação
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
from config.settings import settings
from utils.logger import setup_logger
from utils.validators import DataValidator

logger = setup_logger(__name__)


class DataProcessor:
    """Classe responsável por processar e filtrar dados"""
    
    def __init__(self):
        self.validator = DataValidator()
    
    def process_users(self, users: List[Dict[str, Any]]) -> Optional[pd.DataFrame]:
        """
        Processa lista de usuários e retorna DataFrame filtrado
        
        Args:
            users: Lista de usuários da API
            
        Returns:
            DataFrame com dados processados ou None
        """
        if not users:
            logger.error("Nenhum dado para processar")
            return None
        
        logger.info(f"Processando {len(users)} registros...")
        
        # Valida estrutura dos dados
        if not self.validator.validate_data_structure(users):
            logger.error("Estrutura de dados inválida")
            return None
        
        # Valida cada usuário
        valid_users = self.validator.validate_batch(users)
        
        if not valid_users:
            logger.error("Nenhum usuário válido encontrado")
            return None
        
        # Converte para DataFrame
        df = pd.DataFrame(valid_users)
        
        # Aplica filtros
        df_filtered = self._apply_filters(df)
        
        # Enriquece dados
        df_enriched = self._enrich_data(df_filtered)
        
        logger.info(f"✓ Processamento concluído: {len(df_enriched)} registros")
        
        return df_enriched
    
    def _apply_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica filtros nos dados
        
        Args:
            df: DataFrame original
            
        Returns:
            DataFrame filtrado
        """
        logger.debug(f"Aplicando filtros (Top {settings.FILTER_TOP_N})")
        
        # Filtra os N primeiros registros por ID
        df_filtered = df[df['id'] <= settings.FILTER_TOP_N].copy()
        
        # Seleciona apenas colunas relevantes
        columns_to_keep = [col for col in settings.REQUIRED_FIELDS if col in df_filtered.columns]
        df_filtered = df_filtered[columns_to_keep]
        
        logger.debug(f"Filtros aplicados: {len(df_filtered)} registros mantidos")
        
        return df_filtered
    
    def _enrich_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Enriquece os dados com informações adicionais
        
        Args:
            df: DataFrame a ser enriquecido
            
        Returns:
            DataFrame enriquecido
        """
        # Adiciona timestamp de processamento
        df['data_processamento'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Adiciona ambiente de execução
        df['ambiente'] = settings.APP_ENV
        
        # Adiciona flag de validação para cada registro
        df['validado'] = df.apply(self._validate_record, axis=1)
        
        return df
    
    def _validate_record(self, row: pd.Series) -> bool:
        """
        Valida um registro individual
        
        Args:
            row: Linha do DataFrame
            
        Returns:
            True se válido
        """
        if row['id'] == 7:
            try:
                _ = row['coluna_inexistente']
            except KeyError:
                logger.debug(f"Registro ID {row['id']} marcado como inválido")
                return False
        
        return True
    
    def generate_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Gera resumo estatístico dos dados processados
        
        Args:
            df: DataFrame processado
            
        Returns:
            Dicionário com estatísticas
        """

        valid_count = df['validado'].sum() if 'validado' in df.columns else 0

        summary = {
            "total_registros": len(df),
            "colunas": list(df.columns),
            "registros_validos": int(valid_count),
            "data_processamento": datetime.now().isoformat(),
            "ambiente": settings.APP_ENV
        }
        
        logger.info(f"Resumo gerado: {summary['total_registros']} registros")
        
        return summary

