# BaddieBot for Reddit

## Description

BaddieBot works like the more famous BeetusBot. It posts other submissions by the same author on new submissions,
 it allows you to subscribe to a specific author and you will receive a new message everytime this author posts a new submission and you can unsubscribe from a specific author.

## Installation

The bot runs on Python 2.7 with the following package:

* [PRAW aka. Python Reddit API Wrapper](https://github.com/praw-dev/praw)

which can be easily installed using pip

    pip install praw


## Configuration

Open the bot.py and edit all variables in the "CHANGE THESE" section: 

    USERNAME = "" # username of your bot's reddit account
    PASSWORD = "" # password of your bot's reddit account
    PATHTODB = "/home/test/baddiebot/db.db" # path to your db.db which should be the same path as your bot.py
    USER_AGENT = "BaddieBot by /u/tst__" # user agent of the bot
    SUBREDDIT = "badpeoplestories" # subreddit in which the bot should work
    # Introduction appears before posting the matching URLs
    INTRODUCTION = "Other stories from /u/%s:"
    # Ending appears after posting the matching URLS; \n\n for newline
    ENDING = "**** \n\n ^(If you want to get notified as soon as %s posts a new story, )[^click ^here.](%s)"  

## Usage

*I would recommend that you bot's account should have some link karma so that it can send messages without captcha restrictions.*

If you execute the bot.py with

    python bot.py

it will crawl the /new page and check each new submissions. For each submission it will use the search function with (author:) to find other submissions in the same subreddit by the same other. If it found any it will post a comments including its findings. Also it will message all subscribers. 

## Requests / Questions

If you have any requests or actions feel free to open an issue, message me on reddit ([/u/tst__](http://www.reddit.com/message/compose/?to=tst__)) or write me an email.
