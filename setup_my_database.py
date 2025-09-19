#!/usr/bin/env python3
"""
Setup Script for Your Custom Database

This script creates a new SQLite database using your custom schema and sample data.
It replaces the original database with your own data structure.

Usage:
    python setup_my_database.py

Features:
- Creates database from your custom schema
- Includes sample data for testing
- Provides database statistics
- Validates data integrity
"""

import sqlite3
import pathlib
from datetime import datetime

def setup_database():
    """
    Set up the custom database using the new schema.
    
    This function:
    1. Creates a new SQLite database
    2. Executes the custom schema SQL
    3. Validates the setup
    4. Provides statistics
    """
    
    # Get the current directory and file paths
    current_dir = pathlib.Path(__file__).resolve().parent
    db_path = current_dir / "sql_agent_class.db"
    schema_path = current_dir / "my_database_schema.sql"
    
    print("🚀 Setting up your custom database...")
    print(f"📁 Database location: {db_path}")
    print(f"📄 Schema file: {schema_path}")
    
    # Check if schema file exists
    if not schema_path.exists():
        print(f"❌ Error: Schema file not found at {schema_path}")
        return False
    
    try:
        # Read the schema SQL
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        print("📖 Reading schema file...")
        
        # Create database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🗄️  Creating database tables...")
        
        # Execute the schema SQL
        cursor.executescript(schema_sql)
        
        # Commit changes
        conn.commit()
        
        print("✅ Database created successfully!")
        
        # Get database statistics
        print("\n📊 Database Statistics:")
        print("=" * 50)
        
        # Get table information
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"📋 {table_name}: {count} records")
        
        # Get some sample data
        print("\n🔍 Sample Data Preview:")
        print("=" * 50)
        
        # Show sample customers
        cursor.execute("SELECT id, name, email, region FROM customers LIMIT 3")
        customers = cursor.fetchall()
        print("👥 Sample Customers:")
        for customer in customers:
            print(f"   {customer[0]}: {customer[1]} ({customer[2]}) - {customer[3]}")
        
        # Show sample products
        cursor.execute("SELECT id, name, category, price_cents FROM products LIMIT 3")
        products = cursor.fetchall()
        print("\n🛍️  Sample Products:")
        for product in products:
            price = product[3] / 100  # Convert cents to dollars
            print(f"   {product[0]}: {product[1]} ({product[2]}) - ${price:.2f}")
        
        # Show recent orders
        cursor.execute("""
            SELECT o.id, c.name, o.order_date, o.status, o.total_amount_cents 
            FROM orders o 
            JOIN customers c ON o.customer_id = c.id 
            ORDER BY o.order_date DESC 
            LIMIT 3
        """)
        orders = cursor.fetchall()
        print("\n📦 Recent Orders:")
        for order in orders:
            total = order[4] / 100  # Convert cents to dollars
            print(f"   Order {order[0]}: {order[1]} - {order[2]} - {order[3]} - ${total:.2f}")
        
        # Test some analytics queries
        print("\n📈 Analytics Preview:")
        print("=" * 50)
        
        # Total revenue
        cursor.execute("""
            SELECT SUM(oi.total_price_cents) as total_revenue
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE o.status IN ('delivered', 'shipped')
        """)
        total_revenue = cursor.fetchone()[0] or 0
        print(f"💰 Total Revenue: ${total_revenue / 100:.2f}")
        
        # Top selling product
        cursor.execute("""
            SELECT p.name, SUM(oi.quantity) as total_sold
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            JOIN orders o ON oi.order_id = o.id
            WHERE o.status IN ('delivered', 'shipped')
            GROUP BY p.id, p.name
            ORDER BY total_sold DESC
            LIMIT 1
        """)
        top_product = cursor.fetchone()
        if top_product:
            print(f"🏆 Top Selling Product: {top_product[0]} ({top_product[1]} units)")
        
        # Customer count by region
        cursor.execute("""
            SELECT region, COUNT(*) as customer_count
            FROM customers
            GROUP BY region
            ORDER BY customer_count DESC
        """)
        regions = cursor.fetchall()
        print("🌍 Customers by Region:")
        for region in regions:
            print(f"   {region[0]}: {region[1]} customers")
        
        conn.close()
        
        print(f"\n🎉 Database setup completed successfully!")
        print(f"📁 Database file: {db_path}")
        print(f"⏰ Created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n💡 Next Steps:")
        print("1. Run the SQL agent scripts to test your database")
        print("2. Customize the schema in 'my_database_schema.sql' for your needs")
        print("3. Add your own data by modifying the INSERT statements")
        print("4. Use the analytics scripts to explore your data")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def validate_database():
    """
    Validate the database structure and data integrity.
    """
    print("\n🔍 Validating database integrity...")
    
    current_dir = pathlib.Path(__file__).resolve().parent
    db_path = current_dir / "sql_agent_class.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check foreign key constraints
        cursor.execute("PRAGMA foreign_key_check")
        fk_errors = cursor.fetchall()
        
        if fk_errors:
            print("⚠️  Foreign key constraint violations found:")
            for error in fk_errors:
                print(f"   {error}")
        else:
            print("✅ Foreign key constraints validated")
        
        # Check for orphaned records
        cursor.execute("""
            SELECT COUNT(*) FROM order_items oi
            LEFT JOIN orders o ON oi.order_id = o.id
            WHERE o.id IS NULL
        """)
        orphaned_items = cursor.fetchone()[0]
        
        if orphaned_items > 0:
            print(f"⚠️  Found {orphaned_items} orphaned order items")
        else:
            print("✅ No orphaned order items found")
        
        conn.close()
        print("✅ Database validation completed")
        
    except Exception as e:
        print(f"❌ Error validating database: {e}")

if __name__ == "__main__":
    print("🛠️  Custom Database Setup Tool")
    print("=" * 50)
    
    success = setup_database()
    
    if success:
        validate_database()
        print("\n🎯 Your custom database is ready to use!")
    else:
        print("\n❌ Database setup failed. Please check the error messages above.")
