# delete_tweets

This repo has code to use the tweepy package to delete tweets from your timeline that do not fit certain criteria:

- Tweeted within a certain number of days
- or having a certain number of faves/likes
- or having a certain number of retweets

### Usage: 

To see what it would look like to delete your tweets, run the code in testing mode (with `-t` flag) and examine the output (default: `deleted_tweets.csv`):
 
```
python delete_tweets.py -c twitter.config -d 365 -f 0 -r 0 -s tweets.csv -t -v
```

Then remove the `-t` flag to delete those tweets. Like really really. Like for real.

Vaya con dios.