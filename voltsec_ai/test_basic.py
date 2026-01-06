#!/usr/bin/env python3
"""
Test script for voltsec_ai configuration.
Tests basic functionality without requiring external dependencies.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_config():
    """Test configuration module."""
    print("Testing configuration module...")
    
    from voltsec_ai.config import Config, config
    
    # Test default configuration
    assert config.ollama_base_url == os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    assert config.ollama_model == os.getenv("OLLAMA_MODEL", "nemotron-3-nano:30b")
    assert isinstance(config.ollama_temperature, float)
    
    print(f"  ✓ Default config: {config}")
    
    # Test custom configuration
    os.environ["OLLAMA_BASE_URL"] = "http://test:11434"
    os.environ["OLLAMA_MODEL"] = "test-model"
    os.environ["OLLAMA_TEMPERATURE"] = "0.5"
    
    custom_config = Config()
    assert custom_config.ollama_base_url == "http://test:11434"
    assert custom_config.ollama_model == "test-model"
    assert custom_config.ollama_temperature == 0.5
    
    print(f"  ✓ Custom config: {custom_config}")
    
    print("✓ Configuration tests passed!")


def test_module_structure():
    """Test module structure and imports."""
    print("\nTesting module structure...")
    
    from voltsec_ai import __version__
    print(f"  ✓ Package version: {__version__}")
    
    # Check module files exist
    base_dir = Path(__file__).parent
    required_files = [
        "__init__.py",
        "config.py",
        "tools.py",
        "agents.py",
        "tasks.py",
        "main.py",
        "requirements.txt",
        "README_AI.md",
        "QUICKSTART.md",
        "setup.py"
    ]
    
    for file in required_files:
        file_path = base_dir / file
        assert file_path.exists(), f"Missing required file: {file}"
        print(f"  ✓ Found: {file}")
    
    print("✓ Module structure tests passed!")


def test_requirements():
    """Test requirements.txt format."""
    print("\nTesting requirements.txt...")
    
    req_file = Path(__file__).parent / "requirements.txt"
    with open(req_file) as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    required_packages = ["crewai", "langchain", "langchain-community", "chromadb"]
    
    for pkg in required_packages:
        assert any(pkg in line for line in lines), f"Missing required package: {pkg}"
        print(f"  ✓ Found requirement: {pkg}")
    
    print("✓ Requirements tests passed!")


def main():
    """Run all tests."""
    print("=" * 80)
    print("VOLTSEC_AI - Basic Tests")
    print("=" * 80)
    print()
    
    try:
        test_module_structure()
        test_config()
        test_requirements()
        
        print("\n" + "=" * 80)
        print("ALL TESTS PASSED! ✓")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
