#-------------------------------------------------------------------------------
# imports

import tweepy
import time
from collections import defaultdict
import random
from datetime import datetime as dt
import os
from os import environ

#-------------------------------------------------------------------------------
# tweepy auth / api object

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.me()

# ------------------------------------------------------------------------------
# defining verables

# for like function
search_strings = ['#nothingtowards', '@NothingTowards']

nrTweets = 10

# for generating tweets/reply
starter = ["walk", "Walk", "Performer", "a", "A", "Performers", "Write", "write", "Make", "make", "Reflect",
           "perform", "an", "document", "attempt" "Create", "Use", "Mechanicalize", "look", "Humanize", "observe"]
replystarter = [" ok now: ", " how about: ", " now try: ", " this one's for you: ",
                " Dont do this: ", "try this one:"]

# sheduling tweet interval
# 0.012 for testing and 3.0 for real functionality

tweet_interval = 3.0

file = "id.txt"

#-------------------------------------------------------------------------------
# interacting with fluxus.txt file

with open("fluxus.txt") as f:
    words = f.read().split()

word_dict = defaultdict(list)
for word, next_word in zip(words, words[1:]):
    word_dict[word].append(next_word)

#-------------------------------------------------------------------------------
# tweet counter and tweeting

def post_new_tweet(new_tweet, max_tweets=6):
    global api
    post_new_tweet.count += 1
    if (post_new_tweet.count > max_tweets):
        print("tweet limit reached!")
    else:
        api.update_status(new_tweet)

post_new_tweet.count = 0
time_start = dt.now()
last_tweet_time = dt.now()

def make_random_reply():
    word = random.choice(starter)
    new_reply = word

    while not word.endswith("."):
        print(word, end=' ')
        word = random.choice(word_dict[word])
        new_reply += " " + word
    post_new_reply(new_reply)


def post_new_reply(new_reply):
    global api
    api.update_status("@" + mention.user.screen_name + random.choice(
        replystarter) + new_reply, in_reply_to_status_id=last_seen_id)
    print('replied to @' + mention.user.screen_name)
    print("replyed: ", new_reply)

# making a random tweet

def make_random_tweet():
    word = random.choice(starter)
    new_tweet = word

    while not word.endswith("."):
        print(word, end=' ')
        word = random.choice(word_dict[word])
        new_tweet += " " + word
    post_new_tweet(new_tweet)
    print("Tweeted:", new_tweet)


def favourite_tweets(containing_string, num_tweets=1):
    """
    favourite tweets that contain a given string
    """
    for tweet in tweepy.Cursor(api.search, containing_string).items(num_tweets):
        try:
            print('# tweet liked')
            tweet.favorite()
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

# ------------------------------------------------------------------------------
# interacting with id.txt - storing and reading

def retrieve_id(file):
    f_read = open(file, "r")
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_id(id, file):
    f_write = open(file, "w")
    f_write.write(str(id))
    f_write.close()
    return
# ------------------------------------------------------------------------------
# while loop
while True:
    time_elapsed = dt.now() - time_start
    # note - use '.days > 0' for real functionality & '.seconds > 900' (15min) for test
    if time_elapsed.days > 0:
        time_start = dt.now()
        post_new_tweet.count = 0

    # tweeting interval

    tweet_time_elapsed = dt.now() - last_tweet_time
    if (tweet_time_elapsed.seconds / 3600) > tweet_interval:
        last_tweet_time = dt.now()
        make_random_tweet()

    # reply
    last_seen_id = retrieve_id(file)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode="extended")

    for mention in reversed(mentions):
        last_seen_id = mention.id
        store_id(last_seen_id, file)
        make_random_reply()

    #NOTE - like/favourite
    for search_string in search_strings:
        favourite_tweets(search_string)

    time.sleep(90)