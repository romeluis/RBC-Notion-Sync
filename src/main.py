#!/usr/bin/env python3
"""
RBC-Notion-Sync: Main application
Parses RBC credit card QFX files, categorizes transactions with AI, and uploads to Notion
"""

import os
import sys
from pathlib import Path
from typing import List

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

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qfx_parser import QFXParser
from notion_client import NotionClient
from transaction_categorizer import TransactionCategorizer
from Transaction import Transaction


class RBCNotionSync:
    def __init__(self):
        self.qfx_parser = None
        self.notion_client = None
        self.categorizer = None
        self.transactions = []
        
        # Set up input directory
        self.input_dir = Path(__file__).parent.parent / "input"
        
    def setup_clients(self):
        """Initialize all client connections"""
        print("🔧 Setting up clients...")
        
        # Initialize Notion client
        try:
            self.notion_client = NotionClient()
            if not self.notion_client.test_connection():
                print("❌ Notion connection failed")
                return False
        except Exception as e:
            print(f"❌ Error setting up Notion client: {e}")
            return False
        
        # Initialize transaction categorizer
        try:
            self.categorizer = TransactionCategorizer()
            if not self.categorizer.test_connection():
                print("❌ Ollama connection failed")
                return False
        except Exception as e:
            print(f"❌ Error setting up transaction categorizer: {e}")
            return False
        
        print("✅ All clients set up successfully")
        return True
    
    def find_qfx_files(self) -> List[Path]:
        """Find all QFX files in the input directory"""
        qfx_files = list(self.input_dir.glob("*.qfx"))
        qfx_files.extend(list(self.input_dir.glob("*.QFX")))
        return qfx_files
    
    def parse_qfx_file(self, file_path: Path) -> List[dict]:
        """Parse a QFX file and return transactions"""
        print(f"📁 Parsing QFX file: {file_path.name}")
        
        parser = QFXParser(str(file_path))
        transactions = parser.parse_file()
        
        parser.print_summary()
        return transactions
    
    def categorize_transactions(self, transactions: List[dict]) -> List[str]:
        """Categorize transactions using AI"""
        print(f"\n🤖 Categorizing {len(transactions)} transactions...")
        return self.categorizer.categorize_transactions(transactions)
    
    def upload_to_notion(self, transactions: List[dict], categories: List[str]) -> int:
        """Upload transactions to Notion database"""
        print(f"\n📤 Uploading {len(transactions)} transactions to Notion...")
        return self.notion_client.upload_transactions(transactions, categories)
    
    def process_single_file(self, file_path: Path):
        """Process a single QFX file"""
        print(f"\n{'='*60}")
        print(f"Processing: {file_path.name}")
        print(f"{'='*60}")
        
        # Parse QFX file
        transactions = self.parse_qfx_file(file_path)
        
        if not transactions:
            print("❌ No transactions found in file")
            return
        
        # Categorize transactions
        categories = self.categorize_transactions(transactions)
        
        # Upload to Notion
        uploaded_count = self.upload_to_notion(transactions, categories)
        
        print(f"\n✅ Processed {file_path.name}: {uploaded_count}/{len(transactions)} transactions uploaded")
    
    def run(self):
        """Main execution function"""
        print("🚀 Starting RBC-Notion-Sync")
        print(f"Input directory: {self.input_dir}")
        
        # Check if input directory exists
        if not self.input_dir.exists():
            print(f"❌ Input directory does not exist: {self.input_dir}")
            return
        
        # Find QFX files
        qfx_files = self.find_qfx_files()
        
        if not qfx_files:
            print(f"❌ No QFX files found in {self.input_dir}")
            return
        
        print(f"📂 Found {len(qfx_files)} QFX file(s):")
        for file in qfx_files:
            print(f"   - {file.name}")
        
        # Setup clients
        if not self.setup_clients():
            print("❌ Failed to setup clients. Please check your configuration.")
            return
        
        # Process each file
        total_processed = 0
        for qfx_file in qfx_files:
            try:
                self.process_single_file(qfx_file)
                total_processed += 1
            except Exception as e:
                print(f"❌ Error processing {qfx_file.name}: {e}")
                continue
        
        print(f"\n🎉 Sync completed! Processed {total_processed}/{len(qfx_files)} files")


def main():
    """Entry point for the application"""
    try:
        sync = RBCNotionSync()
        sync.run()
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()