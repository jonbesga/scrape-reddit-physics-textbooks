import csv
import os
import praw
from praw.models import MoreComments


reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)


def write_comment_to_csv(writer, submission, comment):
    writer.writerow(
        {
            "body": comment.body,
            "author": comment.author,
            "thread": submission.title,
            "permalink": comment.permalink,
        }
    )


def write_comments(writer, submission, comments):
    for comment in comments:
        if isinstance(comment, MoreComments):
            more_comments = comment.comments().list()
            write_comments(writer, submission, more_comments)
        else:
            write_comment_to_csv(writer, submission, comment)


def main():
    with open("comments.csv", "w") as fd:
        writer = csv.DictWriter(
            fd, delimiter="|", fieldnames=["body", "author", "thread", "permalink"]
        )
        writer.writeheader()

        results = reddit.subreddit("physics").search("Textbooks & Resources", sort="new", limit=None)

        for submission in results:
            if submission.title.startswith(("Textbook & Resource Thread", "Textbooks & Resources")):
                print(submission.title)
                comments = submission.comments.list()
                write_comments(writer, submission, comments)


if __name__ == '__main__':
    main()
