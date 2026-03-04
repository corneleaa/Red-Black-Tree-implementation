import praw
from textblob import TextBlob
import time

reddit = praw.Reddit(
    client_id="Yours ID",
    client_secret="Write yours",
    user_agent="Write yours"
)

top_users = [
    "chrisdh79", "a_Ninja_b0y", "AutoModerator", "ketralnis", "mvea",
    "Wagamaga", "ControlCAD", "lurker_bee", "vriska1", "diacewrb"
]

def analyze_sentiment(text):
    if not text.strip():
        return 0.0
    blob = TextBlob(text)
    return blob.sentiment.polarity

def get_user_sentiment(username, post_limit=20, comment_limit=30):
    try:
        redditor = reddit.redditor(username)
        post_scores = []
        comment_scores = []

        for submission in redditor.submissions.new(limit=post_limit):
            full_text = (submission.title or "") + "\n" + (submission.selftext or "")
            score = analyze_sentiment(full_text)
            post_scores.append(score)
            time.sleep(0.5)

        for comment in redditor.comments.new(limit=comment_limit):
            score = analyze_sentiment(comment.body)
            comment_scores.append(score)
            time.sleep(0.5)

        post_avg = sum(post_scores) / len(post_scores) if post_scores else 0
        comment_avg = sum(comment_scores) / len(comment_scores) if comment_scores else 0

        return post_avg, comment_avg

    except Exception as e:
        print(f"Klaida su naudotoju {username}: {e}")
        return 0, 0

def main():

    for user in top_users:
        post_avg, comment_avg = get_user_sentiment(user)
        print(f" {user:20s} | Postų sentimentas: {post_avg:+.2f} | Komentarų sentimentas: {comment_avg:+.2f}")

if __name__ == "__main__":
    main()
