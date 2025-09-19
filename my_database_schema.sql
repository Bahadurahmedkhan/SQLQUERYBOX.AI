-- Custom Database Schema for Your Data
-- This schema is designed to be flexible and can be customized for your specific needs

PRAGMA foreign_keys = ON;

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS refunds;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- Core Business Tables
-- You can modify these tables to match your specific business domain

CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  phone TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT,
  region TEXT,
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
  notes TEXT
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  category TEXT,
  subcategory TEXT,
  price_cents INTEGER NOT NULL,
  cost_cents INTEGER,
  sku TEXT UNIQUE,
  stock_quantity INTEGER DEFAULT 0,
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'discontinued', 'out_of_stock')),
  created_at TEXT NOT NULL,
  updated_at TEXT
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  order_number TEXT UNIQUE NOT NULL,
  order_date TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled', 'refunded')),
  total_amount_cents INTEGER NOT NULL,
  shipping_address TEXT,
  billing_address TEXT,
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT,
  FOREIGN KEY(customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price_cents INTEGER NOT NULL,
  total_price_cents INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(order_id) REFERENCES orders(id),
  FOREIGN KEY(product_id) REFERENCES products(id)
);

CREATE TABLE payments (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  amount_cents INTEGER NOT NULL,
  payment_method TEXT NOT NULL CHECK (payment_method IN ('credit_card', 'debit_card', 'paypal', 'bank_transfer', 'cash', 'cryptocurrency')),
  transaction_id TEXT,
  paid_at TEXT,
  status TEXT NOT NULL CHECK (status IN ('pending', 'succeeded', 'failed', 'refunded', 'cancelled')),
  gateway TEXT,
  notes TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(order_id) REFERENCES orders(id)
);

CREATE TABLE refunds (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  amount_cents INTEGER NOT NULL,
  reason TEXT,
  refunded_at TEXT NOT NULL,
  status TEXT DEFAULT 'completed' CHECK (status IN ('pending', 'completed', 'failed')),
  notes TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(order_id) REFERENCES orders(id)
);

-- Additional useful tables for business analytics

CREATE TABLE categories (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  parent_id INTEGER,
  created_at TEXT NOT NULL,
  FOREIGN KEY(parent_id) REFERENCES categories(id)
);

CREATE TABLE inventory_movements (
  id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL,
  movement_type TEXT NOT NULL CHECK (movement_type IN ('in', 'out', 'adjustment', 'return')),
  quantity INTEGER NOT NULL,
  reason TEXT,
  reference_id INTEGER, -- Can reference order_id, etc.
  created_at TEXT NOT NULL,
  FOREIGN KEY(product_id) REFERENCES products(id)
);

CREATE TABLE customer_segments (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  criteria TEXT, -- JSON or text description of segment criteria
  created_at TEXT NOT NULL
);

-- Indexes for better performance
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_region ON customers(region);
CREATE INDEX idx_customers_created_at ON customers(created_at);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_refunds_order_id ON refunds(order_id);

-- Sample data for testing (you can replace this with your own data)
-- Customers
INSERT INTO customers (id, name, email, phone, created_at, region, status) VALUES
(1, 'John Smith', 'john.smith@example.com', '+1-555-0101', '2024-01-15', 'North America', 'active'),
(2, 'Sarah Johnson', 'sarah.j@example.com', '+1-555-0102', '2024-02-03', 'North America', 'active'),
(3, 'Ahmed Hassan', 'ahmed.h@example.com', '+20-555-0103', '2024-03-20', 'Middle East', 'active'),
(4, 'Maria Garcia', 'maria.g@example.com', '+34-555-0104', '2024-04-11', 'Europe', 'active'),
(5, 'Li Wei', 'li.wei@example.com', '+86-555-0105', '2024-05-05', 'Asia Pacific', 'active'),
(6, 'Emma Wilson', 'emma.w@example.com', '+44-555-0106', '2024-06-25', 'Europe', 'active');

-- Categories
INSERT INTO categories (id, name, description, created_at) VALUES
(1, 'Electronics', 'Electronic devices and accessories', '2024-01-01'),
(2, 'Clothing', 'Apparel and fashion items', '2024-01-01'),
(3, 'Home & Garden', 'Home improvement and garden supplies', '2024-01-01'),
(4, 'Books', 'Books and educational materials', '2024-01-01'),
(5, 'Sports', 'Sports equipment and accessories', '2024-01-01');

-- Products
INSERT INTO products (id, name, description, category, subcategory, price_cents, cost_cents, sku, stock_quantity, created_at) VALUES
(1, 'Wireless Headphones', 'High-quality wireless Bluetooth headphones', 'Electronics', 'Audio', 12999, 8000, 'WH-001', 50, '2024-01-01'),
(2, 'Smartphone Case', 'Protective case for latest smartphones', 'Electronics', 'Accessories', 2999, 1500, 'SC-001', 100, '2024-01-01'),
(3, 'Cotton T-Shirt', 'Comfortable 100% cotton t-shirt', 'Clothing', 'Tops', 1999, 800, 'CT-001', 200, '2024-01-01'),
(4, 'Running Shoes', 'Professional running shoes for athletes', 'Sports', 'Footwear', 8999, 4500, 'RS-001', 75, '2024-01-01'),
(5, 'Coffee Maker', 'Automatic drip coffee maker', 'Home & Garden', 'Kitchen', 5999, 3000, 'CM-001', 30, '2024-01-01'),
(6, 'Programming Book', 'Learn Python programming fundamentals', 'Books', 'Technology', 3999, 2000, 'PB-001', 150, '2024-01-01');

