#!/usr/bin/env python3

"""
Test script to verify dynamic category loading works correctly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from transaction_categorizer import TransactionCategorizer

def test_dynamic_categories():
    """Test that categories are loaded dynamically from rules file"""
    
    print("🧪 Testing dynamic category loading...")
    
    # Create a test categorizer (will use default model selection)
    categorizer = TransactionCategorizer(model_name="llama3.2")
    
    print(f"\n📋 Loaded categories ({len(categorizer.categories)}):")
    for i, category in enumerate(categorizer.categories, 1):
        print(f"   {i}. {category}")
    
    print(f"\n📝 Sample rules loaded: {len(categorizer.rules)}")
    if categorizer.rules:
        # Show first 5 rules as example
        for i, (pattern, category) in enumerate(list(categorizer.rules.items())[:5]):
            print(f"   {pattern} -> {category}")
        if len(categorizer.rules) > 5:
            print(f"   ... and {len(categorizer.rules) - 5} more")
    
    # Test prompt generation with dynamic categories
    test_transaction = {
        'title': 'TEST MERCHANT',
        'location': 'Toronto, ON',
        'amount': -25.50
    }
    
    prompt = categorizer._create_categorization_prompt(test_transaction)
    print(f"\n🤖 Sample AI prompt (first 500 chars):")
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
    
    print("\n✅ Dynamic category test completed!")

if __name__ == "__main__":
    test_dynamic_categories()
