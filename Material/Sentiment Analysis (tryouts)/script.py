#!/usr/bin/python
from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from sys import argv
import json
import sentiment_analysis
import os


result = open('result.json','a+')
i = 0
big_d ={} 

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="xSXlcimCGWGeTNd3D9j4AG66n"
consumer_secret="DDW6DH60H8pBIgRlBzuIUixfeQYYaGsjv979lGMELUM1QqL4oQ"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="936766788137902080-ESvjG2qhYtK3fvn13v0Jp5WloeerWCd"
access_token_secret="jrGN9M1gT3usZ9yWlXIGfAgLCkGahNLqdDn0fQhzDtssu"

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
	global i
	global big_d
	if (i > 1000):
		exit()
        f = open('file.txt', 'a+')
        j = json.loads(data)
        s = j['text'].encode('utf-8')
        f.write(s)
        print('\n' + s)
        f.truncate()
	simple = {}
        j['score'], j['magnitude'] = sentiment_analysis.analyze('file.txt')
	simple['score']=j['score']  
	simple['timestamp_ms']=j['timestamp_ms']
	f = open('file.txt', 'r+')
	tweet_id = 'tweet' + str(i+1)
	big_d[tweet_id] = simple
	os.remove('result.json')
	result = open('result.json', 'a+')
	json.dump(big_d, result)
	i += 1
        f.close()
	#os.system("gsutil cp result.json gs://tweet_bucket/")
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=[argv[1]])
    result.close()
