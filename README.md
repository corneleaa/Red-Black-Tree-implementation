# Reddit User Activity Analysis

## Overview

This project analyzes Reddit user activity and content using the Reddit API and advanced tree data structures. The system collects large amounts of data from several subreddits, processes the information, and performs multiple types of analysis including user activity ranking, word frequency analysis, subreddit popularity analysis, and sentiment analysis.

The project demonstrates the application of algorithmic data structures such as **Red-Black Trees** and **AVL Trees** for efficient processing of large datasets. These structures enable fast insertion, searching, and sorting operations when dealing with tens of thousands of users and textual data.

The analysis was implemented in **Python** and relies on the **Reddit API (PRAW)** for data collection.

---

# Project Goals

The goal of this project is to analyze Reddit user activity and the characteristics of the content they create.

The main objectives include:

- Collecting active Reddit users from selected subreddits
- Ranking users by their activity level
- Identifying the most frequently used words in user content
- Identifying the most active subreddits used by the most active users
- Performing sentiment analysis on user posts and comments
- Demonstrating the use of efficient data structures for large-scale data analysis

---

# Technologies Used

The project was implemented using the following tools and libraries:

- **Python** - main programming language  
- **PRAW** - Reddit API wrapper used for collecting data from Reddit  
- **TextBlob** - library used for sentiment analysis  
- **JSON** - used for storing collected user data  
- **tqdm** - progress bar for long-running data collection tasks  

Algorithmic data structures used in the project:

- **Red-Black Tree**
- **AVL Tree**

These structures provide efficient **O(log n)** insertion and search operations, which is essential when working with large datasets.

---

# Project Structure

The project consists of several Python modules, each responsible for a specific part of the analysis.

### `proj.py`

Responsible for collecting user activity data from Reddit.

Main tasks:
- Connect to Reddit API using PRAW
- Retrieve posts from selected subreddits
- Extract authors of posts and comments
- Assign activity points to users
- Store aggregated results in a JSON file

User activity scoring system:

- **+5 points** for creating a post
- **+1 point** for writing a comment

Collected results are stored in:

The script also saves timestamps to avoid collecting the same posts multiple times.

---

### `red_black_tree.py`

Implements the **Red-Black Tree** data structure.

This structure is used to store users and their activity scores efficiently.

Key characteristics:

- Balanced binary search tree
- Guarantees **O(log n)** insertion and lookup
- Automatically maintains balance using rotations and color rules

Usage in the project:

- Users are inserted into the tree with their activity score
- If a user already exists, their score is updated
- The tree is traversed to identify the **Top 10 most active users**

Red-Black Trees are particularly suitable for scenarios with **frequent insertions and updates**, such as continuous data collection.

---

### `analyze_words_subreddits.py`

Performs analysis of **user-generated text** using an **AVL Tree**.

This module analyzes the content of the **Top 1000 most active users**.

Steps performed:

1. Load user activity data from `users_data.json`
2. Select the **1000 most active users**
3. Retrieve their recent posts and comments
4. Clean and tokenize text
5. Remove **stop words**
6. Insert words into an AVL tree
7. Count subreddit appearances using another AVL tree

Two AVL Trees are used:

- Word frequency tree
- Subreddit frequency tree

The results include:

- **Top 20 most frequent words**
- **Top 20 most active subreddits**

AVL Trees are used because they maintain **strict balance**, which makes search operations extremely efficient.

---

### `sentiments_analysis.py`

Performs **sentiment analysis** on the content of the most active users.

For each selected user:

- Up to **20 recent posts** are retrieved
- Up to **30 recent comments** are retrieved

Each text is analyzed using **TextBlob**, which produces a sentiment score in the range:

The program calculates:

- Average sentiment of posts
- Average sentiment of comments

This provides insight into the emotional tone of the content created by active Reddit users.

---

# Data Collection

Data is collected using the **Reddit API** via the PRAW library.

The analysis focuses on the following subreddits:

For each subreddit:

- Up to **1000 newest submissions** are retrieved
- Comments are processed recursively
- User activity is recorded and aggregated

During the data collection process, over **115,000 unique Reddit users** were identified and analyzed.

The collected data is stored in JSON format for further analysis.

---

# Data Structures Used

## Red-Black Tree

Red-Black Tree was used for **user activity ranking**.

Reasons for using Red-Black Tree:

- Efficient insertion operations
- Guaranteed logarithmic complexity
- Good performance for frequent updates
- Automatic balancing

Each time a username is encountered:

- If the user already exists, their activity score increases
- If the user does not exist, a new node is created

This allows efficient management of large numbers of users.

---

## AVL Tree

AVL Tree was used for **text analysis**.

Reasons for using AVL Tree:

- Strict balancing guarantees
- Extremely efficient search performance
- Suitable for frequency analysis
- Good for large datasets where many queries are performed

In the project:

- Words are inserted into the tree
- If a word already exists, its counter increases
- If it does not exist, a new node is created

AVL rotations maintain the balance of the tree automatically.

---

# Results

The analysis produced several key insights.

Main results:

- **115,873 unique Reddit users collected**
- **Top 10 most active users identified**
- **Top 20 most frequently used words identified**
- **Top 20 most active subreddits identified**
- **Sentiment analysis performed for top users**

These results provide insight into both the **activity patterns** and **content characteristics** of Reddit users.
