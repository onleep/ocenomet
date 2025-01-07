import logging
import os
from logging.handlers import RotatingFileHandler

# Настраивает логгер с ротацией файлов логов.
def setup_logger():
    log_folder = 'logs'
    os.makedirs(log_folder, exist_ok=True)

    log_file = os.path.join(log_folder, 'app.log')
    logger = logging.getLogger("app_logger")

    # Установка обработчиков только один раз
    if not logger.hasHandlers():
        handler = RotatingFileHandler(
            log_file, maxBytes=10**6, backupCount=3, encoding="utf-8"
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    return logger
