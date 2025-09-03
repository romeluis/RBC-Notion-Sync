"""
QFX File Parser for RBC Credit Card Transactions
Parses OFX/QFX files and extracts transaction data using regex-based parsing
"""

import re
from datetime import datetime, timezone, timedelta
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
        
        Applies timezone conversion and adds 1 day to correct QFX date discrepancy.
        RBC QFX files consistently show dates 1 day behind the actual transaction dates
        visible in the banking interface.
        """
        date_str = date_str.strip()
        
        # Extract timezone offset if present
        timezone_offset = 0
        timezone_match = re.search(r'\[([+-]?\d+)\]', date_str)
        if timezone_match:
            timezone_offset = int(timezone_match.group(1))
        
        # Remove timezone info
        date_str = re.sub(r'\[.*\]', '', date_str)
        
        # Parse the date and time
        if len(date_str) >= 8:
            # Extract date part (YYYYMMDD)
            date_part = date_str[:8]
            
            # Extract time part if available (HHMMSS)
            time_part = "000000"  # default to midnight
            if len(date_str) >= 14:
                time_part = date_str[8:14]
            elif len(date_str) >= 12:
                time_part = date_str[8:12] + "00"  # HHMM -> HHMMSS
            elif len(date_str) >= 10:
                time_part = date_str[8:10] + "0000"  # HH -> HHMMSS
            
            # Parse datetime
            datetime_str = date_part + time_part
            dt = datetime.strptime(datetime_str, '%Y%m%d%H%M%S')
            
            # Apply timezone offset to get the correct local date
            if timezone_offset != 0:
                tz = timezone(timedelta(hours=timezone_offset))
                dt = dt.replace(tzinfo=tz)
                # Convert to local time to get the correct date
                dt = dt.astimezone()
            
            # Create date at midnight in local timezone
            local_date = datetime(dt.year, dt.month, dt.day)
            
            # Add one day to correct QFX date discrepancy
            # (QFX dates are consistently 1 day behind banking interface)
            corrected_date = local_date + timedelta(days=1)
            
            return corrected_date
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
