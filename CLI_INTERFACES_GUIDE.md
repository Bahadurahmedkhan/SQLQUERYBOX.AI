# 🖥️ SQL Agent CLI Interfaces Guide

## Overview

Interactive command-line interfaces for all SQL agent scripts, allowing users to enter prompts about the database and get responses from the Gemini-powered agents.

## 🚀 Available CLI Interfaces

### 1. **00_simple_llm_cli.py** - Simple LLM Agent CLI
**Purpose**: Conversational AI agent without database tools
**Features**:
- General technology and programming questions
- Educational demonstrations of agent framework
- No database access (conversational only)

**Usage**:
```bash
python scripts/00_simple_llm_cli.py
```

**Example Questions**:
- "What is machine learning?"
- "Explain how databases work"
- "What are the benefits of using AI agents?"

---

### 2. **01_simple_agent_cli.py** - Simple SQL Agent CLI
**Purpose**: Basic SQL agent with unrestricted database access
**Features**:
- Natural language to SQL conversion
- Basic database queries
- No security restrictions (educational only)

**Usage**:
```bash
python scripts/01_simple_agent_cli.py
```

**Example Questions**:
- "How many customers do we have?"
- "Show me products under $50"
- "What's our total revenue?"

---

### 3. **02_risky_delete_demo_cli.py** - Dangerous SQL Agent CLI ⚠️
**Purpose**: Educational demo of dangerous SQL patterns
**Features**:
- Can execute ANY SQL including DELETE, DROP, etc.
- Shows what NOT to do in production
- Multiple safety warnings

**Usage**:
```bash
python scripts/02_risky_delete_demo_cli.py
```

**⚠️ WARNING**: This agent can actually delete data! Use with caution.

---

### 4. **03_guardrailed_agent_cli.py** - Safe SQL Agent CLI 🛡️
**Purpose**: Production-ready secure SQL agent
**Features**:
- Only SELECT statements allowed
- Automatic LIMIT injection
- SQL injection protection
- Comprehensive security guardrails

**Usage**:
```bash
python scripts/03_guardrailed_agent_cli.py
```

**Example Questions**:
- "Show me top 10 customers by revenue"
- "What's our monthly sales trend?"
- "Which products are most popular?"

---

### 5. **04_complex_queries_cli.py** - Advanced Analytics CLI 📊
**Purpose**: Sophisticated business intelligence and analytics
**Features**:
- Complex multi-table JOINs
- Revenue analysis and customer lifetime value
- Time-series analysis
- Multi-turn conversations

**Usage**:
```bash
python scripts/04_complex_queries_cli.py
```

**Example Questions**:
- "Show me revenue trends for the last 6 months"
- "Who are our top customers by lifetime value?"
- "What's our product performance ranking?"

## 🎯 Common Commands

All CLI interfaces support these commands:

| Command | Description |
|---------|-------------|
| `help` | Show example questions and usage |
| `schema` | Display database structure |
| `clear` | Clear the terminal screen |
| `quit` / `exit` / `q` | Exit the CLI |

### Additional Commands by Interface:

**Script 00 (Simple LLM)**:
- `help` - Technology and programming examples

**Script 01 (Simple Agent)**:
- `help` - Basic database query examples
- `schema` - Database table structure

**Script 02 (Risky Demo)** ⚠️:
- `help` - Dangerous SQL examples
- `warning` - Detailed security warnings

**Script 03 (Safe Agent)** 🛡️:
- `help` - Safe analytics examples
- `schema` - Database structure
- `security` - Security features explanation

**Script 04 (Advanced Analytics)** 📊:
- `help` - Complex analytics examples
- `schema` - Database structure with business logic
- `examples` - Sophisticated query examples

## 🗄️ Database Schema

Your custom database includes these tables:

### Core Business Tables
- **customers** - Customer information (id, name, email, region, status)
- **products** - Product catalog (id, name, category, price, stock)
- **orders** - Order records (id, customer_id, order_date, status, total)
- **order_items** - Line items (id, order_id, product_id, quantity, price)
- **payments** - Payment information (id, order_id, amount, method, status)
- **refunds** - Refund records (id, order_id, amount, reason)

### Analytics Tables
- **categories** - Product categories (id, name, description, parent_id)
- **inventory_movements** - Stock tracking (id, product_id, movement_type, quantity)
- **customer_segments** - Customer segmentation (id, name, criteria)

## 💡 Usage Tips

### Getting Started
1. **Start with Script 03** (Safe Agent) for secure database exploration
2. **Use Script 04** (Advanced Analytics) for complex business intelligence
3. **Try Script 00** (Simple LLM) for general AI conversations

### Best Practices
- **Ask specific questions** for better results
- **Use natural language** - no need to write SQL
- **Try follow-up questions** for deeper analysis
- **Use the `help` command** for inspiration

### Example Conversation Flow
```
User: "What's our total revenue?"
Agent: [Shows total revenue]

User: "Break that down by month"
Agent: [Shows monthly revenue breakdown]

User: "Which month had the highest revenue?"
Agent: [Identifies peak month and provides analysis]
```

## 🔧 Troubleshooting

### Common Issues

**"Quota exceeded" Error**
```
Solution: Wait for rate limit reset (15 requests/minute for free tier)
```

**"Database not found" Error**
```
Solution: Run python setup_my_database.py to create the database
```

**"API key not found" Error**
```
Solution: Check gemini_config.py contains your API key
```

### Getting Help
- Use the `help` command in any CLI
- Check the `schema` command for database structure
- Review error messages for specific guidance

## 🎉 Quick Start

1. **Choose your CLI**:
   ```bash
   # For safe database exploration
   python scripts/03_guardrailed_agent_cli.py
   
   # For advanced analytics
   python scripts/04_complex_queries_cli.py
   ```

2. **Ask your first question**:
   ```
   💬 Ask about your database: How many customers do we have?
   ```

3. **Explore further**:
   ```
   💬 Ask about your database: help
   ```

## 📊 Sample Analytics Queries

### Customer Analytics
- "Show me customers by region"
- "Who are our top 10 customers by revenue?"
- "What's the average customer lifetime value?"

### Product Analytics
- "Which product categories generate the most revenue?"
- "Show me products with low stock"
- "What's our best-selling product?"

### Business Intelligence
- "Show me monthly revenue trends"
- "What's our average order value?"
- "Which region has the most customers?"

### Advanced Analytics
- "Show me customer lifetime value ranking"
- "What are our revenue trends for the last 6 months?"
- "Identify our top-performing product categories"

## 🚀 Ready to Use!

All CLI interfaces are ready to use with your custom database and Gemini API. Start with the Safe Agent (Script 03) for secure exploration, then move to Advanced Analytics (Script 04) for sophisticated business intelligence!
