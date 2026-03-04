import praw
import time
import json
import os
from tqdm import tqdm

reddit = praw.Reddit(
    client_id="Write yours",
    client_secret="Write yours",
    user_agent="Write yours"
)

def load_last_timestamp(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_last_timestamp(filepath, timestamp_dict):
    with open(filepath, 'w') as f:
        json.dump(timestamp_dict, f)

def save_users_json(filename, user_data):
    existing_data = {}
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                existing_data = json.load(f)
        except Exception:
            pass

    for user, score in user_data.items():
        existing_data[user] = existing_data.get(user, 0) + score

    with open(filename, 'w') as f:
        json.dump(existing_data, f)

def get_active_users(subreddit_name, submission_limit=1000, since_timestamp=0):
    users = {}
    subreddit = reddit.subreddit(subreddit_name)
    submissions = list(subreddit.new(limit=submission_limit))

    latest_timestamp = since_timestamp

    for submission in tqdm(submissions, desc=f"[{subreddit_name}]"):
        if submission.created_utc <= since_timestamp:
            continue

        if submission.created_utc > latest_timestamp:
            latest_timestamp = submission.created_utc

        if submission.author:
            users[submission.author.name] = users.get(submission.author.name, 0) + 5

        try:
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                if comment.author:
                    name = comment.author.name
                    users[name] = users.get(name, 0) + 1
        except Exception:
            continue

        time.sleep(1)

    return users, latest_timestamp

if __name__ == "__main__":
    json_file = "users_data.json"
    timestamp_file = "last_timestamp.txt"

    subreddit_list = ["technology", "programming", "science", "gadgets"]

    last_timestamps = load_last_timestamp(timestamp_file)

    for subreddit in subreddit_list:
        since = last_timestamps.get(subreddit, 0)
        users, new_timestamp = get_active_users(subreddit, submission_limit=1000, since_timestamp=since)

        if users:
            save_users_json(json_file, users)
            last_timestamps[subreddit] = new_timestamp
            save_last_timestamp(timestamp_file, last_timestamps)
