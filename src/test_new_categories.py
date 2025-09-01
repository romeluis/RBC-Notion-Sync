#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transaction_categorizer import TransactionCategorizer

def test_new_categories():
    """Test the new categories"""
    
    categorizer = TransactionCategorizer()
    
    test_transactions = [
        {'title': 'SEPHORA CANADA', 'amount': -75.99, 'date': '2024-01-20'},
        {'title': 'APPLE STORE EATON CENTRE', 'amount': -1299.00, 'date': '2024-01-21'},
        {'title': 'EVENTBRITE/CONCERT TICKET', 'amount': -89.50, 'date': '2024-01-22'},
        {'title': 'ZARA YORKDALE', 'amount': -129.99, 'date': '2024-01-23'}
    ]
    
    print("🧪 Testing new categories...\n")
    
    for transaction in test_transactions:
        print(f"📝 {transaction['title']}")
        category = categorizer.categorize_transaction(transaction)
        print(f"   → {category}\n")

if __name__ == "__main__":
    test_new_categories()
