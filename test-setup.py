#!/usr/bin/env python3
"""
Test script to verify Claude Live Viewer setup
"""

import os
import sys
from pathlib import Path

def test_environment():
    """Test environment setup"""
    print("🧪 Testing Claude Live Viewer Setup")
    print("=" * 50)
    
    # Test environment variables
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        if api_key.startswith("sk-ant-"):
            print("✅ ANTHROPIC_API_KEY is set and looks valid")
        else:
            print("⚠️  ANTHROPIC_API_KEY is set but doesn't look like a valid key")
    else:
        print("❌ ANTHROPIC_API_KEY is not set")
        return False
    
    # Test Python dependencies
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI not installed")
        return False
    
    try:
        import anthropic
        print(f"✅ Anthropic SDK {anthropic.__version__}")
    except ImportError:
        print("❌ Anthropic SDK not installed")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn available")
    except ImportError:
        print("❌ Uvicorn not installed")
        return False
    
    # Test file structure
    project_root = Path(__file__).parent
    
    required_files = [
        "backend/main.py",
        "backend/claude_agent.py", 
        "backend/screen_capture.py",
        "backend/activity_logger.py",
        "backend/behavioral_system.py",
        "frontend/package.json",
        "frontend/pages/index.tsx",
        "scripts/start-vm.sh",
        ".env"
    ]
    
    for file_path in required_files:
        if (project_root / file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            return False
    
    # Test Anthropic API connection
    print("\n🔗 Testing Anthropic API connection...")
    try:
        client = anthropic.Anthropic(api_key=api_key)
        # Simple test - just create the client, don't make a request
        print("✅ Anthropic client created successfully")
    except Exception as e:
        print(f"❌ Anthropic API connection failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Claude Live Viewer is ready to run.")
    print("\nNext steps:")
    print("1. Start the VM: ./scripts/start-vm.sh")
    print("2. In another terminal, start the frontend: cd frontend && npm run dev")
    print("3. Access the web interface at http://localhost:3000")
    
    return True

if __name__ == "__main__":
    # Load environment variables
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
    
    success = test_environment()
    sys.exit(0 if success else 1)