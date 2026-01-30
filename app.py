from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb+srv://archee20barapatre_db_user:ArcheeBarapatre@cluster0.d7ywz1t.mongodb.net/?appName=Cluster0")

db = client.github_events
collection = db.events


@app.route('/')
def index():
    events = collection.find().sort("timestamp", -1).limit(10)
    formatted = []

    for e in events:
        ts = e["timestamp"]
        if isinstance(ts, str):
            ts = datetime.strptime(ts, "%d %b %Y - %I:%M %p")

        formatted.append({
            "author": e["author"],
            "action": e["action"],
            "from_branch": e.get("from_branch"),
            "to_branch": e.get("to_branch"),
            "timestamp": ts.strftime("%d %b %Y - %I:%M %p")
        })

    return render_template("index.html", events=formatted)


@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == "push":
        author = payload['pusher']['name']
        to_branch = payload['ref'].split('/')[-1]

        data = {
            "author": author,
            "action": "PUSH",
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": datetime.utcnow()
        }

        collection.insert_one(data)

    elif event_type == "pull_request":
        pr = payload['pull_request']
        author = pr['user']['login']
        from_branch = pr['head']['ref']
        to_branch = pr['base']['ref']

        data = {
            "author": author,
            "action": "PULL_REQUEST",
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": datetime.utcnow()
        }

        collection.insert_one(data)

    return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    app.run(debug=True)
