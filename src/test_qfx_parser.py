#!/usr/bin/env python3
"""
Test script for QFX parser
"""

import sys
import os
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qfx_parser import QFXParser
from test_utils import get_test_qfx_file, print_qfx_file_info

def test_qfx_parser():
    print("Testing QFX Parser...")
    
    # Print info about available QFX files
    if not print_qfx_file_info():
        return False
    
    # Get the first available QFX file
    qfx_file = get_test_qfx_file()
    if not qfx_file:
        print("❌ No QFX files found")
        return False
    
    print(f"Using file: {qfx_file.name}")
    
    # Create parser instance
    parser = QFXParser(str(qfx_file))
    
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
