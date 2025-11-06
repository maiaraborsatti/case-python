"""
Aplicação Principal - Sistema de Coleta e Processamento de Dados v2.0

Este sistema coleta dados de APIs públicas, processa e salva em Excel.
Executa apenas em horário específico configurado.

Arquitetura:
- app/: Lógica principal da aplicação
- config/: Configurações centralizadas
- services/: Serviços de integração (API, processamento, arquivos)
- utils/: Utilitários e helpers
"""

import sys
import os

# Adiciona o diretório raiz ao path para imports funcionarem
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from config.settings import settings
from utils.logger import setup_logger
from app.scheduler import ScheduleManager
from services.api_client import APIClient
from services.data_processor import DataProcessor
from services.file_handler import FileHandler

# Configura logger
logger = setup_logger(__name__)


class Application:
    """Classe principal da aplicação"""
    
    def __init__(self):
        logger.info("="*70)
        logger.info("SISTEMA DE COLETA E PROCESSAMENTO DE DADOS v2.0")
        logger.info("="*70)
        logger.info(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Ambiente: {settings.APP_ENV}")
        logger.info(f"Encoding: {settings.FILE_ENCODING}")
        logger.info("")
        
        # Inicializa componentes
        self.scheduler = ScheduleManager()
        self.api_client = APIClient()
        self.data_processor = DataProcessor()
        self.file_handler = FileHandler()
        
        # Valida configuração do ambiente
        if not settings.validate_environment():
            logger.error("Ambiente inválido!")
            logger.error("Configure a variável APP_ENV corretamente")
        
        self._setup_directories()
    
    def _setup_directories(self):
        """Configura diretórios necessários"""
        try:
            os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
        except OSError as e:
            logger.error(f"Erro ao criar diretório: {e}")
    
    def executar(self) -> bool:
        """
        Método principal que orquestra a execução
        
        Returns:
            True se executou com sucesso, False caso contrário
        """
        try:
            # Passo 1: Verifica horário
            logger.info("PASSO 1: Verificando horário de execução...")
            if not self.scheduler.pode_executar():
                 logger.warning("Sistema só pode ser executado às 14:00")
                 logger.info("Use APP_ENV=development para ignorar horário")
                 self.scheduler.aguardar_proximo_horario()
                 return False
            
            # Passo 2: Coleta dados da API
            logger.info("\nPASSO 2: Coletando dados da API...")
            dados = self.api_client.fetch_users()
            
            if dados is None:
                logger.error("✗ Falha ao coletar dados da API")
                return False
            
            # Passo 3: Processa dados
            logger.info("\nPASSO 3: Processando e validando dados...")
            df_processado = self.data_processor.process_users(dados)
            
            if df_processado is None or df_processado.empty:
                logger.error("✗ Falha no processamento dos dados")
                return False
            
            # Passo 4: Gera resumo
            logger.info("\nPASSO 4: Gerando resumo estatístico...")
            summary = self.data_processor.generate_summary(df_processado)
            
            # Passo 5: Salva arquivos
            logger.info("\nPASSO 5: Salvando arquivos...")
            
            # Salva Excel
            excel_ok = self.file_handler.save_to_excel(df_processado)
            if not excel_ok:
                logger.error("✗ Falha ao salvar arquivo Excel")
                return False
            
            # Salva resumo
            summary_ok = self.file_handler.save_summary(summary)
            if not summary_ok:
                logger.warning("⚠ Falha ao salvar resumo (não crítico)")
            
            # Sucesso!
            logger.info("\n" + "="*70)
            logger.info("✓ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
            logger.info("="*70)
            logger.info(f"Total de registros processados: {len(df_processado)}")
            logger.info(f"Arquivo gerado: {settings.get_output_path()}")
            logger.info(f"Ambiente: {settings.APP_ENV}")
            
            return True
            
        except KeyboardInterrupt:
            logger.warning("\n⚠ Execução interrompida pelo usuário")
            return False
            
        except Exception as e:
            logger.error(f"\n✗ Erro inesperado durante execução: {e}")
            logger.exception("Detalhes completos do erro:")
            return False


def main():
    """Função de entrada da aplicação"""
    try:
        # Cria e executa aplicação
        app = Application()
        sucesso = app.executar()
        
        # Define código de saída
        sys.exit(0 if sucesso else 1)
        
    except Exception as e:
        logger.error(f"Erro crítico: {e}")
        logger.exception("Stack trace completo:")
        sys.exit(1)


if __name__ == "__main__":
    main()

