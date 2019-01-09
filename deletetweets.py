#!/usr/bin/env python

import argparse
import json
import sys
import time
import os
import twitter
from dateutil.parser import parse

__author__ = "Koen Rouwhorst"
__version__ = "0.1"

def delete(api, date):   
    with open("tweet.js") as file:
        count = 0

        file_string = file.read().replace('window.YTD.tweet.part0 = ', '')
        tweet_list = json.loads(file_string)

        for tweet in tweet_list:
            tweet_id = tweet['id']
            tweet_date = parse(tweet['created_at'], ignoretz=True).date()

            if date != "" and tweet_date >= parse(date).date():
                continue

            try:
                print "Deleting tweet #{0} ({1})".format(tweet_id, tweet_date)

                api.DestroyStatus(tweet_id)
                count += 1
                time.sleep(0.5)

            except twitter.TwitterError, err:
                print "Exception: %s\n" % err.message

    print "Number of deleted tweets: %s\n" % count

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():
    parser = argparse.ArgumentParser(description="Delete old tweets.")
    parser.add_argument("-d", dest="date", required=True,
                        help="Delete tweets until this date")

    args = parser.parse_args()

    api = twitter.Api(consumer_key="",
                      consumer_secret="",
                      access_token_key="",
                      access_token_secret="")

    delete(api, args.date)

if __name__ == "__main__":
    main()
