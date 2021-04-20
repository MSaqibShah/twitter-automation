from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials


# # # # Twitter Client # # # #
class TwitterClient():
    def __init__(self,twitter_user=NONE):
        self.auth = TwitterAuth().auth_twitter_app()
        self.twitter_client = API(self.auth)

    def get_user_timeline_tweets(self,num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline).items(num_tweets):
            tweets.append(tweet)
        return tweets

# # # # Twitter Authenticator # # # #
class TwitterAuth():
    #Authentcates Twitter
    def auth_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_auth = TwitterAuth()

    def stream_tweets(self, fetched_tweets_filename, hashtag_list):
        #This handles Twitter auth and the connection to the Twitter Streaming APT
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_auth.auth_twitter_app()
        stream = Stream(auth, listener)
        stream.filter(track=hashtag_list)

class TwitterListener(StreamListener):
    """
    Basic Listener Class that print recieved tweets to StdOut
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" %str(e))
        return True

    def on_error(self, status):
        if status == 420:
            return False  #Kills the connection in case data rate limit occurs
        print(status)


if __name__ == "__main__" :

    hashtag_list =['Ball', 'Bat', 'Beach','Sun']
    fetched_tweets_filename = "tweets.json"

    twitter_client = TwitterClient()
    print(twitter_client.get_user_timeline_tweets(1))
    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweets_filename, hashtag_list)
