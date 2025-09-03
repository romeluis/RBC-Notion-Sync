#!/usr/bin/env python3
"""
Test .env loading functionality
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_env_loading():
    print("🧪 Testing .env file loading...")
    
    # Try to load dotenv
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv is installed")
        
        # Look for .env file
        env_path = Path(__file__).parent.parent / '.env'
        print(f"📍 Looking for .env file at: {env_path}")
        
        if env_path.exists():
            print("✅ .env file found")
            load_dotenv(env_path)
            print("✅ .env file loaded")
        else:
            print("⚠️  .env file not found")
            print("💡 Create a .env file in the project root with your Notion credentials")
            
        # Check if environment variables are available
        notion_api_key = os.getenv('NOTION_API_KEY')
        notion_db_id = os.getenv('NOTION_DATABASE_ID')
        
        if notion_api_key:
            print(f"✅ NOTION_API_KEY: {notion_api_key[:10]}...")
        else:
            print("❌ NOTION_API_KEY not found")
            
        if notion_db_id:
            print(f"✅ NOTION_DATABASE_ID: {notion_db_id[:10]}...")
        else:
            print("❌ NOTION_DATABASE_ID not found")
            
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    
    # Test NotionClient initialization
    try:
        from notion_client import NotionClient
        print("\n🔌 Testing NotionClient initialization...")
        
        if notion_api_key and notion_db_id:
            client = NotionClient()
            print("✅ NotionClient initialized successfully")
        else:
            print("⚠️  Cannot test NotionClient - missing credentials")
            
    except Exception as e:
        print(f"❌ Error initializing NotionClient: {e}")
    
    return True

if __name__ == "__main__":
    test_env_loading()
