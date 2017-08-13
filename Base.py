# coding : utf - 8 - #

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
	'''
	Base Twitter class for sentiment analysis
	'''
	def __init__(self):
		'''
		Initialization method
		'''
		#token keys from twitter dev env
		consumer_key = 'XXXXXXXXXXXXXXXXXX'
		consumer_secret = 'XXXXXXXXXXXXXXXXXX'
		access_token = 'XXX-X'
		acces_token_secret = 'XXXXXXXX'

		#authentication
		try:
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			self.auth.set_access_token(access_token, acces_token_secret)
			self.api = tweepy.API(self.auth)
		except:
			print("Error in Authetication")

	def clean_tweet(self, tweets):
		'''
		Cleans tweet - removes special characters, 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify tweet using textblob
		'''
		analysis = TextBlob(self.clean_tweet(tweet))
		if analysis.sentiment.polarity > 0:
			return "Positive"
		elif analysis.sentiment.polarity == 0:
			return "Neutral"
		else:
		    return "Negative"

	def get_tweets(self, query, count):
		tweets = []
		# Parse tweets
		try:
			fetched_tweets = self.api.search(q = query, c = count)
			for tweet in fetched_tweets:
				parsed_tweets = {}
				parsed_tweets['text'] = tweet.text
				parsed_tweets['sentiment'] = self.get_tweet_sentiment(tweet.text)

				if tweet.retweet_count > 0:
					if parsed_tweets not in tweets:
						tweets.append(parsed_tweets)
				else:
					tweets.append(parsed_tweets)

			return tweets

		except tweepy.TweepError as e:
			print("Error : " + str(e))

def main():
	api = TwitterClient()

	tweets = api.get_tweets(query = '@iam_str', count = 200)



	for tweet in tweets:
		if tweet['sentiment'] == 'Positive':
			print(tweet['text'] + "\n")


if __name__ == '__main__':
	#calling main fun
	main()

			




