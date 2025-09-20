#!/usr/bin/env python3
"""
Flask Backend API for Interactive Prompt Responder
Serves real database data to the React frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'lectures', 'week_10', 'SQLAgent', 'sql_agent_class.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def cents_to_dollars(cents):
    """Convert cents to dollars"""
    return cents / 100 if cents else 0

def analyze_prompt(prompt):
    """Analyze the prompt to determine what type of data to fetch"""
    prompt_lower = prompt.lower()
    
    # Time-based queries (most specific first)
    if any(word in prompt_lower for word in ['january', 'february', 'march', 'april', 'may', 'june', 
                                           'july', 'august', 'september', 'october', 'november', 'december',
                                           '2024', '2025', 'month', 'year', 'date', 'when', 'purchased in', 'bought in']):
        return 'time_based'
    
    # Customer-specific queries
    if any(word in prompt_lower for word in ['customer', 'user', 'client', 'demographic', 'region', 'purchased', 'bought', 'how many customers']):
        return 'customers'
    
    # Sales and revenue analysis
    if any(word in prompt_lower for word in ['sales', 'revenue', 'profit', 'income', 'earnings', 'total']):
        return 'sales'
    
    # Product analysis
    if any(word in prompt_lower for word in ['product', 'item', 'inventory', 'stock', 'category', 'selling', 'best selling']):
        return 'products'
    
    # Order analysis
    if any(word in prompt_lower for word in ['order', 'purchase', 'transaction', 'payment']):
        return 'orders'
    
    # General analytics
    if any(word in prompt_lower for word in ['analytics', 'data', 'statistics', 'report', 'summary', 'overview']):
        return 'analytics'
    
    # Default to general analytics
    return 'analytics'

@app.route('/api/analyze', methods=['POST'])
def analyze_prompt_endpoint():
    """Main endpoint for prompt analysis"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        analysis_type = analyze_prompt(prompt)
        
        # Get data based on analysis type
        if analysis_type == 'time_based':
            text_response, chart_data = get_time_based_analysis(prompt)
        elif analysis_type == 'sales':
            text_response, chart_data = get_sales_analysis(prompt)
        elif analysis_type == 'customers':
            text_response, chart_data = get_customer_analysis(prompt)
        elif analysis_type == 'products':
            text_response, chart_data = get_product_analysis(prompt)
        elif analysis_type == 'orders':
            text_response, chart_data = get_order_analysis(prompt)
        else:
            text_response, chart_data = get_general_analytics(prompt)
        
        return jsonify({
            'textResponse': text_response,
            'chartData': chart_data,
            'analysisType': analysis_type,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_time_based_analysis(prompt):
    """Get time-based analysis based on specific prompt"""
    conn = get_db_connection()
    prompt_lower = prompt.lower()
    
    try:
        # Extract time information from prompt
        month = None
        year = None
        
        # Check for specific months
        months = {
            'january': '01', 'february': '02', 'march': '03', 'april': '04',
            'may': '05', 'june': '06', 'july': '07', 'august': '08',
            'september': '09', 'october': '10', 'november': '11', 'december': '12'
        }
        
        for month_name, month_num in months.items():
            if month_name in prompt_lower:
                month = month_num
                break
        
        # Check for years
        if '2024' in prompt_lower:
            year = '2024'
        elif '2025' in prompt_lower:
            year = '2025'
        
        # Build date filter
        date_filter = ""
        if year and month:
            date_filter = f"AND strftime('%Y-%m', o.order_date) = '{year}-{month}'"
        elif year:
            date_filter = f"AND strftime('%Y', o.order_date) = '{year}'"
        elif month:
            date_filter = f"AND strftime('%m', o.order_date) = '{month:0>2}'"
        
        # Handle specific queries
        if 'customer' in prompt_lower and ('purchased' in prompt_lower or 'bought' in prompt_lower):
            # Query: "How many customers purchased something in January 2024?"
            query = f"""
                SELECT COUNT(DISTINCT c.id) as customer_count,
                       COUNT(DISTINCT o.id) as order_count,
                       SUM(oi.quantity * oi.unit_price_cents) as total_revenue
                FROM customers c
                JOIN orders o ON c.id = o.customer_id
                JOIN order_items oi ON o.id = oi.order_id
                WHERE o.status IN ('delivered', 'shipped') {date_filter}
            """
            
            result = conn.execute(query).fetchone()
            
            time_period = f"{month_name.title()} {year}" if month and year else f"{year}" if year else "specified period"
            
            # Check if we have data for this period
            if result['customer_count'] == 0:
                # No data for this period - show available data
                available_dates_query = """
                    SELECT DISTINCT strftime('%Y-%m', order_date) as month_year,
                           COUNT(DISTINCT customer_id) as customers,
                           COUNT(*) as orders
                    FROM orders 
                    WHERE status IN ('delivered', 'shipped')
                    GROUP BY strftime('%Y-%m', order_date)
                    ORDER BY month_year
                """
                available_data = conn.execute(available_dates_query).fetchall()
                
                text_response = f"""📅 Time-Based Customer Analysis

❌ No Data Found for {time_period}

🔍 Available Data in Database:
"""
                for row in available_data:
                    text_response += f"• {row['month_year']}: {row['customers']} customers, {row['orders']} orders\n"
                
                if available_data:
                    text_response += f"""
💡 The database contains order data from {available_data[0]['month_year']} to {available_data[-1]['month_year']}.

🎯 Try asking about:
• "How many customers purchased in {available_data[0]['month_year']}?"
• "Show me customer data for {available_data[-1]['month_year']}"
• "What's the overall customer purchase summary?"
"""
                else:
                    text_response += f"""
💡 No order data found in the database.

🎯 Try asking about:
• "What's the overall customer purchase summary?"
• "Show me all customers in the database"
• "What products are available?"
"""
                
                # Create chart showing available data
                chart_data = {
                    'type': 'bar',
                    'title': 'Available Data by Month',
                    'data': {
                        'labels': [row['month_year'] for row in available_data],
                        'datasets': [{
                            'label': 'Customers',
                            'data': [row['customers'] for row in available_data],
                            'backgroundColor': 'rgba(54, 162, 235, 0.8)',
                            'borderColor': 'rgba(54, 162, 235, 1)',
                            'borderWidth': 2
                        }]
                    }
                }
            else:
                # We have data - show the analysis
                text_response = f"""📅 Time-Based Customer Analysis

🛒 Customer Purchase Activity for {time_period}:

👥 Total Customers Who Purchased: {result['customer_count']}
📦 Total Orders Placed: {result['order_count']}
💰 Total Revenue Generated: ${cents_to_dollars(result['total_revenue'] or 0):,.2f}

📊 Analysis:
• Average orders per customer: {result['order_count'] / result['customer_count']:.1f} orders
• Average revenue per customer: ${cents_to_dollars(result['total_revenue'] or 0) / result['customer_count']:,.2f}
• Average order value: ${cents_to_dollars(result['total_revenue'] or 0) / result['order_count']:,.2f}

💡 This data shows customer engagement and purchasing behavior during the specified time period."""
                
                # Get daily breakdown for chart
                daily_query = f"""
                    SELECT strftime('%d', o.order_date) as day,
                           COUNT(DISTINCT c.id) as customers,
                           COUNT(DISTINCT o.id) as orders
                    FROM customers c
                    JOIN orders o ON c.id = o.customer_id
                    WHERE o.status IN ('delivered', 'shipped') {date_filter}
                    GROUP BY strftime('%d', o.order_date)
                    ORDER BY day
                """
                
                daily_data = conn.execute(daily_query).fetchall()
                
                chart_data = {
                    'type': 'line',
                    'title': f'Customer Activity - {time_period}',
                    'data': {
                        'labels': [f"Day {row['day']}" for row in daily_data],
                        'datasets': [
                            {
                                'label': 'Customers',
                                'data': [row['customers'] for row in daily_data],
                                'borderColor': 'rgb(75, 192, 192)',
                                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                                'tension': 0.4
                            },
                            {
                                'label': 'Orders',
                                'data': [row['orders'] for row in daily_data],
                                'borderColor': 'rgb(255, 99, 132)',
                                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                                'tension': 0.4
                            }
                        ]
                    }
                }
            
        elif 'revenue' in prompt_lower or 'sales' in prompt_lower:
            # Query: "What was the revenue in January 2024?"
            query = f"""
                SELECT 
                    COUNT(DISTINCT o.id) as order_count,
                    SUM(oi.quantity * oi.unit_price_cents) as total_revenue,
                    AVG(oi.quantity * oi.unit_price_cents) as avg_order_value
                FROM orders o
                JOIN order_items oi ON o.id = oi.order_id
                WHERE o.status IN ('delivered', 'shipped') {date_filter}
            """
            
            result = conn.execute(query).fetchone()
            
            time_period = f"{month_name.title()} {year}" if month and year else f"{year}" if year else "specified period"
            
            # Check if we have data for this period
            if result['order_count'] == 0:
                # No data for this period - show available data
                available_dates_query = """
                    SELECT DISTINCT strftime('%Y-%m', order_date) as month_year,
                           COUNT(*) as orders,
                           SUM(oi.quantity * oi.unit_price_cents) as revenue
                    FROM orders o
                    JOIN order_items oi ON o.id = oi.order_id
                    WHERE o.status IN ('delivered', 'shipped')
                    GROUP BY strftime('%Y-%m', order_date)
                    ORDER BY month_year
                """
                available_data = conn.execute(available_dates_query).fetchall()
                
                text_response = f"""💰 Revenue Analysis

❌ No Revenue Data Found for {time_period}

🔍 Available Revenue Data in Database:
"""
                for row in available_data:
                    text_response += f"• {row['month_year']}: {row['orders']} orders, ${cents_to_dollars(row['revenue']):,.2f} revenue\n"
                
                if available_data:
                    text_response += f"""
💡 The database contains revenue data from {available_data[0]['month_year']} to {available_data[-1]['month_year']}.

🎯 Try asking about:
• "What was the revenue in {available_data[0]['month_year']}?"
• "Show me sales data for {available_data[-1]['month_year']}"
• "What's the total revenue across all periods?"
"""
                else:
                    text_response += f"""
💡 No revenue data found in the database.

🎯 Try asking about:
• "What's the total revenue across all periods?"
• "Show me all products in the database"
• "What's the overall business summary?"
"""
                
                # Create chart showing available revenue data
                chart_data = {
                    'type': 'bar',
                    'title': 'Available Revenue Data by Month',
                    'data': {
                        'labels': [row['month_year'] for row in available_data],
                        'datasets': [{
                            'label': 'Revenue ($)',
                            'data': [cents_to_dollars(row['revenue']) for row in available_data],
                            'backgroundColor': 'rgba(34, 197, 94, 0.8)',
                            'borderColor': 'rgba(34, 197, 94, 1)',
                            'borderWidth': 2
                        }]
                    }
                }
            else:
                # We have data - show the analysis
                text_response = f"""💰 Revenue Analysis for {time_period}

📊 Financial Performance:
• Total Revenue: ${cents_to_dollars(result['total_revenue'] or 0):,.2f}
• Total Orders: {result['order_count']}
• Average Order Value: ${cents_to_dollars(result['avg_order_value'] or 0):,.2f}

📈 Key Insights:
• Revenue per day: ${cents_to_dollars(result['total_revenue'] or 0) / 30:,.2f} (estimated)
• Order frequency: {result['order_count']} orders in the period
• Customer spending pattern analysis available"""
                
                # Get product breakdown
                product_query = f"""
                    SELECT p.name, SUM(oi.quantity) as units_sold, SUM(oi.quantity * oi.unit_price_cents) as revenue
                    FROM products p
                    JOIN order_items oi ON p.id = oi.product_id
                    JOIN orders o ON oi.order_id = o.id
                    WHERE o.status IN ('delivered', 'shipped') {date_filter}
                    GROUP BY p.id, p.name
                    ORDER BY revenue DESC
                    LIMIT 5
                """
                
                product_data = conn.execute(product_query).fetchall()
                
                chart_data = {
                    'type': 'bar',
                    'title': f'Top Products by Revenue - {time_period}',
                    'data': {
                        'labels': [row['name'] for row in product_data],
                        'datasets': [{
                            'label': 'Revenue ($)',
                            'data': [cents_to_dollars(row['revenue']) for row in product_data],
                            'backgroundColor': 'rgba(34, 197, 94, 0.8)',
                            'borderColor': 'rgba(34, 197, 94, 1)',
                            'borderWidth': 2
                        }]
                    }
                }
            
            # Get product breakdown
            product_query = f"""
                SELECT p.name, SUM(oi.quantity) as units_sold, SUM(oi.quantity * oi.unit_price_cents) as revenue
                FROM products p
                JOIN order_items oi ON p.id = oi.product_id
                JOIN orders o ON oi.order_id = o.id
                WHERE o.status IN ('delivered', 'shipped') {date_filter}
                GROUP BY p.id, p.name
                ORDER BY revenue DESC
                LIMIT 5
            """
            
            product_data = conn.execute(product_query).fetchall()
            
            chart_data = {
                'type': 'bar',
                'title': f'Top Products by Revenue - {time_period}',
                'data': {
                    'labels': [row['name'] for row in product_data],
                    'datasets': [{
                        'label': 'Revenue ($)',
                        'data': [cents_to_dollars(row['revenue']) for row in product_data],
                        'backgroundColor': 'rgba(54, 162, 235, 0.8)',
                        'borderColor': 'rgba(54, 162, 235, 1)',
                        'borderWidth': 2
                    }]
                }
            }
            
        else:
            # General time-based analysis
            query = f"""
                SELECT 
                    COUNT(DISTINCT c.id) as customers,
                    COUNT(DISTINCT o.id) as orders,
                    COUNT(DISTINCT p.id) as products_sold,
                    SUM(oi.quantity * oi.unit_price_cents) as revenue
                FROM customers c
                JOIN orders o ON c.id = o.customer_id
                JOIN order_items oi ON o.id = oi.order_id
                JOIN products p ON oi.product_id = p.id
                WHERE o.status IN ('delivered', 'shipped') {date_filter}
            """
            
            result = conn.execute(query).fetchone()
            
            time_period = f"{month_name.title()} {year}" if month and year else f"{year}" if year else "specified period"
            
            text_response = f"""📅 Business Activity for {time_period}

📊 Key Metrics:
• Active Customers: {result['customers']}
• Total Orders: {result['orders']}
• Products Sold: {result['products_sold']}
• Total Revenue: ${cents_to_dollars(result['revenue'] or 0):,.2f}

📈 Performance Indicators:
• Orders per customer: {result['orders'] / result['customers']:.1f}
• Revenue per customer: ${cents_to_dollars(result['revenue'] or 0) / result['customers']:,.2f}
• Average order value: ${cents_to_dollars(result['revenue'] or 0) / result['orders']:,.2f}"""
            
            chart_data = {
                'type': 'doughnut',
                'title': f'Activity Breakdown - {time_period}',
                'data': {
                    'labels': ['Customers', 'Orders', 'Products'],
                    'datasets': [{
                        'data': [result['customers'], result['orders'], result['products_sold']],
                        'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56'],
                        'borderWidth': 2,
                        'borderColor': '#fff'
                    }]
                }
            }
        
        return text_response, chart_data
        
    finally:
        conn.close()

def get_sales_analysis(prompt=""):
    """Get sales analysis data"""
    conn = get_db_connection()
    
    try:
        # Total revenue
        total_revenue = conn.execute("""
            SELECT SUM(oi.quantity * oi.unit_price_cents) as total_revenue
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE o.status IN ('delivered', 'shipped')
        """).fetchone()['total_revenue'] or 0
        
        # Revenue by region
        revenue_by_region = conn.execute("""
            SELECT c.region, SUM(oi.quantity * oi.unit_price_cents) as revenue
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            JOIN customers c ON o.customer_id = c.id
            WHERE o.status IN ('delivered', 'shipped')
            GROUP BY c.region
            ORDER BY revenue DESC
        """).fetchall()
        
        # Top selling products
        top_products = conn.execute("""
            SELECT p.name, SUM(oi.quantity) as total_sold, SUM(oi.quantity * oi.unit_price_cents) as revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            JOIN orders o ON oi.order_id = o.id
            WHERE o.status IN ('delivered', 'shipped')
            GROUP BY p.id, p.name
            ORDER BY total_sold DESC
            LIMIT 5
        """).fetchall()
        
        # Monthly revenue trend
        monthly_revenue = conn.execute("""
            SELECT strftime('%Y-%m', o.order_date) as month, 
                   SUM(oi.quantity * oi.unit_price_cents) as revenue
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE o.status IN ('delivered', 'shipped')
            GROUP BY strftime('%Y-%m', o.order_date)
            ORDER BY month
        """).fetchall()
        
        # Generate text response
        text_response = f"""📈 Sales Performance Analysis

💰 Total Revenue: ${cents_to_dollars(total_revenue):,.2f}

🌍 Revenue by Region:
"""
        for region in revenue_by_region:
            text_response += f"• {region['region']}: ${cents_to_dollars(region['revenue']):,.2f}\n"
        
        text_response += f"""
🏆 Top Selling Products:
"""
        for product in top_products:
            text_response += f"• {product['name']}: {product['total_sold']} units (${cents_to_dollars(product['revenue']):,.2f})\n"
        
        # Generate chart data
        chart_data = {
            'type': 'bar',
            'title': 'Revenue by Region',
            'data': {
                'labels': [region['region'] for region in revenue_by_region],
                'datasets': [{
                    'label': 'Revenue ($)',
                    'data': [cents_to_dollars(region['revenue']) for region in revenue_by_region],
                    'backgroundColor': [
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)'
                    ],
                    'borderColor': [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    'borderWidth': 2
                }]
            }
        }
        
        return text_response, chart_data
        
    finally:
        conn.close()

def get_customer_analysis(prompt=""):
    """Get customer analysis data"""
    conn = get_db_connection()
    prompt_lower = prompt.lower()
    
    try:
        # Customer count by region
        customers_by_region = conn.execute("""
            SELECT region, COUNT(*) as customer_count
            FROM customers
            GROUP BY region
            ORDER BY customer_count DESC
        """).fetchall()
        
        # Customer order statistics
        customer_stats = conn.execute("""
            SELECT 
                COUNT(DISTINCT c.id) as total_customers,
                COUNT(DISTINCT o.id) as total_orders,
                AVG(order_totals.total_amount) as avg_order_value
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id AND o.status = 'paid'
            LEFT JOIN (
                SELECT order_id, SUM(quantity * unit_price_cents) as total_amount
                FROM order_items
                GROUP BY order_id
            ) order_totals ON o.id = order_totals.order_id
        """).fetchone()
        
        # Top customers by spending
        top_customers = conn.execute("""
            SELECT c.name, c.region, SUM(oi.quantity * oi.unit_price_cents) as total_spent,
                   COUNT(DISTINCT o.id) as order_count
            FROM customers c
            JOIN orders o ON c.id = o.customer_id
            JOIN order_items oi ON o.id = oi.order_id
            WHERE o.status IN ('delivered', 'shipped')
            GROUP BY c.id, c.name, c.region
            ORDER BY total_spent DESC
            LIMIT 5
        """).fetchall()
        
        # Generate text response
        text_response = f"""👥 Customer Analysis

📊 Customer Overview:
• Total Customers: {customer_stats['total_customers']}
• Total Orders: {customer_stats['total_orders']}
• Average Order Value: ${cents_to_dollars(customer_stats['avg_order_value'] or 0):,.2f}

🌍 Customers by Region:
"""
        for region in customers_by_region:
            text_response += f"• {region['region']}: {region['customer_count']} customers\n"
        
        text_response += f"""
💎 Top Customers by Spending:
"""
        for customer in top_customers:
            text_response += f"• {customer['name']} ({customer['region']}): ${cents_to_dollars(customer['total_spent']):,.2f} ({customer['order_count']} orders)\n"
        
        # Add specific insights based on prompt
        if 'purchased' in prompt_lower or 'bought' in prompt_lower:
            text_response += f"""
🛒 Purchase Behavior:
• {customer_stats['total_customers']} customers have made purchases
• {customer_stats['total_orders']} total orders placed
• Average of {customer_stats['total_orders'] / customer_stats['total_customers']:.1f} orders per customer"""
        
        if 'region' in prompt_lower or 'demographic' in prompt_lower:
            text_response += f"""
🌍 Regional Distribution:
• {customers_by_region[0]['region']} has the most customers ({customers_by_region[0]['customer_count']})
• Regional diversity: {len(customers_by_region)} different regions represented"""
        
        # Generate chart data
        chart_data = {
            'type': 'doughnut',
            'title': 'Customer Distribution by Region',
            'data': {
                'labels': [region['region'] for region in customers_by_region],
                'datasets': [{
                    'data': [region['customer_count'] for region in customers_by_region],
                    'backgroundColor': [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF'
                    ],
                    'borderWidth': 2,
                    'borderColor': '#fff'
                }]
            }
        }
        
        return text_response, chart_data
        
    finally:
        conn.close()

def get_product_analysis(prompt=""):
    """Get product analysis data"""
    conn = get_db_connection()
    
    try:
        # Products by category
        products_by_category = conn.execute("""
            SELECT category, COUNT(*) as product_count, AVG(price_cents) as avg_price
            FROM products
            GROUP BY category
            ORDER BY product_count DESC
        """).fetchall()
        
        # Best selling products
        best_sellers = conn.execute("""
            SELECT p.name, p.category, SUM(oi.quantity) as total_sold, SUM(oi.quantity * oi.unit_price_cents) as revenue
            FROM products p
            JOIN order_items oi ON p.id = oi.product_id
            JOIN orders o ON oi.order_id = o.id
            WHERE o.status IN ('delivered', 'shipped')
            GROUP BY p.id, p.name, p.category
            ORDER BY total_sold DESC
            LIMIT 5
        """).fetchall()
        
        # Price analysis
        price_stats = conn.execute("""
            SELECT 
                MIN(price_cents) as min_price,
                MAX(price_cents) as max_price,
                AVG(price_cents) as avg_price,
                COUNT(*) as total_products
            FROM products
        """).fetchone()
        
        # Generate text response
        text_response = f"""🛍️ Product Analysis

📦 Product Overview:
• Total Products: {price_stats['total_products']}
• Price Range: ${cents_to_dollars(price_stats['min_price']):,.2f} - ${cents_to_dollars(price_stats['max_price']):,.2f}
• Average Price: ${cents_to_dollars(price_stats['avg_price']):,.2f}

📊 Products by Category:
"""
        for category in products_by_category:
            text_response += f"• {category['category']}: {category['product_count']} products (avg: ${cents_to_dollars(category['avg_price']):,.2f})\n"
        
        text_response += f"""
🏆 Best Selling Products:
"""
        for product in best_sellers:
            text_response += f"• {product['name']} ({product['category']}): {product['total_sold']} sold (${cents_to_dollars(product['revenue']):,.2f})\n"
        
        # Generate chart data
        chart_data = {
            'type': 'bar',
            'title': 'Products by Category',
            'data': {
                'labels': [category['category'] for category in products_by_category],
                'datasets': [{
                    'label': 'Number of Products',
                    'data': [category['product_count'] for category in products_by_category],
                    'backgroundColor': 'rgba(102, 126, 234, 0.8)',
                    'borderColor': 'rgba(102, 126, 234, 1)',
                    'borderWidth': 2
                }]
            }
        }
        
        return text_response, chart_data
        
    finally:
        conn.close()

def get_order_analysis(prompt=""):
    """Get order analysis data"""
    conn = get_db_connection()
    
    try:
        # Order status distribution
        order_status = conn.execute("""
            SELECT status, COUNT(*) as order_count
            FROM orders
            GROUP BY status
            ORDER BY order_count DESC
        """).fetchall()
        
        # Monthly order trend
        monthly_orders = conn.execute("""
            SELECT strftime('%Y-%m', order_date) as month, COUNT(*) as order_count
            FROM orders
            GROUP BY strftime('%Y-%m', order_date)
            ORDER BY month
        """).fetchall()
        
        # Average order value by status
        avg_order_value = conn.execute("""
            SELECT 
                o.status,
                COUNT(*) as order_count,
                AVG(order_totals.total_amount) as avg_value
            FROM orders o
            LEFT JOIN (
                SELECT order_id, SUM(quantity * unit_price_cents) as total_amount
                FROM order_items
                GROUP BY order_id
            ) order_totals ON o.id = order_totals.order_id
            GROUP BY o.status
            ORDER BY avg_value DESC
        """).fetchall()
        
        # Generate text response
        text_response = f"""📦 Order Analysis

📊 Order Status Distribution:
"""
        for status in order_status:
            text_response += f"• {status['status'].title()}: {status['order_count']} orders\n"
        
        text_response += f"""
💰 Average Order Value by Status:
"""
        for status in avg_order_value:
            if status['avg_value']:
                text_response += f"• {status['status'].title()}: ${cents_to_dollars(status['avg_value']):,.2f} ({status['order_count']} orders)\n"
        
        # Generate chart data
        chart_data = {
            'type': 'line',
            'title': 'Monthly Order Trend',
            'data': {
                'labels': [order['month'] for order in monthly_orders],
                'datasets': [{
                    'label': 'Number of Orders',
                    'data': [order['order_count'] for order in monthly_orders],
                    'borderColor': 'rgb(75, 192, 192)',
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'tension': 0.4
                }]
            }
        }
        
        return text_response, chart_data
        
    finally:
        conn.close()

def get_general_analytics(prompt=""):
    """Get general analytics data"""
    conn = get_db_connection()
    
    try:
        # Overall statistics
        stats = conn.execute("""
            SELECT 
                (SELECT COUNT(*) FROM customers) as total_customers,
                (SELECT COUNT(*) FROM products) as total_products,
                (SELECT COUNT(*) FROM orders) as total_orders,
                (SELECT SUM(oi.quantity * oi.unit_price_cents) FROM order_items oi JOIN orders o ON oi.order_id = o.id WHERE o.status = 'paid') as total_revenue
        """).fetchone()
        
        # Recent activity
        recent_orders = conn.execute("""
            SELECT o.id, c.name, o.order_date, o.status
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            ORDER BY o.order_date DESC
            LIMIT 5
        """).fetchall()
        
        # Generate text response
        text_response = f"""📊 General Analytics Dashboard

🎯 Key Metrics:
• Total Customers: {stats['total_customers']}
• Total Products: {stats['total_products']}
• Total Orders: {stats['total_orders']}
• Total Revenue: ${cents_to_dollars(stats['total_revenue'] or 0):,.2f}

📈 Recent Activity:
"""
        for order in recent_orders:
            text_response += f"• Order {order['id']}: {order['name']} - {order['order_date']} ({order['status']})\n"
        
        # Generate chart data
        chart_data = {
            'type': 'bar',
            'title': 'Business Overview',
            'data': {
                'labels': ['Customers', 'Products', 'Orders', 'Revenue ($)'],
                'datasets': [{
                    'label': 'Count/Value',
                    'data': [
                        stats['total_customers'],
                        stats['total_products'],
                        stats['total_orders'],
                        cents_to_dollars(stats['total_revenue'] or 0)
                    ],
                    'backgroundColor': [
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)'
                    ],
                    'borderColor': [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    'borderWidth': 2
                }]
            }
        }
        
        return text_response, chart_data
        
    finally:
        conn.close()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/database/info', methods=['GET'])
def database_info():
    """Get database information"""
    conn = get_db_connection()
    
    try:
        # Get table counts
        tables = ['customers', 'products', 'orders', 'order_items', 'payments', 'refunds']
        table_counts = {}
        
        for table in tables:
            count = conn.execute(f"SELECT COUNT(*) as count FROM {table}").fetchone()['count']
            table_counts[table] = count
        
        return jsonify({
            'database_path': DB_PATH,
            'table_counts': table_counts,
            'timestamp': datetime.now().isoformat()
        })
        
    finally:
        conn.close()

if __name__ == '__main__':
    print("🚀 Starting Flask backend server...")
    print(f"📁 Database path: {DB_PATH}")
    print("🌐 Server will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
