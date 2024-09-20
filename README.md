GitHub Webhook Receiver with Flask and React
Overview
This project implements a GitHub webhook receiver using a Flask backend and React frontend. The webhook listens for specific GitHub events—push, pull_request, and merge—stores them in MongoDB, and displays the event data in real-time on a frontend UI. The UI automatically refreshes every 15 seconds and allows users to load more events when available.

Features
GitHub Webhook Integration: Automatically listens to GitHub actions (push, pull request, merge) and captures relevant data.
Data Storage: Stores the captured event data in MongoDB for persistent storage.
REST API: Exposes a /events API to fetch the events with pagination.
Real-time Updates: The React frontend polls the backend every 15 seconds to update the UI with the latest events.
Load More Functionality: Allows the user to load more historical events.
Project Structure

/app
    /extensions.py     # MongoDB initialization
    /webhooks/routes.py # Flask routes for webhook and event retrieval
/main.py               # Flask application entry point
/frontend              # React frontend
    /src
        /components
            /EventsList.js  # React component to display GitHub events
Backend (Flask)
Installation
Clone this repository.

Install the required Python packages:

pip install -r requirements.txt
Ensure MongoDB is running locally on mongodb://localhost:27017.

Run the Flask server:

python main.py
API Endpoints
Webhook Receiver: POST /receiver
Listens for incoming GitHub webhook events and stores them in MongoDB.
Fetch Events: GET /events
Retrieves the latest events with optional query parameters:
limit: Number of events to retrieve (default is 5).
offset: Number of events to skip for pagination (default is 0).
MongoDB Schema
Events are stored in MongoDB with the following fields:

action: Type of action (push, pull_request, or merge).
author: Author of the action.
from_branch: Source branch (if applicable).
to_branch: Target branch (if applicable).
timestamp: Date and time of the event.
Frontend (React)
Installation
Navigate to the frontend directory:

cd frontend
Install the required Node.js packages:

npm install
Run the React development server:


npm start
React Component: EventsList
Fetches events from the Flask backend and displays them.
Automatically refreshes every 15 seconds to fetch new events.
Provides a “Load More” button to load additional events from the backend.
Setting Up GitHub Webhooks
Create two repositories on GitHub:

action-repo: The repository where GitHub actions (push, pull request, merge) will occur.
webhook-repo: The repository containing this webhook receiver code.
In action-repo, go to Settings > Webhooks > Add webhook and configure it as follows:

Payload URL: http://<your_server>/receiver
Content type: application/json
Events: Choose push, pull_request, and merge.
Once set up, GitHub will send the specified event data to the webhook receiver when actions occur in action-repo.

Running the Project
Start the Flask backend by running:


python main.py
Start the React frontend:
npm start
Trigger GitHub events by performing actions (push, pull requests, merges) in action-repo.

The frontend will fetch and display these events in real time, with options to load more past events.

Tech Stack
Backend: Flask, Flask-PyMongo, Flask-CORS, MongoDB
Frontend: React, Axios
Database: MongoDB
