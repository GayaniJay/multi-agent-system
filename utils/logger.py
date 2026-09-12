import logging
import os


def setup_logger():
    logger = logging.getLogger("MAS_System")

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        # Create logs folder
        os.makedirs("logs", exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # -------- Terminal Log --------
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # -------- File Log --------
        file_handler = logging.FileHandler(
            "logs/system.log",
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()