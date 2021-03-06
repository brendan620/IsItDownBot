#!/usr/bin/env python

from secret import *
import tweepy
import time
import random
import validators
import requests


auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)

idFile=open("lastID.txt")
lastTweet=idFile.readline()

while True:
	
	mentionList = api.mentions_timeline(count=1)
	for mention in mentionList:
                
		if(lastTweet != str(mention.id)):
			#Check status
			mentionBody=mention.text.split(" ")
			
			if validators.url(mentionBody[1].strip("@")):
				r = requests.head(mentionBody[1].strip("@"))
				tweet_body = "@" + mention.user.screen_name + " Status code:" + str(r.status_code)
				if str(r.status_code)[0] == "5":
					tweet_body=tweet_body+ ". The page you are requesting appears to be down."
				else:
					tweet_body=tweet_body+ ". The page you are requesting appears to be up."
			else:
				tweet_body = "@" + mention.user.screen_name + " The URL provided was not valid. Please check the Bio for the correct syntax."

			     
			api.update_status(tweet_body ,mention.id)
			lastTweet=str(mention.id)
			idFile=open("lastID.txt",'w')
			idFile.write(str(lastTweet))
	time.sleep(5)

idFile.close()
