import React, { useState } from 'react';
import PromptInput from './components/PromptInput';
import TextResponse from './components/TextResponse';
import GraphicalResponse from './components/GraphicalResponse';
import { Send, Brain, BarChart3 } from 'lucide-react';

function App() {
  const [responses, setResponses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState('checking');

  // Check backend status on component mount
  React.useEffect(() => {
    const checkBackendStatus = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/health', {
          method: 'GET',
          timeout: 5000
        });
        if (response.ok) {
          setBackendStatus('connected');
        } else {
          setBackendStatus('error');
        }
      } catch (error) {
        setBackendStatus('error');
      }
    };
    
    checkBackendStatus();
  }, []);

  const handlePromptSubmit = async (prompt) => {
    setIsLoading(true);
    
    try {
      // Call the real API with timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
      
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      const newResponse = {
        id: Date.now(),
        prompt,
        textResponse: data.textResponse,
        graphicalData: data.chartData,
        analysisType: data.analysisType,
        timestamp: new Date().toLocaleString()
      };
      
      setResponses(prev => [newResponse, ...prev]);
    } catch (error) {
      console.error('Error fetching data:', error);
      
      // Show error message instead of mock data
      const errorMessage = error.name === 'AbortError' 
        ? 'Request timed out. Please ensure the backend server is running on port 5000.'
        : `API Error: ${error.message}. Please ensure the backend server is running.`;
      
      const newResponse = {
        id: Date.now(),
        prompt,
        textResponse: `❌ Error: ${errorMessage}\n\nTo fix this:\n1. Make sure the backend server is running\n2. Run: python start_backend.py\n3. Or run: python start_both.py\n4. Check that port 5000 is available`,
        graphicalData: {
          type: 'bar',
          title: 'Connection Error',
          data: {
            labels: ['Error'],
            datasets: [{
              label: 'Status',
              data: [0],
              backgroundColor: 'rgba(239, 68, 68, 0.8)',
              borderColor: 'rgba(239, 68, 68, 1)',
              borderWidth: 2
            }]
          }
        },
        analysisType: 'error',
        timestamp: new Date().toLocaleString(),
        error: true
      };
      
      setResponses(prev => [newResponse, ...prev]);
    }
    
    setIsLoading(false);
  };

  const generateTextResponse = (prompt) => {
    const lowerPrompt = prompt.toLowerCase();
    
    if (lowerPrompt.includes('weather') || lowerPrompt.includes('temperature')) {
      return `Based on your query about weather, here's the current analysis:

🌤️ Current Weather Conditions:
- Temperature: 22°C (72°F)
- Humidity: 65%
- Wind Speed: 12 km/h
- Conditions: Partly Cloudy

📊 Weather Trends:
The temperature has been stable over the past week with minimal fluctuations. The humidity levels are within normal range for this season. Expect similar conditions for the next 3 days with a slight chance of light rain on Thursday.

💡 Recommendations:
- Perfect weather for outdoor activities
- Light clothing recommended
- Consider carrying an umbrella for Thursday`;
    }
    
    if (lowerPrompt.includes('sales') || lowerPrompt.includes('revenue') || lowerPrompt.includes('profit')) {
      return `📈 Sales Performance Analysis:

Q3 2024 Results:
- Total Revenue: $2.4M (+15% vs Q2)
- Gross Profit: $1.8M (75% margin)
- Units Sold: 12,450 (+8% growth)
- Average Order Value: $193 (+12% increase)

🎯 Key Insights:
• Digital channels driving 60% of growth
• Premium product line outperforming by 25%
• Customer retention rate at 87%
• New customer acquisition up 22%

📊 Regional Performance:
- North America: 45% of total sales
- Europe: 30% of total sales  
- Asia-Pacific: 25% of total sales

🚀 Growth Opportunities:
1. Expand premium product marketing
2. Increase digital channel investment
3. Focus on high-value customer segments`;
    }
    
    if (lowerPrompt.includes('user') || lowerPrompt.includes('customer') || lowerPrompt.includes('demographic')) {
      return `👥 User Demographics & Behavior Analysis:

📊 User Base Overview:
- Total Active Users: 45,230
- New Users (30 days): 8,940
- Returning Users: 36,290
- User Retention Rate: 87%

🎯 Demographics Breakdown:
• Age Groups:
  - 18-24: 25%
  - 25-34: 35%
  - 35-44: 22%
  - 45-54: 12%
  - 55+: 6%

• Geographic Distribution:
  - Urban: 68%
  - Suburban: 24%
  - Rural: 8%

• Device Usage:
  - Mobile: 72%
  - Desktop: 20%
  - Tablet: 8%

💡 Key Insights:
- Mobile-first user behavior is dominant
- Peak usage hours: 7-9 AM and 6-8 PM
- Average session duration: 12 minutes
- Most engaged users are 25-34 age group`;
    }
    
    // Default response for other prompts
    return `🤖 AI Response to: "${prompt}"

Thank you for your query! I've analyzed your request and here's my comprehensive response:

📝 Analysis Summary:
Your prompt has been processed through our advanced AI system. The query contains ${prompt.split(' ').length} words and covers the topic you've specified.

🔍 Key Points Addressed:
• Topic identification and categorization
• Context analysis and understanding
• Response generation based on available data
• Structured information presentation

💡 Insights Generated:
Based on the patterns in your query, I've identified several relevant aspects that contribute to a comprehensive response. The system has processed your request using natural language understanding and generated this contextual reply.

🎯 Next Steps:
If you need more specific information or have follow-up questions, please feel free to ask. I'm here to help with detailed analysis and insights on any topic you're interested in exploring further.`;
  };

  const generateGraphicalData = (prompt) => {
    const lowerPrompt = prompt.toLowerCase();
    
    if (lowerPrompt.includes('weather') || lowerPrompt.includes('temperature')) {
      return {
        type: 'line',
        title: 'Temperature Trends (7 Days)',
        data: {
          labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          datasets: [{
            label: 'Temperature (°C)',
            data: [20, 22, 24, 21, 23, 25, 22],
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.4
          }]
        }
      };
    }
    
    if (lowerPrompt.includes('sales') || lowerPrompt.includes('revenue') || lowerPrompt.includes('profit')) {
      return {
        type: 'bar',
        title: 'Sales Performance by Region',
        data: {
          labels: ['North America', 'Europe', 'Asia-Pacific', 'Latin America'],
          datasets: [{
            label: 'Revenue (Millions $)',
            data: [1.08, 0.72, 0.60, 0.24],
            backgroundColor: [
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 99, 132, 0.8)',
              'rgba(255, 205, 86, 0.8)',
              'rgba(75, 192, 192, 0.8)'
            ],
            borderColor: [
              'rgba(54, 162, 235, 1)',
              'rgba(255, 99, 132, 1)',
              'rgba(255, 205, 86, 1)',
              'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 2
          }]
        }
      };
    }
    
    if (lowerPrompt.includes('user') || lowerPrompt.includes('customer') || lowerPrompt.includes('demographic')) {
      return {
        type: 'doughnut',
        title: 'User Age Distribution',
        data: {
          labels: ['18-24', '25-34', '35-44', '45-54', '55+'],
          datasets: [{
            data: [25, 35, 22, 12, 6],
            backgroundColor: [
              '#FF6384',
              '#36A2EB',
              '#FFCE56',
              '#4BC0C0',
              '#9966FF'
            ],
            borderWidth: 2,
            borderColor: '#fff'
          }]
        }
      };
    }
    
    // Default chart for other prompts
    return {
      type: 'bar',
      title: 'Query Analysis Metrics',
      data: {
        labels: ['Complexity', 'Length', 'Clarity', 'Relevance', 'Engagement'],
        datasets: [{
          label: 'Score (1-10)',
          data: [7, 6, 8, 9, 7],
          backgroundColor: 'rgba(102, 126, 234, 0.8)',
          borderColor: 'rgba(102, 126, 234, 1)',
          borderWidth: 2
        }]
      }
    };
  };

  return (
    <div className="container">
      <header className="card" style={{ textAlign: 'center', marginBottom: '30px' }}>
        <h1 style={{ 
          fontSize: '2.5rem', 
          marginBottom: '10px',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text'
        }}>
          <Brain size={40} style={{ marginRight: '15px', verticalAlign: 'middle' }} />
          Interactive Prompt Responder
        </h1>
        <p style={{ fontSize: '1.1rem', color: '#666', marginBottom: '10px' }}>
          Enter your prompt and get both text and graphical responses powered by AI
        </p>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '8px',
          fontSize: '0.9rem',
          fontWeight: '600'
        }}>
          <span style={{
            padding: '4px 8px',
            borderRadius: '4px',
            backgroundColor: backendStatus === 'connected' ? '#d1fae5' : backendStatus === 'checking' ? '#fef3c7' : '#fee2e2',
            color: backendStatus === 'connected' ? '#065f46' : backendStatus === 'checking' ? '#92400e' : '#991b1b'
          }}>
            {backendStatus === 'connected' ? '✅ Backend Connected' : 
             backendStatus === 'checking' ? '🔄 Checking Backend...' : 
             '❌ Backend Disconnected'}
          </span>
          {backendStatus === 'error' && (
            <span style={{ fontSize: '0.8rem', color: '#666' }}>
              Run: python start_backend.py
            </span>
          )}
        </div>
      </header>

      <PromptInput onSubmit={handlePromptSubmit} isLoading={isLoading} />

      {responses.length > 0 && (
        <div style={{ marginTop: '30px' }}>
          <h2 style={{ 
            fontSize: '1.8rem', 
            marginBottom: '20px', 
            color: 'white',
            textAlign: 'center',
            textShadow: '0 2px 4px rgba(0,0,0,0.3)'
          }}>
            <BarChart3 size={30} style={{ marginRight: '10px', verticalAlign: 'middle' }} />
            Responses
          </h2>
          
          {responses.map((response) => (
            <div key={response.id} className="fade-in">
              <div className="card" style={{ marginBottom: '20px' }}>
                <div style={{ 
                  padding: '12px 16px', 
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  borderRadius: '8px',
                  marginBottom: '20px',
                  fontSize: '1.1rem',
                  fontWeight: '600'
                }}>
                  <Send size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                  {response.prompt}
                </div>
                
                <div style={{ 
                  fontSize: '0.9rem', 
                  color: '#666', 
                  marginBottom: '20px',
                  fontStyle: 'italic',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}>
                  <span>Generated on: {response.timestamp}</span>
                  <span style={{
                    padding: '4px 8px',
                    borderRadius: '4px',
                    fontSize: '0.8rem',
                    fontWeight: '600',
                    backgroundColor: response.error ? '#fee2e2' : '#d1fae5',
                    color: response.error ? '#991b1b' : '#065f46'
                  }}>
                    {response.error ? '❌ API Error' : '✅ Real Data'}
                  </span>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                  <TextResponse response={response.textResponse} />
                  <GraphicalResponse data={response.graphicalData} />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
