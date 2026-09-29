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

    logger.info("Starting Nexus...")
    
    try:
        config = get_config()
        logger.info(f"Environment: {config.environment}")
        
        logger.info("Initializing local storage database...")
        from src.storage.database.migrations import MigrationManager
        MigrationManager().apply_migrations()
        logger.info("Database migrations applied.")
        
        from src.services.system.cleanup import run_auto_cleanup
        run_auto_cleanup(days=15)
        
        logger.info("Initialization complete. Core systems ready.")
        
        app = QApplication(sys.argv)
        
        from src.ui.theme import ThemeManager
        theme_mgr = ThemeManager.get_instance()
        theme_mgr.apply_theme()
        
        window = MainWindow()
        # Re-colour the native title bar whenever the user switches theme
        theme_mgr.theme_changed.connect(lambda _: window.on_theme_changed())
        window.show()
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)
