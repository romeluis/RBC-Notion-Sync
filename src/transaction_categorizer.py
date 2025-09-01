"""
LLM client for transaction categorization using Ollama
Enhanced with rule-based categorization for known patterns
"""

import ollama
from typing import List, Dict, Optional
from pathlib import Path
import re


class TransactionCategorizer:
    def __init__(self, model_name: Optional[str] = None, confidence_threshold: float = 0.7):
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold  # Threshold for auto-categorization
        # Default categories - will be extended with categories from rules file
        self.default_categories = [
            "Partying",      # Alcohol/club/bar (LCBO, Fifth Social Club, Track & Field, etc.)
            "Groceries",     # Standard options (Loblaws, Whole Foods, Metro)
            "Misc",          # Anything not in other categories
            "Transportation", # TTC, Go Transit, Uber, etc.
            "Cafe",          # Coffee shops and cafes for work
            "Eating Out",    # Restaurants and fast food
            "Subscription",  # Recurring bills (Equinox, Freedom Mobile, Disney+, ClassPass, Apple One ~$50)
            "Clothing",      # Clothing stores and fashion (Zara, H&M, etc.)
            "Technology",    # Tech purchases (Apple, Best Buy, AliExpress, etc.)
            "Events",        # Event tickets and entertainment (Eventbrite, concerts, etc.)
            "Vanity"         # Beauty, grooming, personal care (Sephora, barber shops, etc.)
        ]
        
        # Load rules and dynamically discover categories
        self.rules, self.category_descriptions = self._load_categorization_rules()
        self.categories = self._get_all_categories()
        
        # If no model specified, prompt user to select one
        if not self.model_name:
            self.model_name = self._select_model_interactive()
    
    def _load_categorization_rules(self) -> tuple[Dict[str, str], Dict[str, str]]:
        """
        Load categorization rules and descriptions from the rules file
        Returns (rules_dict, descriptions_dict)
        """
        rules = {}
        descriptions = {}
        rules_file = Path(__file__).parent.parent / "transaction_rules.txt"
        
        # Default descriptions for built-in categories
        default_descriptions = {
            "Partying": "Alcohol purchases, bars, clubs, nightlife activities",
            "Groceries": "Food shopping, supermarkets, farmers markets, meal ingredients",
            "Misc": "Anything that doesn't fit other categories",
            "Transportation": "Public transit, rideshare, gas, parking, car maintenance",
            "Cafe": "Coffee shops, cafes, places for work or casual meetings",
            "Eating Out": "Restaurants, fast food, takeout, dining experiences",
            "Subscription": "Recurring bills and subscriptions (streaming, gym, phone, etc.)",
            "Clothing": "Clothing stores, fashion, apparel, shoes, accessories",
            "Technology": "Tech purchases, electronics, software, gadgets",
            "Events": "Event tickets, entertainment, concerts, shows, activities",
            "Vanity": "Beauty, grooming, personal care, cosmetics, spa treatments"
        }
        
        # Start with default descriptions
        descriptions.update(default_descriptions)
        
        try:
            if rules_file.exists():
                with open(rules_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        
                        # Skip empty lines
                        if not line:
                            continue
                        
                        # Parse category description: "# CATEGORY_DESC: CategoryName | Description"
                        if line.startswith('# CATEGORY_DESC:'):
                            desc_part = line.replace('# CATEGORY_DESC:', '').strip()
                            if ' | ' in desc_part:
                                category, description = desc_part.split(' | ', 1)
                                category = category.strip()
                                description = description.strip()
                                
                                if category and description:
                                    descriptions[category] = description
                            else:
                                print(f"Warning: Invalid description format on line {line_num}: {line}")
                            continue
                        
                        # Skip other comments
                        if line.startswith('#'):
                            continue
                        
                        # Parse rule: "SEARCH_STRING -> CATEGORY"
                        if ' -> ' in line:
                            search_string, category = line.split(' -> ', 1)
                            search_string = search_string.strip()
                            category = category.strip()
                            
                            if search_string and category:
                                rules[search_string.upper()] = category
                        else:
                            print(f"Warning: Invalid rule format on line {line_num}: {line}")
                
                print(f"📋 Loaded {len(rules)} categorization rules")
                custom_desc_count = len([k for k in descriptions.keys() if k not in default_descriptions])
                if custom_desc_count > 0:
                    print(f"📝 Loaded {custom_desc_count} custom category descriptions")
            else:
                print(f"⚠️  Rules file not found: {rules_file}")
                
        except Exception as e:
            print(f"❌ Error loading rules: {e}")
        
        return rules, descriptions
    
    def _save_category_description(self, category: str, description: str):
        """
        Save a category description to the transaction_rules.txt file
        """
        rules_file = Path(__file__).parent.parent / "transaction_rules.txt"
        
        try:
            # Check if description already exists
            description_line = f"# CATEGORY_DESC: {category} | {description}"
            existing_descriptions = set()
            
            if rules_file.exists():
                with open(rules_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check if this category description already exists
                for line in content.split('\n'):
                    if line.startswith('# CATEGORY_DESC:'):
                        desc_part = line.replace('# CATEGORY_DESC:', '').strip()
                        if ' | ' in desc_part:
                            cat, _ = desc_part.split(' | ', 1)
                            existing_descriptions.add(cat.strip())
                
                # If category description doesn't exist, append it
                if category not in existing_descriptions:
                    with open(rules_file, 'a', encoding='utf-8') as f:
                        f.write(f"\n{description_line}\n")
                    print(f"✅ Saved description for '{category}' to {rules_file.name}")
                else:
                    print(f"ℹ️  Description for '{category}' already exists in {rules_file.name}")
            
        except Exception as e:
            print(f"❌ Error saving category description: {e}")
    
    def _get_all_categories(self) -> List[str]:
        """
        Get all categories from default categories plus any new ones from rules file
        """
        # Start with default categories
        all_categories = set(self.default_categories)
        
        # Add any categories found in rules that aren't in defaults
        for category in self.rules.values():
            all_categories.add(category)
        
        # Convert back to sorted list, putting default categories first
        categories_list = []
        for cat in self.default_categories:
            if cat in all_categories:
                categories_list.append(cat)
                all_categories.remove(cat)
        
        # Add any new categories at the end
        categories_list.extend(sorted(all_categories))
        
        return categories_list
    
    def _apply_rules(self, transaction: Dict) -> Optional[str]:
        """
        Apply rule-based categorization
        Returns category if a rule matches, None otherwise
        """
        transaction_title = transaction['title'].upper()
        
        # Check each rule
        for search_string, category in self.rules.items():
            if search_string in transaction_title:
                return category
        
        return None
    
    def _parse_ai_response(self, response_text: str) -> tuple[str, float]:
        """
        Parse AI response to extract category and confidence
        Returns (category, confidence)
        """
        category = "Misc"
        confidence = 0.5  # Default low confidence
        
        lines = response_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('Category:'):
                category_part = line.replace('Category:', '').strip()
                if category_part in self.categories:
                    category = category_part
            elif line.startswith('Confidence:'):
                confidence_part = line.replace('Confidence:', '').strip()
                try:
                    confidence = float(confidence_part)
                    confidence = max(0.0, min(1.0, confidence))  # Clamp to 0-1
                except ValueError:
                    confidence = 0.5
        
        return category, confidence
    
    def _ask_user_for_category(self, transaction: Dict, ai_category: str, ai_confidence: float) -> str:
        """
        Ask user to manually categorize a transaction when AI confidence is low
        """
        print(f"\n❓ Low confidence categorization for:")
        print(f"   Transaction: {transaction['title']}")
        print(f"   Location: {transaction['location']}")
        print(f"   Amount: ${abs(transaction['amount']):.2f}")
        print(f"   AI suggestion: {ai_category} (confidence: {ai_confidence:.2f})")
        
        print(f"\n📋 Available categories:")
        for i, category in enumerate(self.categories, 1):
            description = self.category_descriptions.get(category, "Custom category")
            print(f"   {i}. {category} - {description}")
        print(f"   {len(self.categories) + 1}. Type custom category")
        
        while True:
            choice = ""
            try:
                choice = input(f"\nSelect category (1-{len(self.categories) + 1}) or press Enter to use AI suggestion: ").strip()
                
                if not choice:
                    # User accepts AI suggestion
                    print(f"Using AI suggestion: {ai_category}")
                    return ai_category
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.categories):
                    selected_category = self.categories[choice_num - 1]
                    print(f"Selected: {selected_category}")
                    
                    # Ask if they want to add this as a rule
                    add_rule = input(f"Add '{transaction['title']}' -> '{selected_category}' as a rule? (y/N): ").strip().lower()
                    if add_rule == 'y':
                        self._suggest_new_rule(transaction['title'], selected_category)
                    
                    return selected_category
                elif choice_num == len(self.categories) + 1:
                    # User wants to type a custom category
                    custom_category = input("Enter custom category name: ").strip()
                    if custom_category:
                        print(f"Selected custom category: {custom_category}")
                        
                        # Add to our categories list for this session
                        if custom_category not in self.categories:
                            self.categories.append(custom_category)
                            
                            # Ask for description if not already defined
                            if custom_category not in self.category_descriptions:
                                description = input(f"Enter description for '{custom_category}' (optional): ").strip()
                                if description:
                                    self.category_descriptions[custom_category] = description
                                    # Ask if they want to save this description
                                    save_desc = input(f"Save this description to category_descriptions.txt? (y/N): ").strip().lower()
                                    if save_desc == 'y':
                                        self._save_category_description(custom_category, description)
                                else:
                                    self.category_descriptions[custom_category] = "Custom category"
                        
                        # Ask if they want to add this as a rule
                        add_rule = input(f"Add '{transaction['title']}' -> '{custom_category}' as a rule? (y/N): ").strip().lower()
                        if add_rule == 'y':
                            self._suggest_new_rule(transaction['title'], custom_category)
                        
                        return custom_category
                    else:
                        print("Category name cannot be empty")
                else:
                    print(f"Please enter a number between 1 and {len(self.categories) + 1}")
                    
            except ValueError:
                # Check if user typed text instead of number (might be a category name)
                if choice and choice.strip():
                    # Treat as custom category input
                    custom_category = choice.strip()
                    print(f"Selected custom category: {custom_category}")
                    
                    # Add to our categories list for this session
                    if custom_category not in self.categories:
                        self.categories.append(custom_category)
                        
                        # Ask for description if not already defined
                        if custom_category not in self.category_descriptions:
                            description = input(f"Enter description for '{custom_category}' (optional): ").strip()
                            if description:
                                self.category_descriptions[custom_category] = description
                                # Ask if they want to save this description
                                save_desc = input(f"Save this description to category_descriptions.txt? (y/N): ").strip().lower()
                                if save_desc == 'y':
                                    self._save_category_description(custom_category, description)
                            else:
                                self.category_descriptions[custom_category] = "Custom category"
                    
                    # Ask if they want to add this as a rule
                    add_rule = input(f"Add '{transaction['title']}' -> '{custom_category}' as a rule? (y/N): ").strip().lower()
                    if add_rule == 'y':
                        self._suggest_new_rule(transaction['title'], custom_category)
                    
                    return custom_category
                else:
                    print("Please enter a valid number or category name")
            except KeyboardInterrupt:
                print(f"\nUsing AI suggestion: {ai_category}")
                return ai_category
    
    def _suggest_new_rule(self, transaction_title: str, category: str):
        """
        Suggest adding a new rule based on user input
        """
        # Use AI to extract the identifying pattern from the transaction title
        identifying_pattern = self._extract_identifying_pattern(transaction_title)
        
        print(f"\n💡 Suggested rule for future transactions:")
        print(f"   {identifying_pattern} -> {category}")
        
        add_to_file = input(f"Add this rule to transaction_rules.txt? (Y/n): ").strip().lower()
        if add_to_file != 'n':
            self._add_rule_to_file(identifying_pattern, category)
    
    def _extract_identifying_pattern(self, transaction_title: str) -> str:
        """
        Use AI to extract the core identifying pattern from a transaction title
        This removes IDs, numbers, and other variable parts
        """
        try:
            if not self.model_name:
                self.model_name = self._select_model_interactive()
            
            prompt = f"""Extract the core identifying pattern from this transaction title that would be useful for categorizing similar transactions.

Transaction title: {transaction_title}

Rules:
1. Remove variable parts like numbers, IDs, random codes
2. Keep the core merchant/business name
3. Remove location-specific details
4. Keep words that identify the type of business
5. Return ONLY the identifying pattern in UPPERCASE
6. Make it general enough to match similar transactions

Examples:
- "PRESTO FARE/PKF123ABC" → "PRESTO FARE"
- "STARBUCKS #12345" → "STARBUCKS"
- "AMAZON*4X5HZ3583" → "AMAZON"
- "MCDONALD'S #40569" → "MCDONALD"
- "UBER CANADA/UBERTRIP" → "UBER CANADA"

Identifying pattern:"""
            
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            pattern = response['message']['content'].strip().upper()
            
            # Fallback to manual extraction if AI response seems wrong
            if not pattern or len(pattern) < 3 or len(pattern) > 50:
                return self._manual_pattern_extraction(transaction_title)
            
            return pattern
            
        except Exception as e:
            print(f"Error extracting pattern with AI: {e}")
            return self._manual_pattern_extraction(transaction_title)
    
    def _manual_pattern_extraction(self, transaction_title: str) -> str:
        """
        Fallback manual pattern extraction
        """
        title_upper = transaction_title.upper()
        
        # Remove common patterns
        import re
        
        # Remove patterns like /ABC123, #12345, *ABC123
        cleaned = re.sub(r'[/#*]\w+', '', title_upper)
        
        # Remove standalone numbers
        cleaned = re.sub(r'\b\d+\b', '', cleaned)
        
        # Remove extra spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Take first 1-2 meaningful words
        words = cleaned.split()
        if len(words) >= 2:
            return ' '.join(words[:2])
        elif len(words) == 1:
            return words[0]
        else:
            return title_upper
    
    def _add_rule_to_file(self, pattern: str, category: str):
        """
        Add a new rule to the transaction_rules.txt file
        """
        rules_file = Path(__file__).parent.parent / "transaction_rules.txt"
        
        try:
            # Read existing content
            existing_content = ""
            if rules_file.exists():
                with open(rules_file, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            
            # Check if rule already exists
            new_rule = f"{pattern} -> {category}"
            if new_rule in existing_content:
                print(f"✅ Rule already exists: {new_rule}")
                return
            
            # Find the right section to add the rule
            section_headers = {
                'Transportation': '# Transportation',
                'Groceries': '# Groceries',
                'Subscription': '# Subscriptions',
                'Partying': '# Partying (Alcohol/Bars/Clubs)',
                'Cafe': '# Coffee/Cafes',
                'Eating Out': '# Eating Out',
                'Clothing': '# Clothing',
                'Technology': '# Technology',
                'Events': '# Events',
                'Vanity': '# Vanity',
                'Misc': '# Misc (known patterns that should be misc)'
            }
            
            header = section_headers.get(category, '# Misc (known patterns that should be misc)')
            
            # Add rule to appropriate section
            lines = existing_content.split('\n')
            insert_index = len(lines)
            
            # Find the section
            for i, line in enumerate(lines):
                if line.strip() == header:
                    # Find next section or end of file
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip().startswith('# ') and lines[j].strip() != header:
                            insert_index = j
                            break
                    else:
                        insert_index = len(lines)
                    break
            
            # Insert the new rule
            lines.insert(insert_index, f"{pattern} -> {category}")
            
            # Write back to file
            with open(rules_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            print(f"✅ Added rule to {rules_file}: {new_rule}")
            
            # Update our in-memory rules
            self.rules[pattern] = category
            
        except Exception as e:
            print(f"❌ Error adding rule to file: {e}")
            print(f"Please manually add: {pattern} -> {category}")
    
    def _get_available_models(self) -> List[str]:
        """Get list of available Ollama models"""
        try:
            models_response = ollama.list()
            
            # Handle different response structures
            if 'models' in models_response:
                models_list = models_response['models']
            else:
                models_list = models_response
            
            # Extract model names safely
            model_names = []
            for model in models_list:
                try:
                    if hasattr(model, 'model'):
                        # This is a Model object with a 'model' attribute
                        model_names.append(getattr(model, 'model'))
                    elif isinstance(model, dict):
                        # Try different possible keys for model name
                        name = model.get('name') or model.get('model') or model.get('id')
                        if name:
                            model_names.append(name)
                    elif isinstance(model, str):
                        model_names.append(model)
                    else:
                        # Try to convert to string and see if it contains model info
                        model_str = str(model)
                        if 'model=' in model_str:
                            # Extract model name from string representation
                            import re
                            match = re.search(r"model='([^']+)'", model_str)
                            if match:
                                model_names.append(match.group(1))
                except Exception as e:
                    print(f"Warning: Could not extract model name from {model}: {e}")
                    continue
            
            return model_names
        except Exception as e:
            print(f"Error getting available models: {e}")
            return []
    
    def _select_model_interactive(self) -> str:
        """Prompt user to select a model from available models"""
        print("🤖 Selecting Ollama model for transaction categorization...")
        
        # Get available models
        available_models = self._get_available_models()
        
        if not available_models:
            print("❌ No Ollama models found. Please install a model first.")
            print("Example: ollama pull llama3.2")
            return "llama3.2"  # Default fallback
        
        print(f"\n📋 Available models:")
        for i, model in enumerate(available_models, 1):
            print(f"   {i}. {model}")
        
        # Recommend llama models for better performance
        recommended = [m for m in available_models if 'llama' in m.lower()]
        if recommended:
            print(f"\n💡 Recommended: {recommended[0]} (Llama models work well for categorization)")
        
        # Prompt for selection
        while True:
            try:
                choice = input(f"\nSelect model (1-{len(available_models)}) or press Enter for default: ").strip()
                
                if not choice:
                    # Use recommended model or first available
                    selected = recommended[0] if recommended else available_models[0]
                    print(f"Using default: {selected}")
                    return selected
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(available_models):
                    selected = available_models[choice_num - 1]
                    print(f"Selected: {selected}")
                    return selected
                else:
                    print(f"Please enter a number between 1 and {len(available_models)}")
                    
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                print("\nUsing default model: llama3.2")
                return "llama3.2"
    
    def _create_categorization_prompt(self, transaction: Dict) -> str:
        """
        Create a prompt for the LLM to categorize a transaction with confidence
        """
        # Build categories list dynamically using descriptions
        categories_text = ""
        for category in self.categories:
            description = self.category_descriptions.get(category, "Custom category")
            categories_text += f"- {category}: {description}\n"
        
        prompt = f"""You are a transaction categorization assistant. Given a credit card transaction, categorize it into one of these exact categories and provide a confidence score.

Categories:
{categories_text.strip()}

Transaction Details:
- Name: {transaction['title']}
- Location: {transaction['location']}
- Amount: ${abs(transaction['amount']):.2f}

Response format (exactly like this):
Category: [CATEGORY_NAME]
Confidence: [0.0-1.0]

Rules:
1. Category must be exactly one of the categories listed above
2. Confidence should be between 0.0 (not sure) and 1.0 (very sure)
3. Consider how clearly the merchant name indicates the category
4. If merchant name is unclear or ambiguous, use lower confidence

Response:"""
        
        return prompt
    
    def categorize_transaction(self, transaction: Dict) -> str:
        """
        Categorize a single transaction using rules first, then LLM with confidence
        Returns the category name
        """
        # First, try rule-based categorization
        rule_category = self._apply_rules(transaction)
        if rule_category:
            return rule_category
        
        # If no rule matches, fall back to AI with confidence
        # Ensure we have a model name
        if not self.model_name:
            self.model_name = self._select_model_interactive()
        
        try:
            prompt = self._create_categorization_prompt(transaction)
            
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            # Parse the response to get category and confidence
            response_text = response['message']['content'].strip()
            category, confidence = self._parse_ai_response(response_text)
            
            # If confidence is below threshold, ask user
            if confidence < self.confidence_threshold:
                return self._ask_user_for_category(transaction, category, confidence)
            
            # Validate that the category is one of our expected categories
            if category in self.categories:
                return category
            else:
                print(f"Warning: LLM returned unexpected category '{category}' for {transaction['title']}, using 'Misc'")
                return "Misc"
                
        except Exception as e:
            print(f"Error categorizing transaction {transaction['title']}: {e}")
            return "Misc"
    
    def categorize_transactions(self, transactions: List[Dict]) -> List[str]:
        """
        Categorize multiple transactions
        Returns list of category names in same order as input transactions
        """
        categories = []
        rules_used = 0
        ai_auto = 0
        ai_manual = 0
        
        print(f"🤖 Categorizing {len(transactions)} transactions using rules + {self.model_name}...")
        print(f"   Confidence threshold: {self.confidence_threshold:.1f} (below this asks for manual input)")
        
        for i, transaction in enumerate(transactions):
            # Check if rule applies first
            rule_category = self._apply_rules(transaction)
            
            if rule_category:
                category = rule_category
                method = "📏 Rule"
                rules_used += 1
            else:
                # Get AI categorization with confidence check
                original_categorize = self.categorize_transaction
                # Temporarily override to get detailed info
                category = self._categorize_with_confidence_info(transaction)
                
                if hasattr(self, '_last_was_manual') and self._last_was_manual:
                    method = "❓ Manual"
                    ai_manual += 1
                    delattr(self, '_last_was_manual')
                else:
                    method = "🤖 AI"
                    ai_auto += 1
            
            categories.append(category)
            print(f"   {i+1:3d}. {transaction['title'][:30]:<30} → {category:<15} ({method})")
        
        print(f"\n📊 Categorization summary: {rules_used} by rules, {ai_auto} by AI, {ai_manual} manual")
        return categories
    
    def _categorize_with_confidence_info(self, transaction: Dict) -> str:
        """
        Helper method to categorize and track if manual input was used
        """
        # This is a bit hacky but allows us to track manual vs auto AI
        rule_category = self._apply_rules(transaction)
        if rule_category:
            return rule_category
        
        if not self.model_name:
            self.model_name = self._select_model_interactive()
        
        try:
            prompt = self._create_categorization_prompt(transaction)
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            response_text = response['message']['content'].strip()
            category, confidence = self._parse_ai_response(response_text)
            
            if confidence < self.confidence_threshold:
                self._last_was_manual = True
                return self._ask_user_for_category(transaction, category, confidence)
            
            return category if category in self.categories else "Misc"
            
        except Exception as e:
            print(f"Error categorizing transaction {transaction['title']}: {e}")
            return "Misc"
    
    def test_connection(self) -> bool:
        """
        Test connection to Ollama and check if model is available
        """
        try:
            # Get available models
            model_names = self._get_available_models()
            
            if not model_names:
                print("❌ No Ollama models found")
                print("Try running: ollama pull llama3.2")
                return False
            
            print(f"Available models: {model_names}")
            
            # Ensure we have a model selected
            if not self.model_name:
                self.model_name = self._select_model_interactive()
            
            # Check if our model is available (check for partial matches too)
            model_available = False
            for name in model_names:
                if self.model_name in name or name.startswith(self.model_name):
                    model_available = True
                    break
            
            if model_available:
                print(f"✅ Model {self.model_name} is available")
                
                # Test with a simple prompt
                test_transaction = {
                    'title': 'STARBUCKS',
                    'location': 'TORONTO ON',
                    'amount': -5.50
                }
                
                print("🧪 Testing categorization...")
                category = self.categorize_transaction(test_transaction)
                print(f"   Test result: STARBUCKS → {category}")
                
                return True
            else:
                print(f"❌ Model {self.model_name} not found")
                print(f"Available models: {model_names}")
                print("Try running: ollama pull llama3.2")
                return False
                
        except Exception as e:
            print(f"❌ Error connecting to Ollama: {e}")
            print("Make sure Ollama is running with: ollama serve")
            return False