-- Orders
INSERT INTO orders (id, customer_id, order_number, order_date, status, total_amount_cents, shipping_address, created_at) VALUES
(101, 1, 'ORD-2024-001', '2024-06-30', 'delivered', 15998, '123 Main St, New York, NY 10001', '2024-06-30'),
(102, 1, 'ORD-2024-002', '2024-07-02', 'delivered', 12999, '123 Main St, New York, NY 10001', '2024-07-02'),
(103, 2, 'ORD-2024-003', '2024-07-10', 'refunded', 8999, '456 Oak Ave, Los Angeles, CA 90210', '2024-07-10'),
(104, 3, 'ORD-2024-004', '2024-07-14', 'delivered', 2999, '789 Palm St, Cairo, Egypt', '2024-07-14'),
(105, 4, 'ORD-2024-005', '2024-07-20', 'shipped', 1999, '321 Elm St, Madrid, Spain', '2024-07-20'),
(106, 4, 'ORD-2024-006', '2024-08-01', 'delivered', 10998, '321 Elm St, Madrid, Spain', '2024-08-01'),
(107, 5, 'ORD-2024-007', '2024-08-03', 'delivered', 17998, '654 Pine St, Beijing, China', '2024-08-03'),
(108, 6, 'ORD-2024-008', '2024-08-05', 'delivered', 5999, '987 Maple St, London, UK', '2024-08-05');

-- Order Items
INSERT INTO order_items (id, order_id, product_id, quantity, unit_price_cents, total_price_cents, created_at) VALUES
(3001, 101, 1, 1, 12999, 12999, '2024-06-30'),
(3002, 101, 2, 1, 2999, 2999, '2024-06-30'),
(3003, 102, 1, 1, 12999, 12999, '2024-07-02'),
(3004, 103, 4, 1, 8999, 8999, '2024-07-10'),
(3005, 104, 2, 1, 2999, 2999, '2024-07-14'),
(3006, 105, 3, 1, 1999, 1999, '2024-07-20'),
(3007, 106, 1, 1, 12999, 12999, '2024-08-01'),
(3008, 106, 2, 1, 2999, 2999, '2024-08-01'),
(3009, 107, 1, 1, 12999, 12999, '2024-08-03'),
(3010, 107, 5, 1, 5999, 5999, '2024-08-03'),
(3011, 108, 5, 1, 5999, 5999, '2024-08-05');

-- Payments
INSERT INTO payments (id, order_id, amount_cents, payment_method, transaction_id, paid_at, status, gateway, created_at) VALUES
(1001, 101, 15998, 'credit_card', 'txn_001', '2024-06-30', 'succeeded', 'stripe', '2024-06-30'),
(1002, 102, 12999, 'credit_card', 'txn_002', '2024-07-02', 'succeeded', 'stripe', '2024-07-02'),
(1003, 103, 8999, 'credit_card', 'txn_003', '2024-07-10', 'refunded', 'stripe', '2024-07-10'),
(1004, 104, 2999, 'paypal', 'pp_001', '2024-07-14', 'succeeded', 'paypal', '2024-07-14'),
(1005, 105, 1999, 'credit_card', 'txn_004', '2024-07-20', 'succeeded', 'stripe', '2024-07-20'),
(1006, 106, 10998, 'credit_card', 'txn_005', '2024-08-01', 'succeeded', 'stripe', '2024-08-01'),
(1007, 107, 17998, 'credit_card', 'txn_006', '2024-08-03', 'succeeded', 'stripe', '2024-08-03'),
(1008, 108, 5999, 'paypal', 'pp_002', '2024-08-05', 'succeeded', 'paypal', '2024-08-05');

-- Refunds
INSERT INTO refunds (id, order_id, amount_cents, reason, refunded_at, created_at) VALUES
(2001, 103, 8999, 'Customer requested return due to size issue', '2024-07-12', '2024-07-12');

-- Inventory Movements
INSERT INTO inventory_movements (id, product_id, movement_type, quantity, reason, reference_id, created_at) VALUES
(1, 1, 'in', 100, 'Initial stock', NULL, '2024-01-01'),
(2, 2, 'in', 200, 'Initial stock', NULL, '2024-01-01'),
(3, 3, 'in', 300, 'Initial stock', NULL, '2024-01-01'),
(4, 4, 'in', 150, 'Initial stock', NULL, '2024-01-01'),
(5, 5, 'in', 50, 'Initial stock', NULL, '2024-01-01'),
(6, 6, 'in', 200, 'Initial stock', NULL, '2024-01-01'),
(7, 1, 'out', 3, 'Order fulfillment', 101, '2024-06-30'),
(8, 2, 'out', 2, 'Order fulfillment', 101, '2024-06-30'),
(9, 1, 'out', 1, 'Order fulfillment', 102, '2024-07-02'),
(10, 4, 'out', 1, 'Order fulfillment', 103, '2024-07-10'),
(11, 4, 'in', 1, 'Return from order', 103, '2024-07-12');

-- Customer Segments
INSERT INTO customer_segments (id, name, description, criteria, created_at) VALUES
(1, 'High Value Customers', 'Customers with total orders > $100', 'total_spent > 10000', '2024-01-01'),
(2, 'Frequent Buyers', 'Customers with 3+ orders', 'order_count >= 3', '2024-01-01'),
(3, 'New Customers', 'Customers who joined in the last 30 days', 'created_at >= date("now", "-30 days")', '2024-01-01'),
(4, 'International Customers', 'Customers outside North America', 'region != "North America"', '2024-01-01');
