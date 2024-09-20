from flask import Blueprint ,request,jsonify , current_app
from dateutil import parser
import pytz
from datetime import datetime
from app.extensions import mongo

app_bp = Blueprint("webhook",__name__)

def Format_Date(date):
    # Parse the date string
    date_obj = parser.isoparse(date)
    
    # Convert to UTC
    date_obj_utc = date_obj.astimezone(pytz.utc)
    
    # Format the date into the target format
    target_format = '%d %B %Y - %I:%M %p UTC'
    return date_obj_utc.strftime(target_format)

@app_bp.route("/receiver",methods=["POST"])
def receiver():
    if request.headers['Content-Type'] =='application/json':
        payload = request.json
        event = request.headers.get('X-GitHub-Event')
        data = None
        #handling push request
        if event == "push":
            data = {
                "action": "push",
                "author": payload['pusher']['name'],
                "to_branch": payload['ref'].split('/')[-1],
                "timestamp": Format_Date(payload["head_commit"]['timestamp'])
            }
            
        #handling merge request
        elif event == "pull_request" and payload['action'] == 'closed':
            pr = payload['pull_request']
            data = {
                "action": "merge",
                "author": pr['user']['login'],
                "from_branch": pr['head']['ref'],
                "to_branch": pr['base']['ref'],
                "timestamp": Format_Date(pr["merged_at"])
            }
            
        #handling pull request
        elif event == "pull_request":
            pr = payload['pull_request']
            data = {
                "action": "pull_request",
                "author": pr['user']['login'],
                "from_branch": pr['head']['ref'],
                "to_branch": pr['base']['ref'],
                "timestamp": Format_Date(pr["created_at"])
            }
            
        if data != None:
            mongo.db.github_events.insert_one(data)
        return event
    
@app_bp.route('/events', methods=['GET'])
def get_events():
    
    limit = int(request.args.get('limit', 5))  # Default to 5 events
    offset = int(request.args.get('offset', 0))  # Offset for pagination
    events = list(mongo.db.github_events.find().sort('timestamp', -1).skip(offset).limit(limit))

    # Convert ObjectId and timestamp to a string for JSON serialization
    for event in events:
        event['_id'] = str(event['_id'])
        if isinstance(event['timestamp'], datetime):
            event['timestamp'] = event['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

    return jsonify(events)
def index():
    return "hello world"