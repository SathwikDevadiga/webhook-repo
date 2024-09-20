import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EventsList = () => {
  const [events, setEvents] = useState([]);
  const [visibleEvents, setVisibleEvents] = useState(5); // Limit initial fetch to 5
  const [loadingMore, setLoadingMore] = useState(false); // Loading state to prevent multiple fetches

  // Function to fetch data from the Flask API with limit and offset
  const fetchEvents = async (offset = 0, limit = 5) => {
    try {
      const response = await axios.get(`http://localhost:5000/events?offset=${offset}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching events:', error);
      return [];
    }
  };

  // Initial useEffect to fetch the first 5 events
  useEffect(() => {
    const loadInitialEvents = async () => {
      const initialEvents = await fetchEvents(0, 5);
      setEvents(initialEvents);
    };

    loadInitialEvents();
  }, []);

  // Function to load more events
  const loadMoreEvents = async () => {
    setLoadingMore(true);
    const moreEvents = await fetchEvents(events.length, 5); // Fetch the next 5 events
    setEvents((prevEvents) => [...prevEvents, ...moreEvents]); // Append new events to the existing ones
    setLoadingMore(false);
  };

  return (
    <div>
      <h2>Recent GitHub Events</h2>
      <ul>
        {events.map((event, index) => (
          <li key={index}>
            {event.action === 'push' && (
              <span><b>"{event.author}"</b> pushed to <b>"{event.to_branch}"</b> on <b>{new Date(event.timestamp).toLocaleString()}</b></span>
            )}
            {event.action === 'pull_request' && (
              <span><b>"{event.author}"</b> submitted a pull request from <b>"{event.from_branch}"</b> to <b>"{event.to_branch}"</b> on <b>{new Date(event.timestamp).toLocaleString()}</b></span>
            )}
            {event.action === 'merge' && (
              <span><b>"{event.author}"</b> merged branch <b>"{event.from_branch}"</b> to <b>"{event.to_branch}"</b> on <b>{new Date(event.timestamp).toLocaleString()}</b></span>
            )}
          </li>
        ))}
      </ul>
      {events.length >= visibleEvents && (
        <button onClick={loadMoreEvents} disabled={loadingMore}>
          {loadingMore ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
};

export default EventsList;
