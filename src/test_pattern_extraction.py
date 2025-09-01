#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transaction_categorizer import TransactionCategorizer

def test_pattern_extraction():
    """Test the AI pattern extraction and rule addition"""
    
    categorizer = TransactionCategorizer()
    
    test_transactions = [
        {
            'title': 'PRESTO FARE/PKF123ABC',
            'amount': -5.50,
            'date': '2024-01-15'
        },
        {
            'title': 'AMAZON*4X5HZ3583',
            'amount': -29.99,
            'date': '2024-01-16'
        },
        {
            'title': 'SUBWAY #40569 TORONTO',
            'amount': -12.50,
            'date': '2024-01-17'
        }
    ]
    
    print("🧪 Testing pattern extraction and rule addition...\n")
    
    for i, transaction in enumerate(test_transactions, 1):
        print(f"Transaction {i}: {transaction['title']}")
        
        # Test pattern extraction
        pattern = categorizer._extract_identifying_pattern(transaction['title'])
        print(f"Extracted pattern: '{pattern}'")
        
        # Simulate manual categorization to test rule addition
        print("\nSimulating manual categorization (for testing rule addition)...")
        
        if i == 1:  # PRESTO
            print("Manual category: Transportation")
            categorizer._add_rule_to_file(pattern, "Transportation")
        elif i == 2:  # AMAZON
            print("Manual category: Misc")
            categorizer._add_rule_to_file(pattern, "Misc")
        elif i == 3:  # SUBWAY
            print("Manual category: Eating Out")
            categorizer._add_rule_to_file(pattern, "Eating Out")
        
        print("-" * 50)

if __name__ == "__main__":
    test_pattern_extraction()
