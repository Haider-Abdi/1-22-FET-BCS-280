import requests


BASE_URL = "http://localhost:5000"

def get_top_users():
    response = requests.get(f"{BASE_URL}/users")
    return response.json()

def get_latest_posts():
    response = requests.get(f"{BASE_URL}/posts?type=latest")
    return response.json()

def get_popular_posts():
    response = requests.get(f"{BASE_URL}/posts?type=popular")
    return response.json()

if __name__ == "__main__":
    while True:
        print("\nOptions:")
        print("1. Get Top 5 Users with Most Comments")
        print("2. Get Latest 5 Posts")
        print("3. Get Most Popular Posts")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            users = get_top_users()
            print("Top 5 Users by Comment Count:")
            for user in users:
                print(f"{user['user_name']} (ID: {user['user_id']}) - {user['comment_count']} comments")

        elif choice == "2":
            latest = get_latest_posts()
            print("Latest 5 Posts:")
            for post in latest:
                print(f"Post ID: {post['id']} - Title: {post.get('title', '(no title)')}")

        elif choice == "3":
            popular = get_popular_posts()
            print("Most Popular Posts:")
            for post in popular:
                print(f"Post ID: {post['id']} - Title: {post.get('title', '(no title)')} - Comments: {post['comment_count']}")

        elif choice == "4":
            break
        else:
            print("Invalid choice.")
