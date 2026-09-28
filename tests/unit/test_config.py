from src.config.config import AppConfig

def test_default_config():
    """Test that configuration loads with default values when no .env is present."""
    config = AppConfig(
        environment="test",
        log_level="DEBUG"
    )
    
    assert config.environment == "test"
    assert config.log_level == "DEBUG"
    assert config.app_data_dir == "app_data"
    assert config.ollama_model == "gemma4:cloud"
