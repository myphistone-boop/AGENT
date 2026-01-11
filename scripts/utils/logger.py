"""
Système de logging configuré
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init

# Initialiser colorama pour Windows
init(autoreset=True)

def setup_logger(name="agent", log_level="INFO"):
    """Configure et retourne un logger"""

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))

    # Éviter les duplicatas
    if logger.handlers:
        return logger

    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler console avec couleurs
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)

    # Handler fichier
    log_dir = Path(__file__).resolve().parent.parent.parent / "outputs" / "reports"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"agent_{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


class ColoredFormatter(logging.Formatter):
    """Formatter avec couleurs pour la console"""

    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        record.msg = f"{log_color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)


# Logger par défaut
logger = setup_logger()


if __name__ == "__main__":
    # Test du logger
    test_logger = setup_logger("test")
    test_logger.debug("Message de debug")
    test_logger.info("Message info")
    test_logger.warning("Message warning")
    test_logger.error("Message erreur")
    test_logger.critical("Message critique")
