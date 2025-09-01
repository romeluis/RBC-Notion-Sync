#!/usr/bin/env python3
"""
Test script for transaction categorizer
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transaction_categorizer import TransactionCategorizer

def test_transaction_categorizer():
    print("Testing Transaction Categorizer...")
    
    try:
        # Create categorizer
        categorizer = TransactionCategorizer()
        
        # Test connection to Ollama
        if not categorizer.test_connection():
            print("\n⚠️  Ollama connection failed")
            print("Make sure:")
            print("1. Ollama is installed")
            print("2. Ollama is running (ollama serve)")
            print("3. The llama3.2 model is installed (ollama pull llama3.2)")
            return False
        
        # Test with sample transactions (mix of rule-based and AI-needed)
        test_transactions = [
            {
                'title': 'PRESTO FARE/PKFTKC9DZC',  # Should be Transportation (rule)
                'location': 'TORONTO ON',
                'amount': -3.35,
                'id': 'test1'
            },
            {
                'title': 'METRO 742',  # Should be Groceries (rule)
                'location': 'TORONTO ON',
                'amount': -25.80,
                'id': 'test2'
            },
            {
                'title': 'TST-Mandys - Yorkvill',  # Should be Eating Out (rule)
                'location': 'TORONTO ON',
                'amount': -15.50,
                'id': 'test3'
            },
            {
                'title': 'ARTLY.COFFEE',  # Should be Cafe (rule)
                'location': 'VANCOUVER BC',
                'amount': -15.42,
                'id': 'test4'
            },
            {
                'title': 'UNKNOWN MERCHANT',  # Should use AI
                'location': 'TORONTO ON',
                'amount': -50.00,
                'id': 'test5'
            },
            {
                'title': 'WEIRD PLACE 123',  # Should use AI
                'location': 'TORONTO ON',
                'amount': -25.00,
                'id': 'test6'
            }
        ]
        
        print(f"\n🧪 Testing with {len(test_transactions)} sample transactions:")
        
        categories = categorizer.categorize_transactions(test_transactions)
        
        print(f"\n✅ Categorization completed successfully")
        print(f"Results: {dict(zip([t['title'] for t in test_transactions], categories))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing transaction categorizer: {e}")
        return False

if __name__ == "__main__":
    test_transaction_categorizer()
