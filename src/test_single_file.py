#!/usr/bin/env python3

"""
Test script to verify the single-file approach for category descriptions
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from transaction_categorizer import TransactionCategorizer

def test_single_file_descriptions():
    """Test that descriptions are loaded from transaction_rules.txt"""
    
    print("🧪 Testing single-file category descriptions...")
    
    # Create a test categorizer (will use default model selection)
    categorizer = TransactionCategorizer(model_name="llama3.2")
    
    print(f"\n📋 Loaded categories with descriptions ({len(categorizer.categories)}):")
    for i, category in enumerate(categorizer.categories, 1):
        description = categorizer.category_descriptions.get(category, "No description")
        print(f"   {i}. {category} - {description}")
    
    print(f"\n📝 Sample rules loaded: {len(categorizer.rules)}")
    if categorizer.rules:
        # Show first 5 rules as example
        for i, (pattern, category) in enumerate(list(categorizer.rules.items())[:5]):
            print(f"   {pattern} -> {category}")
        if len(categorizer.rules) > 5:
            print(f"   ... and {len(categorizer.rules) - 5} more")
    
    # Test prompt generation with dynamic categories
    test_transaction = {
        'title': 'UNKNOWN MERCHANT',
        'location': 'Toronto, ON',
        'amount': -25.50
    }
    
    prompt = categorizer._create_categorization_prompt(test_transaction)
    print(f"\n🤖 Sample AI prompt with descriptions:")
    print("=" * 80)
    print(prompt[:800] + "..." if len(prompt) > 800 else prompt)
    print("=" * 80)
    
    print("\n✅ Single-file category descriptions test completed!")

if __name__ == "__main__":
    test_single_file_descriptions()
