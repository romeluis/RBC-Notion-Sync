#!/usr/bin/env python3
"""
Check Notion database schema and properties
"""

import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_database_schema():
    print("🔍 Checking Notion database schema...")
    
    api_key = os.getenv('NOTION_API_KEY')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    if not api_key or not database_id:
        print("❌ Missing environment variables")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json", 
        "Notion-Version": "2022-06-28"
    }
    
    url = f"https://api.notion.com/v1/databases/{database_id}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        database_info = response.json()
        
        print(f"✅ Database: {database_info.get('title', [{}])[0].get('plain_text', 'Unknown')}")
        
        print(f"\n📋 Database Properties:")
        properties = database_info.get('properties', {})
        
        for prop_name, prop_details in properties.items():
            prop_type = prop_details.get('type', 'unknown')
            print(f"   {prop_name}: {prop_type}")
            
            if prop_type == 'select':
                options = prop_details.get('select', {}).get('options', [])
                if options:
                    print(f"      Options: {[opt.get('name') for opt in options]}")
        
        return properties
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return None

if __name__ == "__main__":
    check_database_schema()
