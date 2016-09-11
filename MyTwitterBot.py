#from lmxl import html

import requests
import re
import tweepy
from nltk.tokenize import word_tokenize  # to break a string into words. 
import nltk.data
import json
import csv

#nltk.download('punkt')
# document = word_tokenize(text)

SECRETS_FILE = "/Users/tialerud/Documents/Twitterbot/secrets.json"
biz_dict_file = "/Users/tialerud/Documents/Twitterbot/bizfydict.csv"

def main():
    ##### Twitter API setup
    with open(SECRETS_FILE) as f:
        secrets = json.load(f)
    auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
    auth.set_access_token(secrets['access_token'], secrets['access_secret'])
    api = tweepy.API(auth)


    ##### Defining required functions and classes #####
    # Turn a two columned csv into a dictionary
    def csv_to_dict(file):
        myDict = {}
        with open(file) as f:
            for line in f:
                (key, val) = line.split(",")
                myDict[key] = val
        return myDict


    # Translate into business speak
    def bizify(status, biz_dict):
        #print(status)
        parsed_status = word_tokenize(status)

        #biz_dict_temp = {'use':'utilize','plan':'action plan','brainstorm':'ideate'}
        #tweet = word_tokenize("Let's brainstorm a plan to use this new tech.")
        tweet_temp = parsed_status

        i = 0
        #counter = 0
        for word in parsed_status:
            if word in biz_dict:
                #counter +=1
                print("yay,",word,"is in the dictionary and maps to ", biz_dict[word])
                tweet_temp[i] = biz_dict[word]
            i +=1
        #if counter == 0:
        #    tweet_temp = "huh?"    

        return " ".join(tweet_temp).strip()
    

    # override tweepy.StreamListener to add logic to on_status
    class MyStreamListener(tweepy.StreamListener):

        def on_connect(self):
            print("connected")

        def on_status(self, status):
            out_bound_status_update = bizify(status.text, biz_dict)
            api.update_status(out_bound_status_update)

        def on_error(self, status_code):
            if status_code == 420:
                print("error code 420")
                #returning False in on_data disconnects the stream
                #return False   


    #####   Done with function and class definition #####

    mydict = dict([('regardless','irregardless'),
    ('appearance','optics'),
    ('change','delta'),
    ('investigation','deep dive'),
    ('respond','circle back'),
    ('finish','close the loop on'),
    ('findings','insights'),
    ('useful','actionable'),
    ('find','surface'),
    ('agreement','alignment'),
    ('important','impactful'),
    ('discuss','dialogue'),
    ('brainstorm','ideation'),
    ('coworker','colleague'),
    ('faster','performant'),
    ('plan','action plan'),
    ('easy','low-hanging fruit'),
    ('data','big data'),
    ('think',"wrap our head's around this"),
    ('use','leverage'),
    ('benefit','ROI'),
    ('complete','run this to the ground'),
    ('meeting','mind meld'),
    ('comparison','apples to apples comparison'),
    ('goal-oriented','solution-oriented'),
    ('improve','create efficiences'),
    ('use','utilize'),
    ('rhythm','cadence'),
    ('new','game-changing'),
    ('contact','gatekeeper'),
    ('start','gain traction'),
    ('problem','pain point'),
    ('improvement','value-add'),
    ('highlight','bring out the wow factor'),
    ('awareness','visibility'),
    ('charged','tasked'),
    ('explain','socialize'),
    ('employees','talent')])
    
    # process biz dict here so not called repeatedly within stream
    biz_dict = mydict
    #biz_dict = csv_to_dict(biz_dict_file)
    #biz_dict_temp = {'use':'utilize','plan':'action plan','brainstorm':'ideate'}

    # set up stream
    myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())
    myStream.filter(track=["@rillestat"]) #,async=True


if __name__ == '__main__':
    main()