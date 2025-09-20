# 🚀 Quick Setup Guide

## Step 1: Install Node.js
If you don't have Node.js installed:
1. Go to [nodejs.org](https://nodejs.org/)
2. Download the LTS version (recommended)
3. Run the installer and follow the setup wizard
4. Verify installation by opening terminal/command prompt and running:
   ```bash
   node --version
   npm --version
   ```

## Step 2: Install Dependencies
Open terminal/command prompt in the project directory and run:
```bash
npm install
```

This will install all required packages:
- React 18
- Chart.js for visualizations
- Webpack for bundling
- Babel for JavaScript compilation
- And other development dependencies

## Step 3: Start the Application
```bash
npm start
```

The application will:
- Start a development server on port 3000
- Automatically open your browser
- Show the Interactive Prompt Responder interface

## Step 4: Try It Out!
1. **Enter a prompt** in the text area (try "Show me weather data")
2. **Click Submit** or press Enter
3. **Watch the magic** - you'll get both text and visual responses!

## Troubleshooting

### Port 3000 Already in Use
If you get an error about port 3000 being in use:
```bash
# Kill any process using port 3000
npx kill-port 3000
# Then try again
npm start
```

### Permission Errors (Windows)
Run command prompt as Administrator if you encounter permission issues.

### Dependencies Won't Install
Try clearing npm cache:
```bash
npm cache clean --force
npm install
```

### Browser Doesn't Open Automatically
Manually navigate to: `http://localhost:3000`

## What You'll See

✅ **Beautiful gradient background**
✅ **Clean, modern interface**
✅ **Interactive prompt input**
✅ **Real-time text responses**
✅ **Dynamic charts and visualizations**
✅ **Mobile-responsive design**

## Next Steps

- Try different prompts to see various responses
- Explore the chart interactions (hover, click, expand)
- Copy text responses to clipboard
- Download charts as images
- Customize the styling and add your own features!

---

**Need help?** Check the main README.md for detailed documentation and troubleshooting tips.
