#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transaction_categorizer import TransactionCategorizer

def test_full_workflow():
    """Test the complete workflow with rule extraction and addition"""
    
    categorizer = TransactionCategorizer()
    
    # Test with a transaction that should trigger manual categorization
    test_transaction = {
        'title': 'CANADIAN TIRE #1234/GAS STATION',
        'amount': -45.67,
        'date': '2024-01-18'
    }
    
    print("🧪 Testing complete workflow with a new merchant...\n")
    print(f"Transaction: {test_transaction['title']}")
    print(f"Amount: ${test_transaction['amount']}")
    
    # This should trigger manual categorization since it's not in rules
    category = categorizer.categorize_transaction(test_transaction)
    
    print(f"\nFinal category: {category}")

if __name__ == "__main__":
    test_full_workflow()
