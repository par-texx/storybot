# StoryBot for Reddit

## Description

StoryBot works like the more famous BeetusBot. It posts other submissions by the same author on new submissions,
 it allows you to subscribe to a specific author so that you will receive a new message every time this author posts a new submission. If you no longer want messages you can unsubscribe from a specific author.

## Installation

The bot runs on Python 2.7 with the following package:

* [PRAW aka. Python Reddit API Wrapper](https://github.com/praw-dev/praw)

which can be easily installed using pip

    pip install praw


## Configuration

Open the config.ini and edit it accordingly. These are the things you have to edit:

    [reddit]
    username=username ; reddit username of your bot
    password=password ; reddit password of your bot
    subreddit=badpeoplestories ; subreddit in which the bot should work

    [technical]
    pathtodb=/home/tim/storybot/db.db ; path to your bot's database, just use your bot's directory + db.db
    debug=on ; set debug=off to allow your bot to comment and send messages

## Usage

*I would recommend that you bot's account should have some link karma so that it can send messages without captcha restrictions.*

If you execute the bot.py with

    python bot.py

it will crawl the /new page and check each new submissions. For each submission it will use the search function with (author:) to find other submissions in the same subreddit by the same other. If it found any it will post a comments including its findings. Also it will message all subscribers. 

## Requests / Questions

If you have any requests or actions feel free to open an issue, message me on reddit ([/u/tst__](http://www.reddit.com/message/compose/?to=tst__)) or write me an email.

