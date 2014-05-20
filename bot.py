import praw
import time
import sqlite3
import os
import sys

### CHANGE THESE ###
####################
USERNAME = ""
PASSWORD = ""
PATHTODB = "/home/tim/baddiebot/db.db"
USER_AGENT = "BaddieBot by /u/tst__"
SUBREDDIT = "badpeoplestories"
# Introduction appears before posting the matching URLs
INTRODUCTION = "Other stories from /u/%s:"
# Ending appears after posting the matching URLS; \n\n for newline
ENDING = "**** \n\n ^(If you want to get notified as soon as %s posts a new story, )[^click ^here.](%s)" 

### STOP CHANGING ###
#####################

# if USERNAME and PASSWORD isn't set the bot will use the environment variables
# NOREPOST_USER for USERNAME
# NOREPOST_PASSWORD for PASSWORD
if USERNAME == "":
    try:
        USERNAME = os.environ['BADDIEBOT_USERNAME']
    except KeyError:
        sys.exit("Please add the username or set the environment variable BADDIEBOT_USERNAME")

if PASSWORD == "":
    try:
        PASSWORD = os.environ['BADDIEBOT_PASSWORD']
    except KeyError:
        sys.exit("Please add the password or set the environment variable BADDIEBOT_PASSWORD")


# login to Reddit
r = praw.Reddit(user_agent=USER_AGENT)
r.login(USERNAME, PASSWORD)

# connect to DB
conn = sqlite3.connect(PATHTODB)
c = conn.cursor()

# create the tables if it don't exist
c.execute("CREATE TABLE IF NOT EXISTS checked_ids (id TEXT);");
c.execute("CREATE TABLE IF NOT EXISTS subscriptions (writer TEXT, subscriber TEXT);");


## check for new messages
for new_message in r.get_unread(unset_has_mail=True, update_user=True):
    if new_message.subject == "subscribe":
        try:
            _, writer = new_message.body.split()
            subscriber = new_message.author.name
            # check if subscriber is already subscribed
            c.execute("SELECT * FROM subscriptions WHERE writer = ? AND subscriber = ?", (writer, subscriber,))
            if c.fetchone() is None:
                c.execute("INSERT INTO subscriptions (writer, subscriber) VALUES (?, ?)", (writer, subscriber ))
                conn.commit()
        except:
            ## TODO track to error log
            pass


    if new_message.subject == "unsubscribe":
        try:
            _, writer = new_message.body.split()
            subscriber = new_message.author.name
            c.execute("DELETE FROM subscriptions WHERE writer = ? AND subscriber = ?", (writer, subscriber))
            conn.commit()
        except:
            pass
    new_message.mark_as_read()



# get the newest submissions
new_sub = r.get_subreddit(SUBREDDIT).get_new()

## check every new submission
for x in new_sub:
    
    # Skip the submission if it's already checked
    c.execute("SELECT id FROM checked_ids WHERE id = ?", (x.id,))
    if c.fetchone() is not None:
        continue
    
    # Skip if the author's account is deleted
    if x.author is None:
        continue

    # notify all subscribers
    c.execute("SELECT subscriber FROM subscriptions WHERE writer = ?", (x.author.name, ))
    for subscriber in c.fetchall():
        unsub_msg = "unsubscribe %s" % x.author.name
        unsubscribe_url = "http://www.reddit.com/message/compose/?to=%s&subject=unsubscribe&message=%s" % (USERNAME, unsub_msg)
        subject = "New submission by /u/%s" % (x.author.name)
        message = "Hello %s,\n\n/u/%s has a new submission.\n\n* [%s](%s)\n\n****\
                   \n\n^(If you want to unsubscribe just, ) [^click ^here.](%s)" % (subscriber[0], x.author.name, \
                                                                                  x.title, x.url, unsubscribe_url)
        
        # this will catch an error if subscriber's account doesn't exist anymore
        try:
            r.send_message(subscriber[0], subject, message)
        except praw.errors.InvalidUser:
            # TODO track error
            # remove user's subscriptions
            c.execute("DELETE FROM subscriptions WHERE subscriber = ?", (subscriber[0], ))
            conn.commit()
        except:
            # TODO create error log
            pass

        time.sleep(3)


    # check for previous submissions
    results = r.search('author:"' + x.author.name + '"', subreddit=SUBREDDIT, sort="new")

    
    # examine the results found from doing a search
    found = []
    for y in results:
        # reject the result if it's the same id as the examined submission
        # i.e. found the result which we are looking at
        if y.id == x.id:
            continue
        else:
            found.append((" ".join(y.title.splitlines()), y.permalink))
    
    # if we found reposts we're going to add a comment to the submission
    if found:
        sub_msg = "subscribe %s" % x.author.name
        subscribe_url = "http://www.reddit.com/message/compose/?to=%s&subject=subscribe&message=%s" % (USERNAME, sub_msg)
        m = INTRODUCTION % (x.author.name)
        for f in found:
            m += "\n\n * [%s](%s)" % f
        m += "\n\n"
        m += ENDING % (x.author.name, subscribe_url)


        x.add_comment(m)
       
    # Insert id into the database to that it won't be rechecked
    c.execute("INSERT INTO checked_ids VALUES (?)", (x.id, ))
    conn.commit()

    time.sleep(5)

conn.close()
