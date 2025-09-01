"""
Transaction class for handling RBC credit card transactions
"""

from datetime import datetime
from typing import Optional


class Transaction:
    def __init__(self, id: str, amount: float, date: datetime, title: str, location: str):
        self.id = id
        self.amount = amount
        self.date = date
        self.title = title
        self.location = location
        self.category = "Misc"  # Default category

    def set_category(self, category: str):
        """Set the transaction category"""
        self.category = category

    def to_dict(self) -> dict:
        """Convert transaction to dictionary format"""
        return {
            'id': self.id,
            'amount': self.amount,
            'date': self.date,
            'title': self.title,
            'location': self.location,
            'category': self.category
        }

    def __str__(self) -> str:
        return f"Transaction({self.title}, ${self.amount:.2f}, {self.category})"