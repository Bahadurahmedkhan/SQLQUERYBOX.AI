#!/usr/bin/env python3
"""
Check order statuses in database
"""

import sqlite3
import os

def check_statuses():
    """Check order statuses"""
    db_path = os.path.join('lectures', 'week_10', 'SQLAgent', 'sql_agent_class.db')
    
    print("🔍 Checking Order Statuses...")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check order statuses
    print("📊 Order statuses in database:")
    cursor.execute('SELECT DISTINCT status FROM orders')
    statuses = cursor.fetchall()
    for status in statuses:
        print(f"  {status['status']}")
    
    print("\n📈 Orders by status:")
    cursor.execute('SELECT status, COUNT(*) as count FROM orders GROUP BY status')
    status_counts = cursor.fetchall()
    for status in status_counts:
        print(f"  {status['status']}: {status['count']} orders")
    
    # Check what happens with 'paid' status
    print("\n🔍 Orders with 'paid' status:")
    cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'paid'")
    paid_count = cursor.fetchone()['count']
    print(f"  Paid orders: {paid_count}")
    
    # Check what happens with 'delivered' status
    print("\n🔍 Orders with 'delivered' status:")
    cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'delivered'")
    delivered_count = cursor.fetchone()['count']
    print(f"  Delivered orders: {delivered_count}")
    
    conn.close()

if __name__ == "__main__":
    check_statuses()
