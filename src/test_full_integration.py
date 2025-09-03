#!/usr/bin/env python3
"""
Full integration test for RBC-Notion-Sync
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Look for .env file in the project root
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
    if env_path.exists():
        print(f"📄 Loaded environment variables from {env_path}")
except ImportError:
    # python-dotenv not installed, fallback to regular environment variables
    pass

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import RBCNotionSync
from test_utils import get_test_qfx_file, print_qfx_file_info

def test_full_integration():
    print("🧪 Testing Full Integration (RBC-Notion-Sync)")
    print("=" * 60)
    
    print("\n1. Checking environment variables...")
    api_key = os.getenv('NOTION_API_KEY')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    if not api_key:
        print("⚠️  NOTION_API_KEY not set - Notion upload will fail")
    else:
        print(f"✅ NOTION_API_KEY: {api_key[:10]}...")
    
    if not database_id:
        print("⚠️  NOTION_DATABASE_ID not set - Notion upload will fail")
    else:
        print(f"✅ NOTION_DATABASE_ID: {database_id[:10]}...")
    
    print("\n2. Testing individual components...")
    
    # Test QFX parsing
    print("\n📁 Testing QFX Parser...")
    try:
        from qfx_parser import QFXParser
        
        # Print info about available QFX files
        if not print_qfx_file_info():
            print("⚠️  Cannot test QFX parsing without files")
            return False
        
        # Get the first available QFX file
        qfx_file = get_test_qfx_file()
        if not qfx_file:
            print("❌ No QFX files found")
            return False
        
        print(f"Using QFX file: {qfx_file.name}")
        
        parser = QFXParser(str(qfx_file))
        transactions = parser.parse_file()
        print(f"✅ QFX Parser: {len(transactions)} transactions parsed")
    except Exception as e:
        print(f"❌ QFX Parser failed: {e}")
        return False
    
    # Test Notion client (if credentials available)
    if api_key and database_id:
        print("\n📤 Testing Notion Client...")
        try:
            from notion_client import NotionClient
            client = NotionClient()
            if client.test_connection():
                print("✅ Notion Client: Connection successful")
            else:
                print("❌ Notion Client: Connection failed")
        except Exception as e:
            print(f"❌ Notion Client failed: {e}")
    
    # Test Ollama (if available)
    print("\n🤖 Testing Ollama...")
    try:
        from transaction_categorizer import TransactionCategorizer
        categorizer = TransactionCategorizer()
        if categorizer.test_connection():
            print("✅ Ollama: Connection successful")
        else:
            print("❌ Ollama: Connection failed")
    except Exception as e:
        print(f"❌ Ollama failed: {e}")
    
    print("\n3. Ready to run full sync!")
    print("To run the complete sync, use:")
    print("python main.py")
    
    return True

if __name__ == "__main__":
    test_full_integration()
