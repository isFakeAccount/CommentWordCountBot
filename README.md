# Comment Word Count Bot

I can search through all the recent comments on a subreddit and collect all the comments above certain word limit and post age.

I can later collect all the comments in a submission and post it on subreddit. 

# Configuration

### Prerequisite 
- Python 3.8+
- PRAW 7.5.0+

To install praw and all the libraries run

```commandline
pip install -r requirements.txt
```

To configure me, edit the yaml file template provided.

```yaml
reddit_credentials:
  username: "fakebot1"
  password: "invalidht4wd50gk"
  client_id: "revokedpDQy3xZ"
  client_secret: "revokedoqsMk5nHCJTHLrwgvHpr"

subreddit: "example_subreddit"
word_count_threshold: 300
days: 7

# Whether to include comment body in submission or not.
include_body: True
```

# References
[A bot that searches for comments longer than a defined word count.](https://www.reddit.com/r/RequestABot/comments/s6rjll/a_bot_that_searches_for_comments_longer_than_a/)
