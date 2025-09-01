# RBC-Notion-Sync Instructions

## Project Overview
A Python script to parse RBC credit card transaction data from QFX files and upload to a Notion database with AI-powered categorization.

## Requirements
1. Parse QFX files from RBC-Notion-Sync/input directory
2. Filter out CREDIT transactions (keep only DEBIT purchases)
3. Upload transactions to Notion database with specific schema
4. Use Ollama LLM to categorize transactions

## Notion Database Schema
- **ID** (text): Transaction ID from QFX (FITID)
- **Transaction Title** (text): NAME from QFX
- **Location** (text): MEMO from QFX  
- **Date** (datetime): DTPOSTED from QFX
- **Amount (CAD$)** (number): TRNAMT from QFX (negative values)
- **Transaction Category** (select): LLM-determined category

## Transaction Categories
- **Partying**: Alcohol/club/bar (LCBO, Fifth Social Club, Track & Field, etc.)
- **Groceries**: Standard options (Loblaws, Whole Foods, Metro)
- **Misc**: Anything not in other categories
- **Transportation**: TTC, Go Transit, Uber, etc.
- **Cafe**: Coffee shops and cafes for work
- **Eating Out**: Restaurants and fast food
- **Subscription**: Recurring bills (Equinox, Freedom Mobile, Disney+, ClassPass, Apple One ~$50)

## QFX File Structure
- OFX format with STMTTRN blocks containing transaction data
- TRNTYPE: CREDIT (payments) or DEBIT (purchases) - filter for DEBIT only
- FITID: Unique transaction ID
- NAME: Merchant name
- MEMO: Location/additional info
- DTPOSTED: Transaction date
- TRNAMT: Amount (negative for purchases)

## Environment Variables
- NOTION_API_KEY: Notion integration API key
- NOTION_DATABASE_ID: Target database ID

## Implementation Steps
1. QFX file parsing
2. Notion API integration
3. Ollama LLM setup for categorization
4. Complete integration and testing
