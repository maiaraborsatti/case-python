"""
Gerenciador de agendamento e controle de horário
"""

from datetime import datetime
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ScheduleManager:
    """Gerencia o agendamento de execução do sistema"""
    
    def __init__(self):
        self.horario_permitido = settings.HORARIO_EXECUCAO
    
    def pode_executar(self) -> bool:
        """
        Verifica se o horário atual permite a execução
        
        Returns:
            True se pode executar, False caso contrário
        """
        hora_atual = datetime.now().strftime("%H:%M")
        
        if hora_atual == self.horario_permitido:
            logger.info(f"✓ Horário permitido: {hora_atual}")
            return True
        else:
            logger.warning(f"✗ Horário não permitido")
            logger.warning(f"  Atual: {hora_atual}")
            logger.warning(f"  Permitido: {self.horario_permitido}")
            return False
    
    def aguardar_proximo_horario(self):
        """Calcula tempo até próxima execução permitida"""
        from datetime import datetime, timedelta
        
        agora = datetime.now()
        hora_alvo = datetime.strptime(self.horario_permitido, "%H:%M").time()
        
        # Cria datetime para hoje no horário alvo
        execucao_hoje = datetime.combine(agora.date(), hora_alvo)
        
        # Se já passou hoje, agenda para amanhã
        if execucao_hoje <= agora:
            execucao_proxima = execucao_hoje + timedelta(days=1)
        else:
            execucao_proxima = execucao_hoje
        
        tempo_espera = execucao_proxima - agora
        
        logger.info(f"Próxima execução em: {tempo_espera}")
        logger.info(f"Horário: {execucao_proxima.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return tempo_espera

