import praw
import json
import time
import re

class AVLNode:
    def __init__(self, key, count=1):
        self.key = key
        self.count = count
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if not root:
            return AVLNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            root.count += 1
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)
        if balance < -1 and key > root.right.key:
            return self.rotate_left(root)
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def insert_key(self, key):
        self.root = self.insert(self.root, key)

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def in_order(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node.left:
            self.in_order(node.left, result)
        result.append((node.key, node.count))
        if node.right:
            self.in_order(node.right, result)
        return result

reddit = praw.Reddit(
    client_id="Write yours",
    client_secret="Write yours",
    user_agent="Write yours"
)

STOP_WORDS = set([
    "the", "and", "that", "this", "with", "you", "have", "for", "are", "but", "was", "from",
    "they", "your", "not", "all", "just", "like", "out", "get", "can", "has", "what", "about",
    "when", "will", "would", "there", "how", "more", "their", "who", "one", "also", "than", "if",
    "it's", "i'm", "i've", "we", "my", "or", "an", "in", "on", "to", "a", "of", "is", "it", "at"
])

def clean_and_split_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    return [word for word in text.split() if word not in STOP_WORDS and len(word) > 2]

def load_user_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)
def analyze_user(username, word_tree, subreddit_tree):
    try:
        redditor = reddit.redditor(username)

        for submission in redditor.submissions.new(limit=20):
            words = clean_and_split_text(submission.title + " " + submission.selftext)
            for word in words:
                word_tree.insert_key(word)
            subreddit_tree.insert_key(submission.subreddit.display_name)
            time.sleep(0.5)

        for comment in redditor.comments.new(limit=30):
            words = clean_and_split_text(comment.body)
            for word in words:
                word_tree.insert_key(word)
            subreddit_tree.insert_key(comment.subreddit.display_name)
            time.sleep(0.5)

    except Exception as e:
        print(f"Klaida su naudotoju {username}: {e}")

def main():
    word_tree = AVLTree()
    subreddit_tree = AVLTree()
    data = load_user_data("users_data.json")  

    top_1000_users = sorted(data.items(), key=lambda x: x[1], reverse=True)[:1000]
    usernames = [user for user, _ in top_1000_users]


    for i, username in enumerate(usernames):
        print(f" {i+1}. {username}")
        analyze_user(username, word_tree, subreddit_tree)

    print("\n TOP 20 žodžių:")
    top_words = sorted(word_tree.in_order(), key=lambda x: x[1], reverse=True)[:20]
    for word, count in top_words:
        print(f"{word:15s} – {count} kartų")

    print("\n TOP 20 subreddit'ų:")
    top_subs = sorted(subreddit_tree.in_order(), key=lambda x: x[1], reverse=True)[:20]
    for sub, count in top_subs:
        print(f"r/{sub:20s} – {count} postų/komentarų")

if __name__ == "__main__":
    main()
