# 💳 RBC-Notion-Sync

> **Intelligent QFX Transaction Parser & Notion Database Sync**

Transform your RBC credit card transactions from QFX files into a beautifully organized Notion database with AI-powered categorization and smart rule-based matching.

![Python](https://img.shields.io/badge/python-v3.13+-blue.svg)
![Notion API](https://img.shields.io/badge/notion-api-black.svg)
![Ollama](https://img.shields.io/badge/ollama-llama3.2-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🔍 **Smart QFX Parsing** - Extracts DEBIT transactions from RBC QFX files
- 🧠 **Hybrid AI Categorization** - Rule-based + AI-powered classification
- 📊 **Notion Integration** - Seamless database sync with duplicate protection
- 🎯 **Interactive Model Selection** - Choose your preferred Ollama model
- ⚡ **Pattern Learning** - Automatically adds new rules from manual categorizations
- 🛡️ **Duplicate Prevention** - Smart transaction ID checking
- 📈 **Confidence Scoring** - AI provides confidence levels for uncertain categorizations

## 🎬 Demo

```bash
🔍 Found QFX file: /input/rbc_transactions.qfx
📊 Parsed 120 transactions from QFX file

🧠 Categorizing transactions...
📋 Rule-based: PRESTO FARE -> Transportation ✅
🤖 AI (85% confidence): MYSTERIOUS CAFE -> Cafe ✅
❓ Manual needed: UNKNOWN STORE (confidence: 65%)
   Select category: 1-11 or type custom:

📤 Uploading to Notion...
✅ 118 new transactions uploaded (2 duplicates skipped)
```

## � Quick Start

### Prerequisites

- Python 3.13+
- [Ollama](https://ollama.com) with llama3.2 model
- Notion workspace with API access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/RBC-Notion-Sync.git
   cd RBC-Notion-Sync
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv .
   source bin/activate  # On Windows: Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install and configure Ollama**
   ```bash
   # Install Ollama (macOS)
   brew install ollama
   
   # Start Ollama service
   ollama serve
   
   # Download AI model (in another terminal)
   ollama pull llama3.2
   ```

### Configuration

1. **Create Notion Integration**
   - Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
   - Create new integration: "RBC Transaction Sync"
   - Copy the integration token

2. **Set up Notion Database**
   Create a database with these properties:
   - **ID** (Text) - Primary key
   - **Transaction Title** (Title)
   - **Location** (Text)
   - **Date** (Date)
   - **Amount** (Number)
   - **Transaction Category** (Select) with options:
     - Transportation, Groceries, Eating Out, Cafe
     - Subscription, Partying, Clothing, Technology
     - Events, Vanity, Misc

3. **Share database with integration** and copy the database ID

4. **Set environment variables**
   ```bash
   export NOTION_API_KEY="your_integration_token"
   export NOTION_DATABASE_ID="your_database_id"
   ```

### Usage

1. **Place QFX files** in the `input/` directory
2. **Run the application**
   ```bash
   cd src
   python main.py
   ```
3. **Follow interactive prompts** for model selection and manual categorization

## 🏗️ Architecture

```
RBC-Notion-Sync/
├── src/
│   ├── main.py                 # Main orchestration
│   ├── qfx_parser.py          # QFX file parsing
│   ├── notion_client.py       # Notion API integration
│   └── transaction_categorizer.py  # AI + rule categorization
├── input/                     # Place QFX files here
├── transaction_rules.txt      # Categorization rules (100+ patterns)
└── requirements.txt          # Python dependencies
```

## 🧠 Intelligent Categorization System

### Three-Tier Categorization

1. **🎯 Rule-Based (Fastest)**
   ```
   PRESTO FARE -> Transportation
   STARBUCKS -> Cafe
   METRO -> Groceries
   ```

2. **🤖 AI-Powered (Smart)**
   - Uses Ollama LLM for unknown merchants
   - Provides confidence scores (0-100%)
   - Context-aware categorization

3. **👤 Human-in-the-Loop (Learning)**
   - Manual categorization for low-confidence transactions
   - Automatically extracts identifying patterns
   - Adds new rules to `transaction_rules.txt`

### Smart Pattern Extraction

The AI intelligently removes variable parts from transaction titles:

```
Input:  "PRESTO FARE/PKF123ABC"  → Output: "PRESTO FARE"
Input:  "AMAZON*4X5HZ3583"       → Output: "AMAZON"
Input:  "SUBWAY #40569 TORONTO"  → Output: "SUBWAY TORONTO"
```

## � Supported Categories

| Category | Examples |
|----------|----------|
| 🚇 **Transportation** | TTC, Presto, Uber, Go Transit |
| 🛒 **Groceries** | Metro, Loblaws, Whole Foods |
| 🍽️ **Eating Out** | Restaurants, McDonald's, Subway |
| ☕ **Cafe** | Starbucks, Tim Hortons, Coffee shops |
| 📱 **Subscription** | Netflix, Spotify, Apple, Rogers |
| 🍺 **Partying** | LCBO, Bars, Clubs |
| 👗 **Clothing** | Zara, H&M, Uniqlo |
| 💻 **Technology** | Apple Store, Best Buy, AliExpress |
| 🎭 **Events** | Eventbrite, Concerts, Theatre |
| 💄 **Vanity** | Sephora, Salons, Beauty products |
| 📦 **Misc** | Everything else |

## 🛠️ Advanced Configuration

### Custom Categories

Add new categories by editing `transaction_categorizer.py`:

```python
self.categories = [
    "Your_Custom_Category",
    # ... existing categories
]
```

### Custom Rules

Edit `transaction_rules.txt`:

```
YOUR_MERCHANT -> Your_Custom_Category
SPECIFIC_PATTERN -> Existing_Category
```

### Confidence Threshold

Adjust AI confidence threshold:

```python
categorizer = TransactionCategorizer(confidence_threshold=0.8)  # Default: 0.7
```

## 🧪 Testing

```bash
# Test individual components
python test_qfx_parser.py
python test_notion_client.py
python test_transaction_categorizer.py

# Test full integration
python test_full_integration.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Ollama connection failed** | Ensure `ollama serve` is running |
| **Model not found** | Run `ollama pull llama3.2` |
| **Notion 400 error** | Check API key and database schema |
| **No transactions found** | Verify QFX files in `input/` directory |
| **Duplicate uploads** | Check transaction ID format |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.com) for local LLM inference
- [Notion API](https://developers.notion.com) for database integration
- [RBC Bank](https://www.rbc.com) for QFX format support

## ⭐ Star History

If this project helped you, please consider giving it a star! ⭐

---

**Built with ❤️ for better financial tracking**
