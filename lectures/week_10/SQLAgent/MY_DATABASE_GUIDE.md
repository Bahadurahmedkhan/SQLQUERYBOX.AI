# 🗄️ Your Custom Database Guide

## Overview

This guide explains your newly created custom database that replaces the original sample data. Your database is designed to be flexible, comprehensive, and ready for advanced SQL agent analytics.

## 📊 Database Structure

### Core Business Tables

#### 1. **customers** - Customer Management
```sql
- id (INTEGER PRIMARY KEY)
- name (TEXT NOT NULL)
- email (TEXT UNIQUE)
- phone (TEXT)
- created_at (TEXT NOT NULL)
- updated_at (TEXT)
- region (TEXT)
- status (TEXT DEFAULT 'active') - 'active', 'inactive', 'suspended'
- notes (TEXT)
```

#### 2. **products** - Product Catalog
```sql
- id (INTEGER PRIMARY KEY)
- name (TEXT NOT NULL)
- description (TEXT)
- category (TEXT)
- subcategory (TEXT)
- price_cents (INTEGER NOT NULL)
- cost_cents (INTEGER)
- sku (TEXT UNIQUE)
- stock_quantity (INTEGER DEFAULT 0)
- status (TEXT DEFAULT 'active') - 'active', 'discontinued', 'out_of_stock'
- created_at (TEXT NOT NULL)
- updated_at (TEXT)
```

#### 3. **orders** - Order Management
```sql
- id (INTEGER PRIMARY KEY)
- customer_id (INTEGER NOT NULL) → customers(id)
- order_number (TEXT UNIQUE NOT NULL)
- order_date (TEXT NOT NULL)
- status (TEXT NOT NULL) - 'pending', 'confirmed', 'shipped', 'delivered', 'cancelled', 'refunded'
- total_amount_cents (INTEGER NOT NULL)
- shipping_address (TEXT)
- billing_address (TEXT)
- notes (TEXT)
- created_at (TEXT NOT NULL)
- updated_at (TEXT)
```

#### 4. **order_items** - Order Line Items
```sql
- id (INTEGER PRIMARY KEY)
- order_id (INTEGER NOT NULL) → orders(id)
- product_id (INTEGER NOT NULL) → products(id)
- quantity (INTEGER NOT NULL)
- unit_price_cents (INTEGER NOT NULL)
- total_price_cents (INTEGER NOT NULL)
- created_at (TEXT NOT NULL)
```

#### 5. **payments** - Payment Processing
```sql
- id (INTEGER PRIMARY KEY)
- order_id (INTEGER NOT NULL) → orders(id)
- amount_cents (INTEGER NOT NULL)
- payment_method (TEXT NOT NULL) - 'credit_card', 'debit_card', 'paypal', 'bank_transfer', 'cash', 'cryptocurrency'
- transaction_id (TEXT)
- paid_at (TEXT)
- status (TEXT NOT NULL) - 'pending', 'succeeded', 'failed', 'refunded', 'cancelled'
- gateway (TEXT)
- notes (TEXT)
- created_at (TEXT NOT NULL)
```

#### 6. **refunds** - Refund Management
```sql
- id (INTEGER PRIMARY KEY)
- order_id (INTEGER NOT NULL) → orders(id)
- amount_cents (INTEGER NOT NULL)
- reason (TEXT)
- refunded_at (TEXT NOT NULL)
- status (TEXT DEFAULT 'completed') - 'pending', 'completed', 'failed'
- notes (TEXT)
- created_at (TEXT NOT NULL)
```

### Advanced Analytics Tables

#### 7. **categories** - Product Categories
```sql
- id (INTEGER PRIMARY KEY)
- name (TEXT NOT NULL UNIQUE)
- description (TEXT)
- parent_id (INTEGER) → categories(id) - For hierarchical categories
- created_at (TEXT NOT NULL)
```

#### 8. **inventory_movements** - Stock Tracking
```sql
- id (INTEGER PRIMARY KEY)
- product_id (INTEGER NOT NULL) → products(id)
- movement_type (TEXT NOT NULL) - 'in', 'out', 'adjustment', 'return'
- quantity (INTEGER NOT NULL)
- reason (TEXT)
- reference_id (INTEGER) - Can reference order_id, etc.
- created_at (TEXT NOT NULL)
```

#### 9. **customer_segments** - Customer Segmentation
```sql
- id (INTEGER PRIMARY KEY)
- name (TEXT NOT NULL UNIQUE)
- description (TEXT)
- criteria (TEXT) - JSON or text description of segment criteria
- created_at (TEXT NOT NULL)
```

## 🔗 Relationships

```
customers (1) ←→ (many) orders
orders (1) ←→ (many) order_items
orders (1) ←→ (many) payments
orders (1) ←→ (many) refunds
products (1) ←→ (many) order_items
products (1) ←→ (many) inventory_movements
categories (1) ←→ (many) categories (self-referencing)
```

## 📈 Sample Data Overview

Your database comes pre-loaded with realistic sample data:

