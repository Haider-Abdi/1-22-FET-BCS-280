# Social Media API Client

This is a simple Python client for interacting with a test social media server API using a Bearer access token.

## Features
- List all users
- List posts for a user
- List comments for a post

## Setup

1. **Clone or download this folder.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your Bearer access token:**
   - Open `client.py` and replace `YOUR_ACCESS_TOKEN_HERE` with your actual token.

## Usage (Interactive Client)

Run the client interactively:
```bash
python client.py
```
Follow the on-screen menu to list users, posts, or comments in real time.

---

## Usage (Microservice API)

Run the Flask microservice:
```bash
python service.py
```

### Endpoints
- `GET /users` — Top 5 users with the most commented posts
- `GET /posts?type=latest` — Latest 5 posts (default)
- `GET /posts?type=popular` — Post(s) with the most comments

**Note:** This client and service are for demonstration and testing purposes only. 