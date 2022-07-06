# Databricks notebook source
# MAGIC %md
# MAGIC # TwitterStream to S3 / DBFS
# MAGIC 
# MAGIC * [DLT Pipeline](https://data-ai-lakehouse.cloud.databricks.com/?o=2847375137997282#joblist/pipelines/e5a33172-4c5c-459b-ab32-c9f3c720fcac)
# MAGIC * [Huggingface Sentiment Analysis](https://data-ai-lakehouse.cloud.databricks.com/?o=2847375137997282#notebook/3842290145331470/command/3842290145331471)

# COMMAND ----------

# this demo requires a bearer token for Twitter from https://developer.twitter.com/en
#
# use databricks secrets with the CLI to store and retrieve it in a safe way.
# for a first try, you could configure your twitter bearer token here, but I recommend against doing so.
bearer_token = "XXXX"

# in my demo, I read in the bearer from another notebook in the cell below (which can be savely removed or commented out)
# note: Twitter API version 1 uses Twitter API keys, version 2 just a bearer token


# COMMAND ----------

# remove this cell (used to set my Twitter token)
%run "./TwitterSetup"

# COMMAND ----------

!/databricks/python3/bin/python -m pip install --upgrade pip

# COMMAND ----------

!pip install tweepy jsonpickle colorama

# COMMAND ----------

import tweepy
import calendar
import time
import jsonpickle
import sys

from colorama import Fore
from colorama import Style


dbfs_dir = "/dbfs/data/twitter_summer2022"

# unlike V1 of the twitter API, V2 does not return all tweet attributes anylonger, so for demo purposes I added a few here 
fields = "lang,geo,author_id,conversation_id,created_at,referenced_tweets,reply_settings,source,in_reply_to_user_id,non_public_metrics,organic_metrics,public_metrics" 


# subclass StreamingClient
class myStream(tweepy.StreamingClient):

    # initializer
    def __init__(self, bearer_token, dirname):
        tweepy.StreamingClient.__init__(self,bearer_token)
        self.dirname = dirname
        self.text_count = 0
        self.tweet_stack = []

        
    # called for every tweet
    def on_tweet(self, tweet):
        #print('*'+tweet.text)
        self.text_count = self.text_count + 1
        self.tweet_stack.append(tweet)
    
        # when to print
        if (self.text_count % 1 == 0):
            print(f"{Fore.BLUE}tweet {self.text_count} from stream:{Style.RESET_ALL} {tweet.text}")
            #print(f'writing tweet: {Fore.RED}{jsonpickle.encode(tweet, unpicklable=False)}{Style.RESET_ALL}')
            
        # how many tweets to batch into one file
        if (self.text_count % 5 == 0):
            self.write_file()
            self.tweet_stack = []

        # hard exit after collecting n tweets
        if (self.text_count == 50000):
            raise Exception("Finished job")

    def write_file(self):
        file_timestamp = calendar.timegm(time.gmtime())
        fname = self.dirname + '/tweets_' + str(file_timestamp) + '.json'
        print(f'{Fore.GREEN}writing tweets to:{Style.RESET_ALL} {fname}')
        
        with open(fname, 'w') as f:
          for tweet in self.tweet_stack:
            f.write(jsonpickle.encode(tweet, unpicklable=False) + '\n')
            
    def on_error(self, status_code):
        print("Error with code ", status_code)
        sys.exit()





tweet_stream = myStream(bearer_token, dbfs_dir)
try:  
    # filter stream
    # see https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule
    #
    tweet_stream.add_rules(tweepy.StreamRule("DAIS2022 OR DLT OR Delta Live Tables OR Data Science OR Databricks "))
    tweet_stream.filter(threaded=False, tweet_fields=fields)
  

except Exception as e:
    print("some error ", e)
    print("Writing out tweets file before I have to exit")
    tweet_stream.write_file()
finally:
    print("Downloaded tweets ", tweet_stream.text_count)
    tweet_stream.disconnect()


# COMMAND ----------

dbutils.notebook.exit("stop")

# COMMAND ----------

# MAGIC %md
# MAGIC # Setup Utilities

# COMMAND ----------

# MAGIC %md 
# MAGIC Create new data directory for tweets

# COMMAND ----------

# create a directory to buffer the streamed data
!mkdir "/dbfs/data/twitter_summer2022"

# COMMAND ----------

# MAGIC %md 
# MAGIC Number of files, -> small files problem, DLT solves it (check with Data Explorer)

# COMMAND ----------

# create a directory to buffer the streamed data
!ls -l /dbfs/data/twitter_summer2022 | wc

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC Delete n files from DBFS directory to trim down demo

# COMMAND ----------

files = dbutils.fs.ls("/data/twitter_summer2022")
d = 500
print(f'number of files: {len(files)}')
print(f'number of files to delete: {d}')


for x, file in enumerate(files):
  # delete n files from directory
  if x < d :
    # print(x, file)
    dbutils.fs.rm(file.path)

    
# use dbutils to copy over files... 
# dbutils.fs.cp("/data/twitter_dataeng/" +f, "/data/twitter_dataeng2/")

# COMMAND ----------


