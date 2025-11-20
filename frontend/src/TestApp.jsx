import React from 'react';

function TestApp() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ color: '#f97316' }}>🎉 DoseSafe Frontend is Working!</h1>
      <p>If you can see this, the basic React setup is working correctly.</p>
      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f0f9ff', borderRadius: '8px' }}>
        <h3>Next Steps:</h3>
        <ul>
          <li>✅ Vite server is running</li>
          <li>✅ React is rendering</li>
          <li>✅ Basic routing is working</li>
        </ul>
      </div>
    </div>
  );
}

export default TestApp;
