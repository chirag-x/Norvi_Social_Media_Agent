import sys
from pathlib import Path

# Add project root to path so we can run directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.config.config import get_config
from src.utils.logger import logger

def main():
    """
    Main entry point for the Nexus application.
    """
    logger.info("Starting Nexus...")
    
    try:
        config = get_config()
        logger.info(f"Environment: {config.environment}")
        logger.info(f"Ollama Target: {config.ollama_model} @ {config.ollama_host}")
        
        # Make sure app data dir exists
        app_data_path = Path(config.app_data_dir)
        app_data_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("Initialization complete. Core systems ready.")
        
        from PySide6.QtWidgets import QApplication
        from src.ui.main_window import MainWindow

        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
