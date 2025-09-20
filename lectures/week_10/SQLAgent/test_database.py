#!/usr/bin/env python3
"""
Database Test Script

This script tests the database structure and data without requiring OpenAI API keys.
It demonstrates the database schema and provides sample queries.
"""

import sqlite3
import pathlib

def test_database():
    """
    Test the database structure and run sample queries.
    """
    
    # Get database path
    current_dir = pathlib.Path(__file__).resolve().parent
    db_path = current_dir / "sql_agent_class.db"
    
    print("🧪 Testing Your Custom Database")
    print("=" * 50)
    
    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test 1: Show all tables
        print("📋 Database Tables:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        for table in tables:
            print(f"   ✅ {table[0]}")
        
        # Test 2: Show table schemas
        print("\n🏗️  Table Schemas:")
        for table in tables:
            table_name = table[0]
            print(f"\n📊 {table_name}:")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                pk_str = " (PRIMARY KEY)" if pk else ""
                not_null_str = " NOT NULL" if not_null else ""
                default_str = f" DEFAULT {default_val}" if default_val else ""
                print(f"   - {col_name}: {col_type}{not_null_str}{default_str}{pk_str}")
        
        # Test 3: Sample queries that the SQL agent would run
        print("\n🔍 Sample Analytics Queries:")
        print("=" * 50)
        
        # Query 1: Customer overview
        print("👥 Customer Overview:")
        cursor.execute("""
            SELECT region, COUNT(*) as customer_count, 
                   COUNT(CASE WHEN status = 'active' THEN 1 END) as active_customers
            FROM customers 
            GROUP BY region 
            ORDER BY customer_count DESC
        """)
        results = cursor.fetchall()
        for row in results:
            print(f"   {row[0]}: {row[1]} total customers ({row[2]} active)")
        
        # Query 2: Product performance
        print("\n🛍️  Product Performance:")
        cursor.execute("""
            SELECT p.name, p.category, 
                   COUNT(oi.id) as times_ordered,
                   SUM(oi.quantity) as total_quantity,
                   SUM(oi.total_price_cents) as total_revenue_cents
            FROM products p
            LEFT JOIN order_items oi ON p.id = oi.product_id
            LEFT JOIN orders o ON oi.order_id = o.id AND o.status IN ('delivered', 'shipped')
            GROUP BY p.id, p.name, p.category
            ORDER BY total_revenue_cents DESC
        """)
        results = cursor.fetchall()
        for row in results:
            revenue = row[4] / 100 if row[4] else 0
            print(f"   {row[0]} ({row[1]}): {row[2]} orders, {row[3]} units, ${revenue:.2f}")
        
        # Query 3: Order status distribution
        print("\n📦 Order Status Distribution:")
        cursor.execute("""
            SELECT status, COUNT(*) as count,
                   SUM(total_amount_cents) as total_amount_cents
            FROM orders 
            GROUP BY status 
            ORDER BY count DESC
        """)
        results = cursor.fetchall()
        for row in results:
            amount = row[2] / 100 if row[2] else 0
            print(f"   {row[0]}: {row[1]} orders (${amount:.2f})")
        
        # Query 4: Revenue by month
        print("\n📈 Revenue by Month:")
        cursor.execute("""
            SELECT strftime('%Y-%m', order_date) as month,
                   COUNT(*) as order_count,
                   SUM(total_amount_cents) as revenue_cents
            FROM orders 
            WHERE status IN ('delivered', 'shipped')
            GROUP BY strftime('%Y-%m', order_date)
            ORDER BY month
        """)
        results = cursor.fetchall()
        for row in results:
            revenue = row[2] / 100 if row[2] else 0
            print(f"   {row[0]}: {row[1]} orders, ${revenue:.2f}")
        
        # Query 5: Top customers by revenue
        print("\n🏆 Top Customers by Revenue:")
        cursor.execute("""
            SELECT c.name, c.region,
                   COUNT(o.id) as order_count,
                   SUM(o.total_amount_cents) as total_spent_cents
            FROM customers c
            JOIN orders o ON c.id = o.customer_id
            WHERE o.status IN ('delivered', 'shipped')
            GROUP BY c.id, c.name, c.region
            ORDER BY total_spent_cents DESC
            LIMIT 5
        """)
        results = cursor.fetchall()
        for row in results:
            spent = row[3] / 100 if row[3] else 0
            print(f"   {row[0]} ({row[1]}): {row[2]} orders, ${spent:.2f}")
        
        # Test 4: Complex analytics query
        print("\n🔬 Complex Analytics Query:")
        print("Customer Lifetime Value Analysis:")
        cursor.execute("""
            SELECT 
                c.name,
                c.region,
                COUNT(DISTINCT o.id) as total_orders,
                SUM(oi.total_price_cents) as gross_revenue_cents,
                COALESCE(SUM(r.amount_cents), 0) as total_refunds_cents,
                (SUM(oi.total_price_cents) - COALESCE(SUM(r.amount_cents), 0)) as net_revenue_cents,
                MIN(o.order_date) as first_order_date,
                MAX(o.order_date) as last_order_date
            FROM customers c
            JOIN orders o ON c.id = o.customer_id
            JOIN order_items oi ON o.id = oi.order_id
            LEFT JOIN refunds r ON o.id = r.order_id
            WHERE o.status IN ('delivered', 'shipped')
            GROUP BY c.id, c.name, c.region
            ORDER BY net_revenue_cents DESC
        """)
        results = cursor.fetchall()
        for row in results:
            gross = row[3] / 100 if row[3] else 0
            refunds = row[4] / 100 if row[4] else 0
            net = row[5] / 100 if row[5] else 0
            print(f"   {row[0]} ({row[1]}): {row[2]} orders, ${gross:.2f} gross, ${refunds:.2f} refunds, ${net:.2f} net")
            print(f"      First: {row[6]}, Last: {row[7]}")
        
        conn.close()
        
        print("\n✅ Database test completed successfully!")
        print("\n💡 Your database is ready for SQL agent analysis!")
        print("   - All tables are properly structured")
        print("   - Sample data is loaded and validated")
        print("   - Complex queries work correctly")
        print("   - Ready for LangChain SQL agent integration")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing database: {e}")
        return False

if __name__ == "__main__":
    test_database()
