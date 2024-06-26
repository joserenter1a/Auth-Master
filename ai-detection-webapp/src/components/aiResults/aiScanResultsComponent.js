import React from 'react';
import './aiScanResultsComponent.css'; 

export const AIScanResult = (response) => {
    const aiScorePercentage = (response.response.aiScore * 100).toFixed(2) + '%';
    const humanScorePercentage = (response.response.humanScore * 100).toFixed(2) + '%';
    const isGeneratedByAi = response.response.aiScore > 0.6;

    const positiveScan = 'We believe that this text was generated by AI';
    const negativeScan = 'We believe that this text was NOT generated by AI';
  return (
    <div className="ai-scan-result">
      <h2>AI Scan Results</h2>
      <p>AI Score: {aiScorePercentage}</p>
      <p>Originality Score: {humanScorePercentage}</p>
      <p> {isGeneratedByAi ? positiveScan : negativeScan }</p>
    </div>
  );
};
