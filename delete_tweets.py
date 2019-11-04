#!/usr/local/bin/env python

import argparse
import json
import pandas as pd
from datetime import datetime, timedelta
import tweepy


class TweetTracker():

    def __init__(self, config:str, testing:bool=True, verbose:bool=False):
        self.config = config
        self.testing = testing
        self.verbose = verbose
        self.api = self.authenticate_api()
        self.deleted_counter = 0
        self.deleted_tweets = self._initialize_list()
        self.saved_counter = 0
        self.saved_tweets = self._initialize_list()

    def authenticate_api(self):
        """ Use config to retrieve authenticated api """
        # load config file
        if self.verbose: print(f"Loading auth vars from '{self.config}'...")
        with open(self.config, "rb") as f:
            keys = json.load(f)

        # set auth vars
        CONSUMER_KEY = keys['API Key']
        CONSUMER_SECRET = keys['API Secret Key']
        ACCESS_TOKEN_KEY = keys['Access Token']
        ACCESS_TOKEN_SECRET = keys['Access Token Secret']
        ACCESS_LEVEL = keys['Access level']
        
        # load api
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        if self.verbose: print("API authenticated.")

        return api

    def process_timeline(self, days_to_keep:int=365, fav_min:int=None, rt_min:int=None):
        """ Process a timeline — deleting/saving tweets """
        timeline = self._get_timeline()
        for status in timeline:
            self.process_tweet(status, days_to_keep, fav_min, rt_min)


    def process_tweet(self, status, days_to_keep:int=365, fav_min:int=None, rt_min:int=None):
        """ Check deletion status then process tweet """
        if self.verbose: 
            print(f"Processing tweet [Testing Mode: {self.testing}]:")
            print(self.print_status(status))
        if self._tweet_delete_criteria(status, days_to_keep, fav_min, rt_min):
            self._delete_tweet(status)
        else:
            self._save_tweet(status)

    def print_status(self, status):
        """
        Pretty print a status/tweet
        """
        print("\n---")
        print(f"ID: {status.id_str}")
        print(f"Source: {status.source}")
        print(f"Date: {status.created_at}")
        print(f"Content: {status.text}")
        print(f"Faves: {status.favorite_count}")
        print(f"RTs: {status.retweet_count}")
        print("---\n")

    def _get_timeline(self):
        """ Get user's timeline """
        return tweepy.Cursor(self.api.user_timeline).items()
        
    def _plain_datetime(self, dt) -> str:
        """ Get datetime object as str: YYYY-mm-DD HH:MM:SS"""
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def _initialize_list(self) -> list:
        """ Get seed list with tweet headers """
        return [['id', 'date', 'text', 'user.id', 'user.screen_name', 'favorite_count', 'retweet_count']]

    def _status2list(self, status) -> list:
        """ Get information from status/tweet as a list """
        return [status.id_str, self._plain_datetime(status.created_at), status.text, status.user.id, status.user.screen_name, status.favorite_count, status.retweet_count]

    def _delete_tweet(self, status):
        """ Delete a tweet and count it """
        self.deleted_tweets.append(self._status2list(status))
        self.deleted_counter += 1
        # this is where a tweet is actually deleted
        if not self.testing:
            api.destroy_status(status.id)

    def _save_tweet(self, status):
        """ Save a tweet and count it """
        self.saved_tweets.append(self._status2list(status))
        self.saved_counter += 1

    def _tweet_delete_criteria(self, status, days_to_keep, fav_min, rt_min):
        """ 
        Defines logic to delete a tweet

        True if a tweet meets all criteria for deletion:
            - tweeted after "days_to_keep" days ago
            - has fewer or equal to "fav_min" favorites
            - has fewer or equal to "rt_min" retweets

        Args:
            status (tweepy obj): a tweet/status (Tweepy object)
            days_to_keep (int): how many days of tweets to keep
            fav_min (int): if favs <= fav_min, delete tweet
            rt_min (int): if rts <= rt_min, delete tweet

        Returns:
            bool: whether the tweet should be deleted (True) or not (False)
        
        """
        
        # true if tweeted created before cutoff date
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        cutoff = status.created_at <= cutoff_date
        if self.verbose: delete_desc = f"Tweets deletion criteria: if before {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}"
        
        # false if favs >= minimum, true if < or fave_min is None
        if fav_min:
            fav = not (status.favorite_count >= fav_min)
            if self.verbose: delete_desc = delete_desc + f" AND if fewer than {fav_min} like(s)"
        else:
            fav = True

        # false if rts >= minimum, true if < or rt_min is None
        if rt_min:
            rt = not (status.retweet_count >= rt_min)
            if self.verbose: delete_desc = delete_desc + f" AND if fewer than {rt_min} RT(s)"
        else:
            rt = True
        
        # final tweet status
        should_be_deleted = cutoff and fav and rt
        
        # print output
        if self.verbose:
            print(delete_desc)
            print(f"Tweet created on {status.created_at} and has {status.favorite_count} like(s) and {status.retweet_count} RT(s)")
            print(f"Tweet should be deleted: {should_be_deleted}")

        return should_be_deleted
    
    def save_data(self, filename:str="tweets.csv"):
        # check extension
        if not filename.endswith(".csv"):
            filename += ".csv"

        # save as dataframe
        df_deleted = pd.DataFrame(data=self.deleted_tweets[1:], columns=self.deleted_tweets[0])
        df_saved = pd.DataFrame(data=self.saved_tweets[1:], columns=self.saved_tweets[0])
        df_deleted.to_csv(path_or_buf="deleted_"+filename, index=False)
        df_saved.to_csv(path_or_buf="saved_"+filename, index=False)


def main(config_filepath, save_filepath, days_to_keep, fav_min, rt_min, testing, verbose):
    """
    Process timeline to find tweets that should be deleted versus saved
    """
    tracker = TweetTracker(config=config_filepath, testing=testing, verbose=verbose)
    tracker.process_timeline(days_to_keep=days_to_keep, fav_min=fav_min, rt_min=rt_min)
    tracker.save_data(filename=save_filepath)


if __name__ == '__main__':
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_filepath", type=str, default='twitter.config', help="Path to config file")
    parser.add_argument("-s", "--save_filepath", type=str, default='tweets.csv', help="Path to save tweets")
    parser.add_argument("-d", "--days_to_keep", type=int, default=365, help="Number of days to keep tweets [Default: 365]")
    parser.add_argument("-f", "--fav_min", type=int, default=0, help="Minimum faves for a tweet to be saved [Default: don't filter on faves")
    parser.add_argument("-r", "--rt_min", type=int, default=0, help="Minimum rts for a tweet to be saved [Default: don't filter on rts")
    parser.add_argument("-t", "--testing", action='store_true', default=False, help="Testing Mode [default: False]")
    parser.add_argument("-v", "--verbose", action='store_true', default=False, help="Verbose [default: False]")

    args = parser.parse_args()

    # unpack args
    config_filepath = args.config_filepath
    save_filepath = args.save_filepath
    days_to_keep = args.days_to_keep
    fav_min = args.fav_min
    rt_min = args.rt_min
    testing = args.testing
    verbose = args.verbose
    print(testing)

    # main
    main(config_filepath, save_filepath, days_to_keep, fav_min, rt_min, testing, verbose)

    """ 
    Testing Mode:
        python delete_tweets.py -c twitter.config -d 365 -f 0 -r 0 -s tweets.csv -t -v

    You can run this and then examine the csv with 'deleted tweets' to verify if applied properly
    """
