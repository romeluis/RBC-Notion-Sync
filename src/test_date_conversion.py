#!/usr/bin/env python3
"""
Test script to verify date conversion is working correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qfx_parser import QFXParser
from datetime import datetime, timezone, timedelta

def test_date_conversion():
    print("Testing Date Conversion...")
    
    parser = QFXParser("")  # Empty path since we're just testing the method
    
    # Test cases based on the actual QFX file format
    test_cases = [
        {
            'input': '20250711120000[-5]',  # July 11, 2025 at 12:00 PM UTC-5
            'description': 'July 11 at noon UTC-5 (from QFX file)'
        },
        {
            'input': '20250711000000[-5]',  # July 11, 2025 at midnight UTC-5
            'description': 'July 11 at midnight UTC-5'
        },
        {
            'input': '20250711235959[-5]',  # July 11, 2025 at 11:59:59 PM UTC-5
            'description': 'July 11 at 11:59 PM UTC-5'
        },
        {
            'input': '20250712010000[-5]',  # July 12, 2025 at 1:00 AM UTC-5
            'description': 'July 12 at 1:00 AM UTC-5'
        }
    ]
    
    print(f"Your current timezone: {datetime.now().astimezone().tzinfo}")
    print(f"Current local time: {datetime.now()}")
    print()
    
    for test_case in test_cases:
        try:
            result = parser._parse_date(test_case['input'])
            print(f"Input: {test_case['input']}")
            print(f"Description: {test_case['description']}")
            print(f"Parsed date: {result}")
            print(f"Parsed date (formatted): {result.strftime('%Y-%m-%d %A')}")
            print()
        except Exception as e:
            print(f"Error parsing {test_case['input']}: {e}")
            print()

if __name__ == "__main__":
    test_date_conversion()
