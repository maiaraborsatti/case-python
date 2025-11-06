"""
Manipulador de arquivos da aplicação
"""

import os
import pandas as pd
from typing import Optional
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class FileHandler:
    """Classe responsável por salvar dados em arquivos"""
    
    def __init__(self):
        self.output_dir = settings.OUTPUT_DIR
        self.encoding = settings.FILE_ENCODING
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Garante que o diretório de saída existe"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Diretório criado: {self.output_dir}")
    
    def save_to_excel(self, df: pd.DataFrame, filename: Optional[str] = None) -> bool:
        """
        Salva DataFrame em arquivo Excel
        
        Args:
            df: DataFrame a ser salvo
            filename: Nome do arquivo (opcional)
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        if df is None or df.empty:
            logger.error("DataFrame vazio ou None")
            return False
        
        # Define nome do arquivo
        if filename is None:
            filename = settings.OUTPUT_FILENAME
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            logger.info(f"Salvando dados em: {filepath}")
            
            # Salva usando openpyxl como engine principal
            try:
                df.to_excel(filepath, index=False, engine='openpyxl')
            except ImportError:
                logger.warning("openpyxl não encontrado, tentando xlsxwriter...")
                df.to_excel(filepath, index=False, engine='xlsxwriter')
            
            # Verifica se arquivo foi criado
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                logger.info(f"✓ Arquivo salvo com sucesso!")
                logger.info(f"  → Arquivo: {filepath}")
                logger.info(f"  → Tamanho: {file_size} bytes")
                logger.info(f"  → Registros: {len(df)}")
                return True
            else:
                logger.error("Arquivo não foi criado")
                return False
                
        except PermissionError:
            logger.error(f"Sem permissão para escrever em: {filepath}")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo Excel: {e}")
            logger.exception("Detalhes do erro:")
            return False
    
    def save_summary(self, summary: dict, filename: str = "summary.json") -> bool:
        """
        Salva resumo em arquivo JSON
        
        Args:
            summary: Dicionário com resumo
            filename: Nome do arquivo JSON
            
        Returns:
            True se salvou com sucesso
        """
        import json
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding=self.encoding) as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Resumo salvo em: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar resumo: {e}")
            return False

