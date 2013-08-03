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
    return (sort, total_posts, subs)

def post_comment(url, limit):
    comment = _reddit.get_submission(url).comments[0]
    author = comment.author
    print comment
    print author
    hist = get_comment_history(author)
    sublist = ''
    count = 0
    for k in hist[0]:
        if count >= limit:
            break 
        sublist += '\n\n'+k+": "+str(float(hist[2][k]) / float(hist[1]) * 100)[:4]+"%"
        count += 1

    resp = "This from someone whose comment history is:"+sublist
    comment.reply(resp)
    print resp
    

def connect():
    global _reddit
    r = praw.Reddit(user_agent='com_history')
    r.login('','')
    _reddit = r
    
if __name__ == "__main__":
    connect()
    if sys.argv[1] == '-l':
        uname = sys.argv[2]
        get_comment_history(uname)
    elif sys.argv[1] == '-p':
        url = sys.argv[2]
        limit = sys.argv[3]
        post_comment(url,limit)
