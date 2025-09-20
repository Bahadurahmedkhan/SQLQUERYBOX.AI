# 🚀 Complete Setup Guide

## Overview
This application now uses **real database data** instead of mock data! The system connects to a SQLite database containing actual business data (customers, products, orders, etc.) and provides intelligent analysis based on your prompts.

## Prerequisites

### Required Software
1. **Python 3.7+** - [Download here](https://www.python.org/downloads/)
2. **Node.js 14+** - [Download here](https://nodejs.org/)
3. **Git** (optional) - [Download here](https://git-scm.com/)

### Verify Installation
```bash
python --version    # Should show Python 3.7+
node --version      # Should show Node.js 14+
npm --version       # Should show npm version
```

## Quick Start (Recommended)

### Option 1: Start Both Servers Automatically
```bash
python start_both.py
```
This single command will:
- Install all Python dependencies
- Install all npm dependencies  
- Start the Flask backend (port 5000)
- Start the React frontend (port 3000)
- Open your browser automatically

### Option 2: Start Servers Separately

**Terminal 1 - Backend:**
```bash
python start_backend.py
```

**Terminal 2 - Frontend:**
```bash
python start_frontend.py
```

## Manual Setup (If needed)

### 1. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Node.js Dependencies
```bash
npm install
```

### 3. Start Backend Server
```bash
cd backend
python app.py
```

### 4. Start Frontend Server (New Terminal)
```bash
npm start
```

## Database Setup

The application uses the existing SQLite database at:
```
lectures/week_10/SQLAgent/sql_agent_class.db
```

### Database Contents
- **Customers**: 6 customers across different regions
- **Products**: 6 products in various categories
- **Orders**: 12 orders with different statuses
- **Payments**: Payment records with different methods
- **Order Items**: Detailed order line items

### Verify Database
You can check the database contents by running:
```bash
cd lectures/week_10/SQLAgent
python setup_my_database.py
```

## Testing the Application

### 1. Open the Application
Navigate to: `http://localhost:3000`

### 2. Try These Real Data Prompts

**Sales Analysis:**
- "Show me sales performance and revenue data"
- "What's our total revenue?"
- "Analyze sales by region"

**Customer Analysis:**
- "Show me customer demographics"
- "How many customers do we have by region?"
- "Who are our top customers?"

**Product Analysis:**
- "What are our best selling products?"
- "Show me products by category"
- "What's our product inventory?"

**Order Analysis:**
- "Show me order trends"
- "What's the status of our orders?"
- "Analyze order patterns"

### 3. Verify Real Data
- Look for the "✅ Real Data" indicator in responses
- Charts should show actual numbers from the database
- Text responses should contain real customer names, product names, etc.

## Troubleshooting

### Backend Issues

**Port 5000 already in use:**
```bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9
# Or on Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Database not found:**
- Ensure the database file exists at `lectures/week_10/SQLAgent/sql_agent_class.db`
- Run `python setup_my_database.py` to create the database

**Python dependencies issues:**
```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### Frontend Issues

**Port 3000 already in use:**
```bash
# Kill process using port 3000
lsof -ti:3000 | xargs kill -9
# Or on Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**npm install fails:**
```bash
npm cache clean --force
npm install
```

**Module not found errors:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### API Connection Issues

**"Using mock data - API unavailable":**
- Ensure backend is running on port 5000
- Check browser console for CORS errors
- Verify Flask server started successfully

**CORS errors:**
- Backend includes Flask-CORS, should work automatically
- If issues persist, check firewall settings

## Development

### Adding New Analysis Types

1. **Backend**: Add new analysis function in `backend/app.py`
2. **Frontend**: Update prompt analysis logic in `src/App.js`

### Customizing Database Queries

Edit the SQL queries in `backend/app.py` functions:
- `get_sales_analysis()`
- `get_customer_analysis()`
- `get_product_analysis()`
- `get_order_analysis()`

### Adding New Chart Types

1. Import new chart type in `src/components/GraphicalResponse.js`
2. Register with Chart.js
3. Add rendering logic

## Production Deployment

### Build Frontend
```bash
npm run build
```

### Deploy Backend
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

## Support

### Common Issues
1. **Database path errors**: Ensure you're running from the correct directory
2. **Port conflicts**: Use different ports or kill existing processes
3. **Dependency issues**: Update pip/npm and reinstall dependencies

### Getting Help
1. Check the browser console for errors
2. Check the terminal output for backend errors
3. Verify all prerequisites are installed correctly
4. Ensure database file exists and is accessible

---

**🎉 You're all set! The application now uses real database data for intelligent analysis and visualization.**
