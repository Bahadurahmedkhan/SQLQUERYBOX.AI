import React from 'react';
import { BarChart3, Download, Maximize2 } from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line, Doughnut } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const GraphicalResponse = ({ data }) => {
  const [isExpanded, setIsExpanded] = React.useState(false);

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            size: 12,
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
          }
        }
      },
      title: {
        display: true,
        text: data.title,
        font: {
          size: 16,
          weight: 'bold',
          family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        },
        color: '#333',
        padding: {
          top: 10,
          bottom: 20
        }
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: 'white',
        bodyColor: 'white',
        borderColor: 'rgba(102, 126, 234, 0.8)',
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: true,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== undefined) {
              label += context.parsed.y;
            } else if (context.parsed !== undefined) {
              label += context.parsed;
            }
            return label;
          }
        }
      }
    },
    scales: data.type !== 'doughnut' ? {
      x: {
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
          drawBorder: false
        },
        ticks: {
          color: '#666',
          font: {
            size: 11
          }
        }
      },
      y: {
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
          drawBorder: false
        },
        ticks: {
          color: '#666',
          font: {
            size: 11
          }
        },
        beginAtZero: true
      }
    } : {},
    elements: {
      bar: {
        borderRadius: 4,
        borderSkipped: false,
      },
      line: {
        tension: 0.4,
        borderWidth: 3,
        pointRadius: 5,
        pointHoverRadius: 7
      },
      arc: {
        borderWidth: 2,
        borderColor: '#fff'
      }
    },
    interaction: {
      intersect: false,
      mode: 'index'
    }
  };

  const renderChart = () => {
    switch (data.type) {
      case 'line':
        return <Line data={data.data} options={chartOptions} />;
      case 'doughnut':
        return <Doughnut data={data.data} options={chartOptions} />;
      case 'bar':
      default:
        return <Bar data={data.data} options={chartOptions} />;
    }
  };

  const handleDownload = () => {
    // Create a canvas element to capture the chart
    const canvas = document.querySelector(`#chart-${data.title.replace(/\s+/g, '-').toLowerCase()}`);
    if (canvas) {
      const link = document.createElement('a');
      link.download = `${data.title.replace(/\s+/g, '-').toLowerCase()}.png`;
      link.href = canvas.toDataURL();
      link.click();
    }
  };

  return (
    <div style={{ 
      background: 'rgba(248, 250, 252, 0.8)',
      borderRadius: '12px',
      padding: '20px',
      border: '1px solid rgba(226, 232, 240, 0.8)',
      height: isExpanded ? '500px' : 'fit-content'
    }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '16px',
        paddingBottom: '12px',
        borderBottom: '2px solid rgba(102, 126, 234, 0.1)'
      }}>
        <h3 style={{ 
          fontSize: '1.2rem', 
          color: '#333',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          margin: 0
        }}>
          <BarChart3 size={20} />
          Visual Response
        </h3>
        
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            style={{
              background: 'rgba(102, 126, 234, 0.1)',
              border: '1px solid rgba(102, 126, 234, 0.3)',
              borderRadius: '6px',
              padding: '6px 10px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              fontSize: '0.85rem',
              color: '#667eea',
              transition: 'all 0.2s ease'
            }}
          >
            <Maximize2 size={14} />
            {isExpanded ? 'Collapse' : 'Expand'}
          </button>
          
          <button
            onClick={handleDownload}
            style={{
              background: 'rgba(16, 185, 129, 0.1)',
              border: '1px solid rgba(16, 185, 129, 0.3)',
              borderRadius: '6px',
              padding: '6px 10px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              fontSize: '0.85rem',
              color: '#10b981',
              transition: 'all 0.2s ease'
            }}
          >
            <Download size={14} />
            Save
          </button>
        </div>
      </div>
      
      <div style={{ 
        height: isExpanded ? '400px' : '300px',
        position: 'relative',
        background: 'white',
        borderRadius: '8px',
        padding: '16px',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
      }}>
        {renderChart()}
      </div>
      
      <div style={{ 
        marginTop: '12px',
        padding: '8px 12px',
        background: 'rgba(102, 126, 234, 0.05)',
        borderRadius: '6px',
        fontSize: '0.8rem',
        color: '#667eea',
        textAlign: 'center'
      }}>
        📊 Interactive chart • {data.type.toUpperCase()} visualization
      </div>
      
      {/* Chart insights */}
      <div style={{ 
        marginTop: '12px',
        padding: '12px',
        background: 'rgba(59, 130, 246, 0.05)',
        borderRadius: '8px',
        border: '1px solid rgba(59, 130, 246, 0.1)'
      }}>
        <h4 style={{ 
          fontSize: '0.9rem', 
          color: '#3b82f6', 
          marginBottom: '8px',
          fontWeight: '600'
        }}>
          📈 Chart Insights:
        </h4>
        <ul style={{ 
          margin: 0, 
          paddingLeft: '16px', 
          fontSize: '0.8rem',
          color: '#4b5563',
          lineHeight: '1.4'
        }}>
          {data.type === 'bar' && (
            <>
              <li>Hover over bars to see exact values</li>
              <li>Click legend items to toggle datasets</li>
              <li>Use zoom/pan for detailed analysis</li>
            </>
          )}
          {data.type === 'line' && (
            <>
              <li>Track trends and patterns over time</li>
              <li>Hover to see precise data points</li>
              <li>Compare multiple metrics easily</li>
            </>
          )}
          {data.type === 'doughnut' && (
            <>
              <li>Click segments to highlight categories</li>
              <li>Perfect for showing proportions</li>
              <li>Hover for detailed percentages</li>
            </>
          )}
        </ul>
      </div>
    </div>
  );
};

export default GraphicalResponse;
