import logging
import os
from datetime import datetime
from utils.config import Config

def setup_logger(name=__name__):
    """Configurar logger con archivo y consola"""
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evitar logs duplicados
    if logger.handlers:
        return logger
    
    # Crear directorio de logs si no existe
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    
    # Formato del log
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    # Handler para archivo
    log_filename = f"avianca_test_{datetime.now().strftime('%Y%m%d')}.log"
    log_filepath = os.path.join(Config.LOG_DIR, log_filename)
    
    file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    return logger

# Logger global
logger = setup_logger(__name__)