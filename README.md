# delete_tweets

This repo has code to use the tweepy package to delete tweets from your timeline that do not fit certain criteria:

- Tweeted within a certain number of days
- or having a certain number of faves/likes
- or having a certain number of retweets

### Setup

You will need to create a developer account at [developer.twitter.com](https://developer.twitter.com). 

Once you're approved, you can create an app. Make sure your app has Read and write permissions, so you can see tweets and also delete them.

Your app setup should look like this:
![Image of app](https://github.com/gaurav-kaushik/delete_tweets/blob/master/images/twitter_app.png?raw=true)

Copy + paste your API keys and tokens in the right locations in `template.config`. You can use this file to run the code.

If the code errors because of API issues, make sure you have the correct permissions, regenerate your tokens/credentials, update your config file, and use the right config file in running the code.

### Usage

To see what it would look like to delete your tweets, run the code in testing mode (with `-t` flag) and examine the output (default: `deleted_tweets.csv`):
 
```
python delete_tweets.py -c template.config -d 365 -f 0 -r 0 -s tweets.csv -t -v
```

Then remove the `-t` flag to delete those tweets. Like really really. Like for real.

Vaya con dios.