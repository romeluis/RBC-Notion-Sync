#!/usr/bin/env python3
"""
Test script for QFX parser
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qfx_parser import QFXParser

def test_qfx_parser():
    # Path to the QFX file
    qfx_file = "/Users/romeluis/Library/Mobile Documents/com~apple~CloudDocs/Scripts/RBC-Notion-Sync/input/ofx32499.qfx"
    
    print("Testing QFX Parser...")
    print(f"File: {qfx_file}")
    
    # Create parser instance
    parser = QFXParser(qfx_file)
    
    # Parse the file
    try:
        transactions = parser.parse_file()
        
        print(f"\n✅ Successfully parsed {len(transactions)} transactions")
        
        # Print summary
        parser.print_summary()
        
        # Show first few transactions
        print("\n📋 First 5 transactions:")
        for i, transaction in enumerate(transactions[:5]):
            print(f"\n{i+1}. {transaction['title']}")
            print(f"   ID: {transaction['id']}")
            print(f"   Date: {transaction['date']}")
            print(f"   Amount: ${transaction['amount']:.2f}")
            print(f"   Location: {transaction['location']}")
        
        if len(transactions) > 5:
            print(f"\n... and {len(transactions) - 5} more transactions")
            
        return True
        
    except Exception as e:
        print(f"❌ Error parsing QFX file: {e}")
        return False

if __name__ == "__main__":
    test_qfx_parser()
