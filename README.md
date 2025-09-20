# Interactive Prompt Responder

A powerful React.js web application that allows users to enter prompts and receive both text and graphical responses. Built with modern web technologies and beautiful UI design.

## Features

🎯 **Interactive Prompt Input**
- Clean, intuitive text area for entering prompts
- Real-time character count
- Keyboard shortcuts (Enter to submit, Shift+Enter for new line)
- Loading states and validation

📝 **Intelligent Text Responses**
- AI-powered text generation based on prompt content
- Formatted responses with emojis and structured content
- Copy-to-clipboard functionality
- Word count and response metadata

📊 **Dynamic Visualizations**
- Interactive charts using Chart.js
- Multiple chart types: Bar, Line, Doughnut
- Expandable/collapsible chart view
- Download charts as PNG images
- Responsive design for all screen sizes

🎨 **Modern UI/UX**
- Beautiful gradient backgrounds
- Glass-morphism design elements
- Smooth animations and transitions
- Mobile-responsive layout
- Professional color scheme

## Quick Start

### Prerequisites
- Node.js (version 14 or higher)
- Python 3.7 or higher
- npm or yarn package manager

### Installation

1. **Clone or download the project files**
   ```bash
   # If you have the files in a directory, navigate to it
   cd interactive-prompt-responder
   ```

2. **Start both servers (Recommended)**
   ```bash
   python start_both.py
   ```
   This will start both the Flask backend (port 5000) and React frontend (port 3000) automatically.

3. **Alternative: Start servers separately**
   
   **Backend only:**
   ```bash
   python start_backend.py
   ```
   
   **Frontend only:**
   ```bash
   python start_frontend.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:3000`
   - The application will automatically open in your default browser
   - The backend API will be available at `http://localhost:5000`

### Build for Production

```bash
npm run build
```

This creates a `dist` folder with optimized production files.

## Usage

### Entering Prompts

1. **Type your prompt** in the text area
2. **Press Enter** to submit (or click the Submit button)
3. **Wait for processing** - the system will generate both text and visual responses
4. **View results** in the response section below

### Example Prompts

Try these sample prompts to see the system in action with **real database data**:

- **Sales Analysis**: "Show me sales performance and revenue data"
- **Customer Analysis**: "Analyze customer demographics and regions"
- **Product Analysis**: "What are the best selling products?"
- **Order Analysis**: "Show me order trends and status distribution"
- **General Analytics**: "Give me a business overview and key metrics"

The system will automatically detect the type of analysis you want and provide relevant data from the actual database!

### Features Overview

#### Text Responses
- Comprehensive analysis based on your prompt
- Structured information with headers and bullet points
- Copy functionality for easy sharing
- Word count and generation metadata

#### Visual Responses
- Interactive charts that respond to your prompt content
- Multiple visualization types (bar, line, doughnut charts)
- Expandable view for detailed analysis
- Download capability for saving charts
- Hover tooltips and interactive legends

## Technology Stack

### Frontend
- **React 18** - Modern React with hooks
- **Chart.js** - Powerful charting library
- **React-Chartjs-2** - React wrapper for Chart.js
- **Lucide React** - Beautiful icon library
- **Webpack** - Module bundler
- **Babel** - JavaScript compiler
- **CSS3** - Modern styling with gradients and animations

### Backend
- **Flask** - Python web framework
- **SQLite** - Database for storing business data
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite3** - Database connectivity

## Project Structure

```
interactive-prompt-responder/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/
│   │   ├── PromptInput.js  # Input component
│   │   ├── TextResponse.js # Text display component
│   │   └── GraphicalResponse.js # Chart component
│   ├── App.js              # Main application component
│   ├── index.js            # React entry point
│   └── index.css           # Global styles
├── lectures/week_10/SQLAgent/
│   └── sql_agent_class.db  # SQLite database with real data
├── package.json            # Frontend dependencies
├── webpack.config.js       # Webpack configuration
├── start_backend.py        # Backend startup script
├── start_frontend.py       # Frontend startup script
├── start_both.py           # Start both servers
└── README.md              # This file
```

## Customization

### Adding New Chart Types

1. Import the new chart type in `GraphicalResponse.js`
2. Register it with Chart.js
3. Add a case in the `renderChart()` function
4. Update the `generateGraphicalData()` function in `App.js`

### Modifying Response Generation

Edit the `generateTextResponse()` and `generateGraphicalData()` functions in `App.js` to customize how the system responds to different types of prompts.

### Styling Changes

- Global styles: `src/index.css`
- Component-specific styles: Inline styles in each component
- Color scheme: Modify the gradient values in CSS

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- Optimized bundle size with Webpack
- Lazy loading for chart components
- Responsive images and efficient rendering
- Smooth 60fps animations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

If you encounter any issues or have questions:

1. Check the browser console for errors
2. Ensure all dependencies are installed correctly
3. Verify Node.js version compatibility
4. Try clearing browser cache and restarting the dev server

---

**Enjoy building amazing interactive experiences! 🚀**
