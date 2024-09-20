import React from 'react';
import EventsList from './EventsList';  // Import the EventsList component

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>GitHub Webhook Events</h1>
        <EventsList />  {/* Render the EventsList component */}
      </header>
    </div>
  );
}

export default App;