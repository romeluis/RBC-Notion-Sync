#!/usr/bin/env python3
"""
Test script for Notion client
"""

import sys
import os
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

from notion_client import NotionClient

def test_notion_client():
    print("Testing Notion Client...")
    
    # Check environment variables
    api_key = os.getenv('NOTION_API_KEY')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    if not api_key:
        print("❌ NOTION_API_KEY environment variable not set")
        print("Please set your Notion API key:")
        print("export NOTION_API_KEY='your_api_key_here'")
        return False
    
    if not database_id:
        print("❌ NOTION_DATABASE_ID environment variable not set")
        print("Please set your Notion database ID:")
        print("export NOTION_DATABASE_ID='your_database_id_here'")
        return False
    
    print(f"✅ API Key: {api_key[:10]}...")
    print(f"✅ Database ID: {database_id[:10]}...")
    
    try:
        # Create client
        client = NotionClient()
        
        # Test connection
        if client.test_connection():
            print("✅ Notion connection successful")
            
            # Create a test transaction
            test_transaction = {
                'id': 'TEST_TRANSACTION_001',
                'title': 'Test Transaction',
                'location': 'Test Location',
                'date': None,  # Will use current date
                'amount': -25.50
            }
            
            print(f"\n🧪 Testing with sample transaction:")
            print(f"   Title: {test_transaction['title']}")
            print(f"   Amount: ${test_transaction['amount']:.2f}")
            
            # Upload test transaction
            success = client.upload_transaction(test_transaction, "Misc")
            
            if success:
                print("✅ Test transaction upload successful")
                return True
            else:
                print("❌ Test transaction upload failed")
                return False
        else:
            print("❌ Notion connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Notion client: {e}")
        return False

if __name__ == "__main__":
    test_notion_client()
