from credentials import *
import tweepy

class Twitter:

    def __init__(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def listen(self):
        print("Checking Tweets...")
        tweets = self.api.search(q="@AlkanPlotter")
        for tweet in tweets:
            if "@AlkanPlotter" in tweet.text:
                user = tweet.user.screen_name
                name = tweet.text.replace("@AlkanPlotter", "").replace(" ", "")
                print("Name von Twitter: " + str(name))
                return (username, tweet.id, name)

    def reply(self, username, tweetid, name, data):
        tweet = self.api.update_with_media(data, "@" + username + " " + name, in_reply_to_status_id = tweetid)
