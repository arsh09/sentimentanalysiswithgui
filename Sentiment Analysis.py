import re
import tweepy
from textblob import TextBlob
import Tkinter as Tk
import tkinter.ttk as ttk


def connect(query, count=10):

    # Your credential here 
    consumer_key = ''
    consumer_secret = '' 
    access_token = ''
    access_secret = ''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    results = api.search(q=query,count=count)

    # empty list to store parsed tweets
    tweets = []
        
    # parsing tweets one by one
    for tweet in results:
        # empty dictionary to store required params of a tweet
        parsed_tweet = {}

        # saving text of tweet
        parsed_tweet['text'] = tweet.text
        # saving sentiment of tweet
        parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)

        # appending parsed tweet to tweets list
        if tweet.retweet_count > 0:
            # if tweet has retweets, ensure that it is appended only once
            if parsed_tweet not in tweets:
                tweets.append(parsed_tweet)
        else:
            tweets.append(parsed_tweet)

    # return parsed tweets
    return tweets


def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'
 
def main():
    q,c = str(specifictweet.get()),int(tweetcount.get())
    tweets = connect(q,c)
    tweet_file  = open("tweets_analysis.txt","a")
    tweet_file.seek(0)
    tweet_file.truncate(0)
    tweet_file.write("Tweets Analysis from Query: %s\n\n" %((str(q)).capitalize()))
    
   

    finalresult = ""
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    finalresult = "Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)) + "\n"
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    finalresult  = finalresult + ("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) + '\n'
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

    # percentage of neutral tweets
    finalresult = finalresult + ("Neutral tweets percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) + '\n'
    print("Neutral tweets percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

    nutweets = []
    for tweet in tweets:
        if tweet not in ptweets and tweet not in ntweets:
            nutweets.append(tweet)
            
    tweet_file.write("Tweets Retrived: %d\n"%len(tweets))
    tweet_file.write("Results: \n")
    tweet_file.write(finalresult)
    tweet_file.write("\n\n")

    # printing positive tweets
    tweet_file.write("Positive tweets:\n\n")
    i = 1
    for tweet in ptweets:
        tweet_file.write(str(i) + ") ")
        tweet_file.write(tweet['text'].encode('utf-8'))
        tweet_file.write("\n\n")
        i = i+1
        
    # printing negative tweets
    tweet_file.write("Negative tweets:\n\n")
    i = 1
    for tweet in ntweets:
        tweet_file.write(str(i) + ") ")
        tweet_file.write(tweet['text'].encode('utf-8'))
        tweet_file.write("\n\n")
        i = i+1
  
    # printing neurtal tweets
    i = 1
    tweet_file.write("Neutral tweets:\n\n")
    for tweet in nutweets:
        tweet_file.write(str(i) + ") ")
        tweet_file.write(tweet['text'].encode('utf-8'))
        tweet_file.write("\n\n")
        i = i+1

    resultanalyzed.set(finalresult)
   
def sentence():
    result = hashtweet.get()
    result = get_tweet_sentiment(result)
    result = str(result)
    result = result.capitalize()
    resultanalyzed.set(result)



root = Tk.Tk()
root.title("Sentiment Analysis")

#Variables
tweetcount = Tk.IntVar()
hashtweet = Tk.StringVar()
specifictweet = Tk.StringVar()
resultanalyzed = Tk.StringVar()
eachtweet = Tk.StringVar()

#Set Variable for initial values
tweetcount.set(20)
hashtweet.set("Write a sentence")
specifictweet.set("Samsung")
resultanalyzed.set("")

frame1 = Tk.LabelFrame(root,text="Tweets Analyzing Option")
frame1.grid(row=0,column=0,padx = 10,pady = 10,sticky = 'nswe')
frame2 = Tk.LabelFrame(root,text="Button Pallete")
frame2.grid(row=0,column=1,padx = 10,pady = 10,sticky = 'nswe')
frame3 = Tk.LabelFrame(root,text="Analyzed Tweets")
frame3.grid(row=1,column=0,columnspan = 2,padx = 10,pady = 10,sticky = 'nswe')
frame4 = Tk.LabelFrame(root,text="Tweets")
frame4.grid(row=2,column=0,columnspan = 2,padx = 10,pady = 10,sticky = 'nswe')

Tk.Label(frame1,text="Tweet Query: ").grid(row=0,sticky = 'w',padx = 10,pady = 10)
Tk.Label(frame1,text="Number of Tweets: ").grid(row=1,sticky = 'w',padx = 10,pady = 10)
Tk.Label(frame1,text="Specific Sentence: ").grid(row=2,sticky = 'w',padx = 10,pady = 10)

samplex = Tk.Entry(frame1,textvariable = specifictweet).grid(row=0,column=1,sticky='e',padx=5,pady=5)
sampley = Tk.Entry(frame1,textvariable = tweetcount).grid(row=1,column=1,sticky='e',padx=5,pady=5)
deltatime = Tk.Entry(frame1,textvariable = hashtweet).grid(row=2,column=1,sticky='e',padx=5,pady=5)


btn1 = Tk.Button(frame2,width=25,text="Perform Sentiment\nAnalysis on Tweets",command=main)
btn1.grid(row=0,column=0,padx = 10,pady = 10,sticky = 'nswe')
btn2 = Tk.Button(frame2,width=25,text="Perform Sentiment\nAnalysis on Sentence",command=sentence)
btn2.grid(row=1,column=0,padx = 10,pady = 10,sticky = 'nswe')
btn3 = Tk.Button(frame2,width=25,text="Save Results\nTo File")
btn3.grid(row=2,column=0,padx = 10,pady = 10,sticky = 'nswe')

resultLabel = Tk.Label(frame3,textvariable=resultanalyzed)
resultLabel.grid(row=0,column=0,columnspan=2,sticky = 'nswe',padx=10,pady=10)

root.mainloop()


