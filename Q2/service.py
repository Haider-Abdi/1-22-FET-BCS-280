from flask import Flask, request, jsonify
import requests
import logging
import time
import os
from dotenv import load_dotenv

app = Flask(__name__)


load_dotenv()

BASE_URL = "http://20.244.56.144/evaluation-service"
AUTH_URL = "http://20.244.56.144/evaluation-service/auth"
AUTH_PAYLOAD = {
    "email": os.getenv("AUTH_EMAIL"),
    "name": os.getenv("AUTH_NAME"),
    "rollNo": os.getenv("AUTH_ROLLNO"),
    "accessCode": os.getenv("AUTH_ACCESS_CODE"),
    "clientID": os.getenv("AUTH_CLIENT_ID"),
    "clientSecret": os.getenv("AUTH_CLIENT_SECRET")
}

token_info = {
    "access_token": None,
    "expires_at": 0
}

def get_token():
    if token_info["access_token"] is None or time.time() >= token_info["expires_at"]:
        try:
            resp = requests.post(AUTH_URL, json=AUTH_PAYLOAD, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            token_info["access_token"] = data["access_token"]
            token_info["expires_at"] = time.time() + int(data["expires_in"])
        except Exception as e:
            logging.error(f"Failed to get access token: {e}")
            return None
    return token_info["access_token"]

def get_headers():
    token = get_token()
    return {"Authorization": f"Bearer {token}"} if token else {}

logging.basicConfig(level=logging.INFO)

def fetch_users():
    try:
        resp = requests.get(f"{BASE_URL}/users", headers=get_headers(), timeout=10)
        resp.raise_for_status()
        return resp.json().get("users", {})
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        return {}

def fetch_user_posts(user_id):
    try:
        resp = requests.get(f"{BASE_URL}/users/{user_id}/posts", headers=get_headers(), timeout=10)
        resp.raise_for_status()
        return resp.json().get("posts", [])
    except Exception as e:
        logging.error(f"Error fetching posts for user {user_id}: {e}")
        return []

def fetch_post_comments(post_id):
    try:
        resp = requests.get(f"{BASE_URL}/posts/{post_id}/comments", headers=get_headers(), timeout=10)
        resp.raise_for_status()
        return resp.json().get("comments", [])
    except Exception as e:
        logging.error(f"Error fetching comments for post {post_id}: {e}")
        return []

@app.route("/users", methods=["GET"])
def top_users():
    users = fetch_users()
    if not users:
        return jsonify({"error": "Could not fetch users from upstream API."}), 502
    user_comment_counts = []
    for user_id, user_name in users.items():
        posts = fetch_user_posts(user_id)
        comment_count = 0
        for post in posts:
            comments = fetch_post_comments(post["id"])
            comment_count += len(comments)
        user_comment_counts.append({"user_id": user_id, "user_name": user_name, "comment_count": comment_count})
    
    top5 = sorted(user_comment_counts, key=lambda x: (-x["comment_count"], x["user_name"]))[:5]
    return jsonify(top5)

@app.route("/posts", methods=["GET"])
def top_or_latest_posts():
    type_param = request.args.get("type", "latest")
    users = fetch_users()
    if not users:
        return jsonify({"error": "Could not fetch users from upstream API."}), 502
    all_posts = []
    for user_id in users:
        posts = fetch_user_posts(user_id)
        all_posts.extend(posts)
    if not all_posts:
        return jsonify([])
    if type_param == "popular":
        
        for post in all_posts:
            comments = fetch_post_comments(post["id"])
            post["comment_count"] = len(comments)
        max_comments = max(post["comment_count"] for post in all_posts)
        popular_posts = [post for post in all_posts if post["comment_count"] == max_comments]
        return jsonify(popular_posts)
    else:  
       
        latest_posts = sorted(all_posts, key=lambda x: -x["id"])[:5]
        return jsonify(latest_posts)

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Unhandled exception: {e}")
    return jsonify({"error": "Internal server error."}), 500

if __name__ == "__main__":
    app.run(debug=True)