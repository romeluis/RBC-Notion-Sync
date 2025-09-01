#!/usr/bin/env python3

"""
Test script to verify category descriptions functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from transaction_categorizer import TransactionCategorizer

def test_category_descriptions():
    """Test that category descriptions are loaded and used correctly"""
    
    print("🧪 Testing category descriptions...")
    
    # Create a test categorizer (will use default model selection)
    categorizer = TransactionCategorizer(model_name="llama3.2")
    
    print(f"\n📋 Loaded categories with descriptions ({len(categorizer.categories)}):")
    for i, category in enumerate(categorizer.categories, 1):
        description = categorizer.category_descriptions.get(category, "No description")
        print(f"   {i}. {category} - {description}")
    
    # Test prompt generation with descriptions
    test_transaction = {
        'title': 'STARBUCKS COFFEE',
        'location': 'Toronto, ON',
        'amount': -5.75
    }
    
    prompt = categorizer._create_categorization_prompt(test_transaction)
    print(f"\n🤖 Sample AI prompt with descriptions:")
    print("=" * 80)
    print(prompt[:1000] + "..." if len(prompt) > 1000 else prompt)
    print("=" * 80)
    
    print("\n✅ Category descriptions test completed!")
    print("\n💡 To test manual categorization with descriptions, run the main script")

if __name__ == "__main__":
    test_category_descriptions()
