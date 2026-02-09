"""Configuration file validator for graceful error handling."""
import json
import os
from pathlib import Path
from typing import Dict, Any


def load_json_config(file_path: Path) -> Dict[str, Any]:
    """
    Load and validate JSON configuration file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data as dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in {file_path}: {e.msg}",
                e.doc,
                e.pos
            )


def validate_targets_config(config: Dict[str, Any]) -> bool:
    """Validate targets.json structure."""
    if "apps" not in config or "params" not in config:
        raise ValueError("targets.json must contain 'apps' and 'params' keys")
    
    if not isinstance(config["apps"], list):
        raise ValueError("'apps' must be a list")
    
    if not isinstance(config["params"], dict):
        raise ValueError("'params' must be a dictionary")
    
    # Validate each app entry
    for app in config["apps"]:
        if "name" not in app or "url" not in app:
            raise ValueError("Each app must have 'name' and 'url' fields")
    
    # Validate params
    if "days_back" not in config["params"] or "max_reviews" not in config["params"]:
        raise ValueError("'params' must contain 'days_back' and 'max_reviews'")
    
    return True


def validate_pain_keywords_config(config: Dict[str, Any]) -> bool:
    """Validate pain_keywords.json structure."""
    if "categories" not in config:
        raise ValueError("pain_keywords.json must contain 'categories' key")
    
    if not isinstance(config["categories"], dict):
        raise ValueError("'categories' must be a dictionary")
    
    # Validate each category
    for category_name, category_data in config["categories"].items():
        if "keywords" not in category_data or "weight" not in category_data:
            raise ValueError(f"Category '{category_name}' must have 'keywords' and 'weight' fields")
        
        if not isinstance(category_data["keywords"], list):
            raise ValueError(f"Category '{category_name}' keywords must be a list")
        
        if not isinstance(category_data["weight"], (int, float)):
            raise ValueError(f"Category '{category_name}' weight must be a number")
    
    return True


def validate_settings_config(config: Dict[str, Any]) -> bool:
    """Validate settings.json structure."""
    required_sections = ["filters", "weights", "processing"]
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"settings.json must contain '{section}' key")
        
        if not isinstance(config[section], dict):
            raise ValueError(f"'{section}' must be a dictionary")
    
    # Validate filters
    filters = config["filters"]
    filter_fields = {
        "min_star_rating": (int, float),
        "min_review_length_words": (int,),
        "drop_generic_5_star": (bool,),
        "force_fetch_count": (int,)
    }
    
    for field, field_type in filter_fields.items():
        if field not in filters:
            raise ValueError(f"'filters' must contain '{field}' field")
        if not isinstance(filters[field], field_type):
            raise ValueError(f"'filters.{field}' must be {field_type}")
    
    # Validate weights
    weights = config["weights"]
    weight_fields = [
        "slope_impact", "volume_impact", "critical_keyword",
        "scam_keyword", "performance_keyword", "ux_keyword"
    ]
    
    for field in weight_fields:
        if field not in weights:
            raise ValueError(f"'weights' must contain '{field}' field")
        if not isinstance(weights[field], (int, float)):
            raise ValueError(f"'weights.{field}' must be a number")
    
    # Validate processing
    processing = config["processing"]
    if "enable_smoke_test" not in processing or "days_back_default" not in processing:
        raise ValueError("'processing' must contain 'enable_smoke_test' and 'days_back_default'")
    
    if not isinstance(processing["enable_smoke_test"], bool):
        raise ValueError("'processing.enable_smoke_test' must be a boolean")
    
    if not isinstance(processing["days_back_default"], int):
        raise ValueError("'processing.days_back_default' must be an integer")
    
    return True


if __name__ == "__main__":
    # Test validation
    config_dir = Path(__file__).parent.parent / "config"
    
    try:
        targets = load_json_config(config_dir / "targets.json")
        validate_targets_config(targets)
        print("✓ targets.json is valid")
        
        pain_keywords = load_json_config(config_dir / "pain_keywords.json")
        validate_pain_keywords_config(pain_keywords)
        print("✓ pain_keywords.json is valid")
        
        settings = load_json_config(config_dir / "settings.json")
        validate_settings_config(settings)
        print("✓ settings.json is valid")
        
    except Exception as e:
        print(f"✗ Configuration validation failed: {e}")
        exit(1)
