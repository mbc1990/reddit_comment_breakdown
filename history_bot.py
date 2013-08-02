import praw
import sys

_reddit = None

def get_comment_history(username):
    user = _reddit.get_redditor(username)
    subs = {}
    com = user.get_comments(limit=1000)
    for c in com:
        if c.subreddit.display_name not in subs:
            subs[c.subreddit.display_name] = 0
        subs[c.subreddit.display_name] += 1

    total_posts = sum(subs.itervalues())
    sort = sorted(subs, key=subs.get, reverse=True)
    for k in sort:
        print k+" "+str(float(subs[k] / float(total_posts)))    

def connect():
    global _reddit
    r = praw.Reddit(user_agent='com_history')
    _reddit = r
    
if __name__ == "__main__":
    connect()
    uname = sys.argv[1]
    get_comment_history(uname)
