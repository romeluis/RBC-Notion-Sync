"""
Notion API client for uploading transactions
"""

import os
import requests
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Look for .env file in the project root (parent of src directory)
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed, fallback to regular environment variables
    pass


class NotionClient:
    def __init__(self, api_key: Optional[str] = None, database_id: Optional[str] = None):
        self.api_key = api_key or os.getenv('NOTION_API_KEY')
        self.database_id = database_id or os.getenv('NOTION_DATABASE_ID')
        
        if not self.api_key:
            raise ValueError("NOTION_API_KEY environment variable is required")
        if not self.database_id:
            raise ValueError("NOTION_DATABASE_ID environment variable is required")
        
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def _format_transaction_for_notion(self, transaction: Dict, category: str = "Misc") -> Dict:
        """
        Format transaction data for Notion API
        """
        # Format date for Notion (ISO 8601)
        date_str = transaction['date'].isoformat() if transaction['date'] else datetime.now().isoformat()
        
        # Ensure amount is negative for purchases
        amount = transaction['amount']
        if amount > 0:
            amount = -amount
        
        return {
            "properties": {
                "ID": {
                    "rich_text": [
                        {
                            "text": {
                                "content": transaction['id']
                            }
                        }
                    ]
                },
                "Transaction Title": {
                    "title": [
                        {
                            "text": {
                                "content": transaction['title']
                            }
                        }
                    ]
                },
                "Location": {
                    "rich_text": [
                        {
                            "text": {
                                "content": transaction['location']
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": date_str
                    }
                },
                "Amount": {
                    "number": amount
                },
                "Transaction Category": {
                    "select": {
                        "name": category
                    }
                }
            }
        }
    
    def check_if_transaction_exists(self, transaction_id: str) -> bool:
        """
        Check if a transaction with the given ID already exists in the database
        """
        url = f"{self.base_url}/databases/{self.database_id}/query"
        
        query_data = {
            "filter": {
                "property": "ID",
                "rich_text": {
                    "equals": transaction_id
                }
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=query_data)
            response.raise_for_status()
            
            results = response.json().get('results', [])
            return len(results) > 0
            
        except requests.exceptions.RequestException as e:
            print(f"Error checking if transaction exists: {e}")
            return False
    
    def upload_transaction(self, transaction: Dict, category: str = "Misc") -> bool:
        """
        Upload a single transaction to Notion database
        Returns True if successful, False otherwise
        """
        # Check if transaction already exists
        if self.check_if_transaction_exists(transaction['id']):
            print(f"Transaction {transaction['id']} already exists, skipping...")
            return True
        
        url = f"{self.base_url}/pages"
        
        # Format transaction data for Notion
        notion_data = self._format_transaction_for_notion(transaction, category)
        notion_data["parent"] = {"database_id": self.database_id}
        
        try:
            response = requests.post(url, headers=self.headers, json=notion_data)
            response.raise_for_status()
            
            print(f"✅ Uploaded: {transaction['title']} (${transaction['amount']:.2f})")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error uploading transaction {transaction['id']}: {e}")
            if hasattr(e, 'response') and e.response:
                try:
                    error_detail = e.response.json()
                    print(f"Response details: {error_detail}")
                except:
                    print(f"Response text: {e.response.text}")
            return False
    
    def upload_transactions(self, transactions: List[Dict], categories: Optional[List[str]] = None) -> int:
        """
        Upload multiple transactions to Notion database
        Returns number of successfully uploaded transactions
        """
        if categories is None:
            categories = ["Misc"] * len(transactions)
        
        if len(categories) != len(transactions):
            raise ValueError("Number of categories must match number of transactions")
        
        successful_uploads = 0
        
        for transaction, category in zip(transactions, categories):
            if self.upload_transaction(transaction, category):
                successful_uploads += 1
        
        print(f"\n📊 Upload Summary: {successful_uploads}/{len(transactions)} transactions uploaded successfully")
        return successful_uploads
    
    def test_connection(self) -> bool:
        """
        Test the connection to Notion API and database
        """
        try:
            # Test API connection by getting database info
            url = f"{self.base_url}/databases/{self.database_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            database_info = response.json()
            print(f"✅ Connected to Notion database: {database_info.get('title', [{}])[0].get('plain_text', 'Unknown')}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error connecting to Notion: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return False
