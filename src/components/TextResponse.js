import React from 'react';
import { FileText, Copy, Check } from 'lucide-react';
import { useState } from 'react';

const TextResponse = ({ response }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(response);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const formatResponse = (text) => {
    // Split by lines and format
    return text.split('\n').map((line, index) => {
      // Handle headers (lines starting with emoji or special characters)
      if (line.match(/^[🌤️📊💡🎯📈👥🔍🚀📝•]/) || line.includes(':')) {
        return (
          <div key={index} style={{ 
            marginBottom: '8px',
            fontWeight: line.includes('📊') || line.includes('🎯') || line.includes('💡') ? '600' : '500',
            color: line.includes('📊') || line.includes('🎯') || line.includes('💡') ? '#667eea' : '#333',
            fontSize: line.includes('📊') || line.includes('🎯') || line.includes('💡') ? '1.1rem' : '1rem'
          }}>
            {line}
          </div>
        );
      }
      
      // Handle bullet points
      if (line.trim().startsWith('•') || line.trim().startsWith('-')) {
        return (
          <div key={index} style={{ 
            marginLeft: '20px', 
            marginBottom: '4px',
            color: '#555',
            lineHeight: '1.5'
          }}>
            {line}
          </div>
        );
      }
      
      // Handle empty lines
      if (line.trim() === '') {
        return <div key={index} style={{ marginBottom: '8px' }}></div>;
      }
      
      // Regular text
      return (
        <div key={index} style={{ 
          marginBottom: '6px',
          color: '#444',
          lineHeight: '1.6'
        }}>
          {line}
        </div>
      );
    });
  };

  return (
    <div style={{ 
      background: 'rgba(248, 250, 252, 0.8)',
      borderRadius: '12px',
      padding: '20px',
      border: '1px solid rgba(226, 232, 240, 0.8)',
      height: 'fit-content'
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
          <FileText size={20} />
          Text Response
        </h3>
        
        <button
          onClick={handleCopy}
          style={{
            background: copied ? '#10b981' : 'rgba(102, 126, 234, 0.1)',
            border: `1px solid ${copied ? '#10b981' : 'rgba(102, 126, 234, 0.3)'}`,
            borderRadius: '6px',
            padding: '6px 10px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            fontSize: '0.85rem',
            color: copied ? 'white' : '#667eea',
            transition: 'all 0.2s ease'
          }}
        >
          {copied ? <Check size={14} /> : <Copy size={14} />}
          {copied ? 'Copied!' : 'Copy'}
        </button>
      </div>
      
      <div style={{ 
        maxHeight: '400px',
        overflowY: 'auto',
        paddingRight: '8px'
      }}>
        <div style={{ 
          fontSize: '0.95rem',
          lineHeight: '1.6',
          color: '#333'
        }}>
          {formatResponse(response)}
        </div>
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
        📝 AI-generated response • {response.split(' ').length} words
      </div>
    </div>
  );
};

export default TextResponse;
