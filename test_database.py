#!/usr/bin/env python3
"""
Test database queries for time-based analysis
"""

import sqlite3
import os

def test_database():
    """Test database queries"""
    db_path = os.path.join('lectures', 'week_10', 'SQLAgent', 'sql_agent_class.db')
    
    print("🧪 Testing Database Queries...")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check what order dates we have
    print("📅 Order dates in database:")
    cursor.execute('SELECT DISTINCT order_date FROM orders ORDER BY order_date')
    dates = cursor.fetchall()
    for date in dates:
        print(f"  {date['order_date']}")
    
    print(f"\n📊 Total orders: {len(dates)}")
    
    # Test January 2024 query
    print("\n🔍 Testing January 2024 query:")
    query = """
        SELECT COUNT(DISTINCT c.id) as customer_count,
               COUNT(DISTINCT o.id) as order_count,
               SUM(oi.quantity * oi.unit_price_cents) as total_revenue
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        JOIN order_items oi ON o.id = oi.order_id
        WHERE o.status = 'paid' AND strftime('%Y-%m', o.order_date) = '2024-01'
    """
    
    try:
        result = cursor.execute(query).fetchone()
        print(f"✅ Query successful!")
        print(f"   Customer count: {result['customer_count'] if result else 0}")
        print(f"   Order count: {result['order_count'] if result else 0}")
        print(f"   Total revenue: {result['total_revenue'] if result else 0}")
    except Exception as e:
        print(f"❌ Query failed: {e}")
    
    # Test with actual dates from database
    print("\n🔍 Testing with actual dates:")
    cursor.execute('SELECT order_date FROM orders LIMIT 1')
    sample_date = cursor.fetchone()['order_date']
    print(f"   Sample date: {sample_date}")
    
    # Extract year-month from sample date
    year_month = sample_date[:7]  # Assuming format YYYY-MM-DD
    print(f"   Year-month: {year_month}")
    
    query2 = f"""
        SELECT COUNT(DISTINCT c.id) as customer_count,
               COUNT(DISTINCT o.id) as order_count,
               SUM(oi.quantity * oi.unit_price_cents) as total_revenue
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        JOIN order_items oi ON o.id = oi.order_id
        WHERE o.status = 'paid' AND strftime('%Y-%m', o.order_date) = '{year_month}'
    """
    
    try:
        result2 = cursor.execute(query2).fetchone()
        print(f"✅ Query with actual date successful!")
        print(f"   Customer count: {result2['customer_count'] if result2 else 0}")
        print(f"   Order count: {result2['order_count'] if result2 else 0}")
        print(f"   Total revenue: {result2['total_revenue'] if result2 else 0}")
    except Exception as e:
        print(f"❌ Query with actual date failed: {e}")
    
    conn.close()

if __name__ == "__main__":
    test_database()
