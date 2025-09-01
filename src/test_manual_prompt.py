#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transaction_categorizer import TransactionCategorizer

def test_manual_prompt():
    """Test with a transaction that should trigger manual categorization"""
    
    categorizer = TransactionCategorizer()
    
    # Test with a very ambiguous transaction
    test_transaction = {
        'title': 'MYSTERIOUS BUSINESS INC/PAYMENT#789',
        'amount': -123.45,
        'date': '2024-01-19'
    }
    
    print("🧪 Testing with ambiguous transaction to trigger manual prompt...\n")
    print(f"Transaction: {test_transaction['title']}")
    print(f"Amount: ${test_transaction['amount']}")
    
    category = categorizer.categorize_transaction(test_transaction)
    
    print(f"\nFinal category: {category}")
    
    # Check if the rule was added
    print("\n📋 Checking if new rule was added...")
    pattern = categorizer._extract_identifying_pattern(test_transaction['title'])
    print(f"Extracted pattern: '{pattern}'")

if __name__ == "__main__":
    test_manual_prompt()
