"""
Application bootstrap.

Responsibilities:

- Load configuration
- Initialize logging
- Initialize local database
- Initialize secure storage
- Initialize Ollama runtime
- Initialize application services
- Start desktop UI
"""


def bootstrap_application() -> None:
    """Bootstrap and start the application."""
    import sys
    from src.config.config import get_config
    from src.utils.logger import logger
    from pathlib import Path
    from PySide6.QtWidgets import QApplication
    from src.ui.main_window import MainWindow

    logger.info("Starting Norvi Social Media Agent...")
    
    try:
        config = get_config()
        logger.info(f"Environment: {config.environment}")
        
        logger.info("Initializing local storage database...")
        from src.storage.database.migrations import MigrationManager
        MigrationManager().apply_migrations()
        logger.info("Database migrations applied.")
        
        logger.info("Initialization complete. Core systems ready.")
        
        app = QApplication(sys.argv)
        
        from src.ui.theme import ThemeManager
        ThemeManager.get_instance().apply_theme()
        
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)
