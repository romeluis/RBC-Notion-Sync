#!/usr/bin/env python3
"""
Debug script for Notion API issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from notion_client import NotionClient

def debug_notion_upload():
    print("🔍 Debugging Notion API upload issues...")
    
    try:
        client = NotionClient()
        
        # Test connection first
        if not client.test_connection():
            print("❌ Connection test failed")
            return
        
        # Create a simple test transaction
        test_transaction = {
            'id': 'DEBUG_TEST_001',
            'title': 'Test Transaction',
            'location': 'Test Location',
            'date': None,  # Will use current date
            'amount': -25.50
        }
        
        print(f"\n🧪 Testing upload with simple transaction:")
        print(f"   ID: {test_transaction['id']}")
        print(f"   Title: {test_transaction['title']}")
        print(f"   Location: {test_transaction['location']}")
        print(f"   Amount: ${test_transaction['amount']:.2f}")
        
        # Try to format the transaction for Notion
        formatted_data = client._format_transaction_for_notion(test_transaction, "Misc")
        
        print(f"\n📋 Formatted data for Notion:")
        import json
        print(json.dumps(formatted_data, indent=2, default=str))
        
        # Try the upload
        success = client.upload_transaction(test_transaction, "Misc")
        
        if success:
            print("✅ Debug upload successful")
        else:
            print("❌ Debug upload failed")
            
    except Exception as e:
        print(f"❌ Error in debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_notion_upload()
