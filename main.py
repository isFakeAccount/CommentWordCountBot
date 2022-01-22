import logging
from datetime import datetime, timedelta
from platform import platform
from time import time

from praw import Reddit
from yaml import safe_load

SECONDS_IN_DAY = 86_400


def is_posted_within(comment_created_utc: float, days: int) -> bool:
    """
    Checks if the comments is posted within last `days` from now.

    :param comment_created_utc: Comment creation date in Unix Time.
    :param days: The length of time for which we will be checking.
    :return: True if the comment is created within last `days` from now, else False.
    """
    time_days_ago = time() - days * SECONDS_IN_DAY
    return comment_created_utc >= time_days_ago


def word_count_above_thresh(comment_body: str, threshold: int) -> bool:
    """
    Checks if the body of the comment is above or equal to threshold.

    :param threshold: The minimum word count for comment to quality.
    :param comment_body: The comment text.
    :return: True if the word count is above threshold else False.
    """
    word_count = len(comment_body.split())
    return word_count >= threshold


def word_counter(reddit, bot_config):
    comments = []
    subreddit = reddit.subreddit(bot_config['subreddit'])
    days = bot_config['days']
    word_count_thresh = bot_config['word_count_threshold']

    # Grabbing all the comments
    logger.info(f"Checking comments of last {days} in r/{bot_config['subreddit']}")
    for comment in subreddit.comments(limit=None):
        if is_posted_within(comment.created_utc, days) and word_count_above_thresh(comment.body, word_count_thresh):
            logger.debug(f"Added comment crated on {datetime.fromtimestamp(comment.created_utc):'%Y-%m-%d %H:%M:%S'} by u/{comment.author}.")
            comments.append(comment)

    # Formatting the submission
    submission_title = f"Writing Prompt Responses [{datetime.today():%b %d, %Y}-{datetime.now() - timedelta(7):%b %d, %Y}]."
    submission_body = f"We received {len(comments)} comments longer than {word_count_thresh} word count in last {days} days.\n\n"
    for comment in comments:
        submission_body += f"[Comment](https://reddit.com{comment.permalink}) by u/{comment.author} in submission titled \"{comment.submission.title}\" on " \
                           f"{datetime.fromtimestamp(comment.created_utc):%b %d, %Y}\n\n"
        if bot_config['include_body']:
            submission_body += f"> {comment.body}\n\n"

    logger.info(f"{submission_title}\n\n{submission_body}")
    if 'y' in input("Submit the submission (above) on subreddit, yes or no? ").lower():
        submission = subreddit.submit(title=submission_title, selftext=submission_body)
        if 'y' in input("Pin the submission, yes or no? This will automatically remove previously pinned submission if any. "):
            submission.mod.distinguish(how="yes")
            submission.mod.sticky()
        logger.info(f"Submission posted at {submission.url}")


def main():
    with open('config.yaml') as config_file:
        bot_config = safe_load(config_file)

    # Logging into Reddit
    reddit = Reddit(client_id=bot_config['reddit_credentials']['client_id'],
                    client_secret=bot_config['reddit_credentials']['client_secret'],
                    username=bot_config['reddit_credentials']['username'],
                    password=bot_config['reddit_credentials']['password'],
                    user_agent=f"{platform()}:TrueRateMeStatsCalculator by (u/is_fake_Account)")
    reddit.validate_on_submit = True
    logger.info(f"Logged in as Reddit User {reddit.user.me()}.")
    word_counter(reddit, bot_config)


if __name__ == '__main__':
    # Setting up root logger
    logger = logging.getLogger("CommentWordCountBot")
    logger.setLevel(logging.DEBUG)

    # Setting up the streaming
    log_stream = logging.StreamHandler()
    log_stream.setLevel(logging.DEBUG)  # To make the script verbose set level to logging.DEBUG
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s')
    log_stream.setFormatter(formatter)
    logger.addHandler(log_stream)
    main()
