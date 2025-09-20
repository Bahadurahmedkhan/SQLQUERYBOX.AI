import React, { useState } from 'react';
import { Send, Loader } from 'lucide-react';

const PromptInput = ({ onSubmit, isLoading }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim() && !isLoading) {
      onSubmit(prompt.trim());
      setPrompt('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="card">
      <h2 style={{ 
        fontSize: '1.5rem', 
        marginBottom: '20px', 
        color: '#333',
        display: 'flex',
        alignItems: 'center',
        gap: '10px'
      }}>
        <Send size={24} />
        Enter Your Prompt
      </h2>
      
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '20px' }}>
          <textarea
            className="input textarea"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything! Try queries like:
• 'Show me weather data'
• 'Analyze sales performance' 
• 'User demographics breakdown'
• 'Create a data visualization'

Press Enter to submit, Shift+Enter for new line..."
            disabled={isLoading}
            style={{ 
              minHeight: '120px',
              fontFamily: 'inherit',
              fontSize: '16px',
              lineHeight: '1.5'
            }}
          />
        </div>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ fontSize: '0.9rem', color: '#666' }}>
            {prompt.length} characters
          </div>
          
          <button 
            type="submit" 
            className="btn"
            disabled={!prompt.trim() || isLoading}
            style={{ 
              minWidth: '140px',
              justifyContent: 'center'
            }}
          >
            {isLoading ? (
              <>
                <Loader className="loading" />
                Processing...
              </>
            ) : (
              <>
                <Send size={18} />
                Submit Prompt
              </>
            )}
          </button>
        </div>
      </form>
      
      <div style={{ 
        marginTop: '20px', 
        padding: '16px', 
        background: 'rgba(102, 126, 234, 0.1)', 
        borderRadius: '8px',
        border: '1px solid rgba(102, 126, 234, 0.2)'
      }}>
        <h4 style={{ 
          marginBottom: '10px', 
          color: '#667eea',
          fontSize: '1rem'
        }}>
          💡 Pro Tips:
        </h4>
        <ul style={{ 
          margin: 0, 
          paddingLeft: '20px', 
          color: '#666',
          fontSize: '0.9rem',
          lineHeight: '1.6'
        }}>
          <li>Be specific about what data or analysis you want</li>
          <li>Mention time periods, categories, or metrics you're interested in</li>
          <li>Ask for both summary and detailed breakdowns</li>
          <li>Request visualizations for better understanding</li>
        </ul>
      </div>
    </div>
  );
};

export default PromptInput;
