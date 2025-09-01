#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transaction_categorizer import TransactionCategorizer

def test_low_confidence():
    """Test with modified confidence threshold to trigger manual prompt"""
    
    # Use a very high confidence threshold to force manual categorization
    categorizer = TransactionCategorizer(confidence_threshold=0.95)
    
    test_transaction = {
        'title': 'ZARA CLOTHING STORE/ORDER#XYZ789',
        'amount': -89.99,
        'date': '2024-01-20'
    }
    
    print("🧪 Testing with high confidence threshold (0.95) to trigger manual prompt...\n")
    print(f"Transaction: {test_transaction['title']}")
    print(f"Amount: ${test_transaction['amount']}")
    print(f"Confidence threshold: {categorizer.confidence_threshold}")
    
    category = categorizer.categorize_transaction(test_transaction)
    
    print(f"\nFinal category: {category}")

if __name__ == "__main__":
    test_low_confidence()
