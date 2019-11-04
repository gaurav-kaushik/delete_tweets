# delete_tweets

This repo has code to use the tweepy package to delete tweets from your timeline that do not fit certain criteria:

- Tweeted within a certain number of days
- or having a certain number of faves/likes
- or having a certain number of retweets

### Setup

You will need to create a developer account at [developer.twitter.com](https://developer.twitter.com). 

Once you're approved, you can create an app. Make sure your app has Read and write permissions, so you can see tweets and also delete them.

Your app setup should look like this:


Copy + paste those credentials in the right location in `template.config`. You can use this file to run the code.

If the code errors because of API issues, make sure you have the correct permissions, regenerate your tokens/credentials, and update your config file.

### Usage: 

To see what it would look like to delete your tweets, run the code in testing mode (with `-t` flag) and examine the output (default: `deleted_tweets.csv`):
 
```
python delete_tweets.py -c twitter.config -d 365 -f 0 -r 0 -s tweets.csv -t -v
```

Then remove the `-t` flag to delete those tweets. Like really really. Like for real.

Vaya con dios.