- **6 customers** across 4 regions (North America, Europe, Asia Pacific, Middle East)
- **6 products** across 5 categories (Electronics, Clothing, Home & Garden, Books, Sports)
- **8 orders** with various statuses and dates
- **11 order items** with realistic pricing
- **8 payments** using different methods (credit card, PayPal)
- **1 refund** for demonstration
- **11 inventory movements** tracking stock changes
- **5 product categories** with hierarchical structure
- **4 customer segments** for analytics

## 🎯 Key Business Metrics

### Revenue Calculations
```sql
-- Gross Revenue (before refunds)
SELECT SUM(oi.total_price_cents) / 100.0 as gross_revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
WHERE o.status IN ('delivered', 'shipped');

-- Net Revenue (after refunds)
SELECT 
    SUM(oi.total_price_cents) - COALESCE(SUM(r.amount_cents), 0)
) / 100.0 as net_revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
LEFT JOIN refunds r ON o.id = r.order_id
WHERE o.status IN ('delivered', 'shipped');
```

### Customer Lifetime Value
```sql
SELECT 
    c.name,
    COUNT(DISTINCT o.id) as total_orders,
    SUM(oi.total_price_cents) / 100.0 as gross_revenue,
    COALESCE(SUM(r.amount_cents), 0) / 100.0 as total_refunds,
    (SUM(oi.total_price_cents) - COALESCE(SUM(r.amount_cents), 0)) / 100.0 as net_revenue
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN refunds r ON o.id = r.order_id
WHERE o.status IN ('delivered', 'shipped')
GROUP BY c.id, c.name
ORDER BY net_revenue DESC;
```

## 🛠️ Customization Guide

### Adding Your Own Data

1. **Modify the schema** in `my_database_schema.sql`:
   - Add new columns to existing tables
   - Create new tables for your specific needs
   - Adjust constraints and relationships

2. **Update sample data** in `my_database_schema.sql`:
   - Replace the INSERT statements with your own data
   - Maintain referential integrity
   - Use realistic dates and values

3. **Recreate the database**:
   ```bash
   python setup_my_database.py
   ```

### Common Customizations

#### Add New Product Attributes
```sql
ALTER TABLE products ADD COLUMN brand TEXT;
ALTER TABLE products ADD COLUMN weight_grams INTEGER;
ALTER TABLE products ADD COLUMN dimensions TEXT;
```

#### Add Customer Demographics
```sql
ALTER TABLE customers ADD COLUMN age INTEGER;
ALTER TABLE customers ADD COLUMN gender TEXT;
ALTER TABLE customers ADD COLUMN income_bracket TEXT;
```

#### Add Order Tracking
```sql
CREATE TABLE order_tracking (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    location TEXT,
    timestamp TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY(order_id) REFERENCES orders(id)
);
```

## 🔍 SQL Agent Integration

Your database is fully compatible with all the SQL agent scripts:

### Script Compatibility
- ✅ **01_simple_agent.py** - Basic SQL agent (requires OpenAI API key)
- ✅ **02_risky_delete_demo.py** - Dangerous patterns demo (requires OpenAI API key)
- ✅ **03_guardrailed_agent.py** - Secure SQL agent (requires OpenAI API key)
- ✅ **04_complex_queries.py** - Advanced analytics (requires OpenAI API key)

### Testing Without API Keys
Use the included test script:
```bash
python test_database.py
```

## 📊 Analytics Examples

### Top Products by Revenue
```sql
SELECT 
    p.name,
    p.category,
    COUNT(oi.id) as times_ordered,
    SUM(oi.quantity) as total_quantity,
    SUM(oi.total_price_cents) / 100.0 as total_revenue
FROM products p
JOIN order_items oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id
WHERE o.status IN ('delivered', 'shipped')
GROUP BY p.id, p.name, p.category
ORDER BY total_revenue DESC;
```

### Monthly Revenue Trends
```sql
SELECT 
    strftime('%Y-%m', order_date) as month,
    COUNT(*) as order_count,
    SUM(total_amount_cents) / 100.0 as revenue
FROM orders 
WHERE status IN ('delivered', 'shipped')
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;
```

### Customer Segmentation
```sql
SELECT 
    c.region,
    COUNT(DISTINCT c.id) as customer_count,
    COUNT(DISTINCT o.id) as total_orders,
    AVG(o.total_amount_cents) / 100.0 as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id AND o.status IN ('delivered', 'shipped')
GROUP BY c.region
ORDER BY customer_count DESC;
```

## 🔧 Maintenance

### Database Reset
```bash
python setup_my_database.py
```

### Backup Database
```bash
cp sql_agent_class.db sql_agent_class_backup_$(date +%Y%m%d).db
```

### Validate Data Integrity
```bash
python test_database.py
```

## 🚀 Next Steps

1. **Customize the schema** for your specific business needs
2. **Add your own data** by modifying the INSERT statements
3. **Set up OpenAI API key** to use the SQL agent scripts
4. **Run analytics queries** to explore your data
5. **Build custom reports** using the SQL agent framework

## 📝 Notes

- All monetary values are stored in cents to avoid floating-point precision issues
- Dates are stored as TEXT in ISO format (YYYY-MM-DD)
- Foreign key constraints are enabled for data integrity
- Indexes are created on frequently queried columns for performance
- The database is designed to scale with additional data

Your custom database is now ready for advanced SQL agent analytics and business intelligence applications!
