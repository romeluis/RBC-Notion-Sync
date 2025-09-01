"""
QFX File Parser for RBC Credit Card Transactions
Parses OFX/QFX files and extracts transaction data using regex-based parsing
"""

import re
from datetime import datetime
from typing import List, Dict, Optional


class QFXParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.raw_content = ""
        self.transactions = []
    
    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse OFX date format: YYYYMMDDHHMMSS[timezone]
        Example: 20250711120000[-5]
        """
        # Remove timezone info if present
        date_str = re.sub(r'\[.*\]', '', date_str.strip())
        
        # Parse the date
        if len(date_str) >= 8:
            # Take first 8 characters for YYYYMMDD
            date_part = date_str[:8]
            return datetime.strptime(date_part, '%Y%m%d')
        else:
            raise ValueError(f"Invalid date format: {date_str}")
    
    def _extract_field_value(self, content: str, field_name: str) -> str:
        """
        Extract field value from OFX content using regex
        """
        pattern = f'<{field_name}>([^<\n]+)'
        match = re.search(pattern, content)
        return match.group(1).strip() if match else ""
    
    def parse_file(self) -> List[Dict]:
        """
        Parse the QFX file and extract transaction data using regex
        Returns list of transaction dictionaries
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.raw_content = file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(self.file_path, 'r', encoding='latin-1') as file:
                self.raw_content = file.read()
        
        # Find all STMTTRN blocks using regex
        stmttrn_pattern = r'<STMTTRN>(.*?)</STMTTRN>'
        stmttrn_matches = re.findall(stmttrn_pattern, self.raw_content, re.DOTALL)
        
        transactions = []
        
        for stmttrn_content in stmttrn_matches:
            # Extract transaction type first
            trntype = self._extract_field_value(stmttrn_content, 'TRNTYPE')
            
            # Only process DEBIT transactions (purchases, not payments)
            if trntype == 'DEBIT':
                # Extract other fields
                fitid = self._extract_field_value(stmttrn_content, 'FITID')
                dtposted = self._extract_field_value(stmttrn_content, 'DTPOSTED')
                trnamt = self._extract_field_value(stmttrn_content, 'TRNAMT')
                name = self._extract_field_value(stmttrn_content, 'NAME')
                memo = self._extract_field_value(stmttrn_content, 'MEMO')
                
                try:
                    transaction_data = {
                        'id': fitid,
                        'type': trntype,
                        'date': self._parse_date(dtposted) if dtposted else None,
                        'amount': float(trnamt) if trnamt else 0.0,
                        'title': name,
                        'location': memo
                    }
                    
                    transactions.append(transaction_data)
                    
                except (ValueError, Exception) as e:
                    print(f"Warning: Could not parse transaction: {e}")
                    continue
        
        self.transactions = transactions
        return transactions
    
    def get_transaction_count(self) -> int:
        """Return the number of parsed transactions"""
        return len(self.transactions)
    
    def print_summary(self):
        """Print a summary of parsed transactions"""
        print(f"Parsed {len(self.transactions)} DEBIT transactions")
        if self.transactions:
            valid_dates = [t['date'] for t in self.transactions if t['date']]
            if valid_dates:
                print(f"Date range: {min(valid_dates)} to {max(valid_dates)}")
            total_amount = sum(t['amount'] for t in self.transactions)
            print(f"Total amount: ${total_amount:.2f}")
