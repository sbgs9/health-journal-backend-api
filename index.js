const EventSource = require('eventsource');
const axios = require('axios');

// URL of the Flask SSE endpoint
const sseUrl = 'http://localhost:5000/events';

// Create a new EventSource object to connect to the SSE endpoint
const eventSource = new EventSource(sseUrl);

// Send a query to the Flask server
axios.post('http://localhost:5000/process_query', { query: 'work place related stress united states' })
  .then(response => {
    console.log('Query processed successfully:', response.data.message);
  })
  .catch(error => {
    console.error('Error processing query:', error);
  });

// Event listener to handle incoming SSE messages
eventSource.onmessage = function(event) {
    // Parse the incoming SSE message
    const data = JSON.parse(event.data);

    // Get the keys of the object
    const key = Object.keys(data)[0];

    if (key === 'search')
        console.log('Received SSE Search Data:', data['search']);
    else if (key === 'pdf')
        console.log('Received SSE PDF Data', data['pdf']);
    else if (key === 'contact')
        console.log('Received SSE Contact Data', data['contact']);
    else if(key === 'link')
        console.log('Received SSE Data of additional Hyperlinks', data['link'])
    else
        console.log('Received SSE Data of Unknown type');
    
};

// Event listener to handle SSE errors
eventSource.onerror = function(error) {
    // Log the error
    console.error('Error connecting to SSE endpoint:', error);

    // Prevent automatic reconnection attempts
    eventSource.close();
};

// Event listener to handle SSE close event
eventSource.onclose = function() {
    console.log('SSE connection terminated');
};
