#!/usr/bin/env python3
"""
Test script for confidence-based transaction categorizer
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transaction_categorizer import TransactionCategorizer

def test_confidence_system():
    print("🧪 Testing Confidence-Based Transaction Categorizer")
    print("=" * 60)
    
    try:
        # Create categorizer with lower confidence threshold for demo
        categorizer = TransactionCategorizer(confidence_threshold=0.8)
        
        if not categorizer.test_connection():
            print("❌ Connection failed")
            return False
        
        # Test transactions with varying confidence levels
        test_transactions = [
            {
                'title': 'PRESTO FARE/ABC123',  # Should use rule
                'location': 'TORONTO ON',
                'amount': -3.35,
                'id': 'test1'
            },
            {
                'title': 'STARBUCKS #12345',  # Should use rule
                'location': 'TORONTO ON',
                'amount': -5.50,
                'id': 'test2'
            },
            {
                'title': 'CLEARLY OBVIOUS RESTAURANT',  # High confidence AI
                'location': 'TORONTO ON',
                'amount': -25.00,
                'id': 'test3'
            },
            {
                'title': 'AMBIGUOUS STORE XYZ',  # Low confidence - should ask
                'location': 'SOMEWHERE ON',
                'amount': -15.00,
                'id': 'test4'
            },
            {
                'title': 'RANDOM MERCHANT 123',  # Low confidence - should ask
                'location': 'UNKNOWN',
                'amount': -30.00,
                'id': 'test5'
            }
        ]
        
        print(f"\n🧪 Testing with {len(test_transactions)} transactions:")
        print(f"Confidence threshold: {categorizer.confidence_threshold}")
        print("(Transactions below this threshold will ask for manual input)\n")
        
        # Note: This will prompt for user input on low-confidence items
        categories = categorizer.categorize_transactions(test_transactions)
        
        print(f"\n✅ Test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing confidence system: {e}")
        return False

if __name__ == "__main__":
    print("Note: This test may prompt you to manually categorize low-confidence transactions.")
    print("You can press Ctrl+C to skip manual input and use AI suggestions.")
    print()
    test_confidence_system()
