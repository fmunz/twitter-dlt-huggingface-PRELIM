# 👋🏼 What is this demo?

I built this Delta Live Tables (DLT) demo to provide a more realistic end-to end demo using Databricks Delta Live Tables. 
DLT is the first ETL framework that uses a simple declarative approach to building reliable data pipelines and automatically managing your infrastructure at scale. Data analysts and engineers can spend less time on tooling and focus on getting value from data. With DLT, engineers are able to treat their data as code and apply modern software engineering best practices like testing, error handling, monitoring and documentation to deploy reliable pipelines at scale.


## The gist

Reading a live Twitter stream, cleansing and transforming the data, applying a bit of ML to it with three lines of code.
<img src="https://raw.githubusercontent.com/fmunz/dlt-l300/main/twitterstream.jpg" width="800">
<!--
![Diagram](https://raw.githubusercontent.com/fmunz/dlt-l300/main/twitterstream.jpg)
-->

## 🤔 What it consists of 
✅ **[Tweepy](https://www.tweepy.org/)** 

I use Tweepy for ingesting live Twitter data. The ingested Twitter data is streamed to an S3 bucket (imagine this as your data lake). With Databricks I can use DBFS to abstract the cloud object store as a folder (this is multicloud, it will for ADFS2 and GCS too)  

✅ **Databricks Delta Live Tables in SQL with Autoloader** 

What matters is the "P" in DLT. "P" for "pipeline". In this example DLT is used together with Databricks Autoloader. Autoloader ingests streaming data and detects the schema. DLT creates a Bronze table for the raw data, then filters the over 40 columns and cleans the data to ensure only tweets in English are contained using SQL constraints (we like to call them Expectations in DLT lingo).   


✅ **Hugging Face Sentiment Analysis**

For sentiment analysis, I picked Hugging Face because I could (the Databricks platform is open and flexible, any ML will work). It doesn't get much easier than using a pretrained Hugging Face language model that is even optized for tweets (it detects :-), 😀, 🥲 and so on). 


✅ **Databricks Workflow**

If you have see a recording of this demo, you will understand how I struggle to switch between the different notebooks for the Twitter Stream, DLT, and ML. Of course this needs to be automated, I use Databricks Workflows for this and simple create three tasks. It's a nice example that show how Python Notebook is scheduled first, followed by a DLT task, followed by the ML task



# 🚀 Setup 

## 🐑 Clone this Demo

Welcome to the repository for the Twitter Stream - DLT - Huggingface Demo

You can use Databricks Projects to clone this repo and get started with this demo, or download the .dbc archive and import the notebooks manually.

## DBR Version
The features used in the notebooks were tested on DBR 10.1 ML. Make sure to use a ML DBR, otherwise the ML part will complain about missing libraries. 


# More demos?

## 🍿 Databricks Workflows
Interested about more details of orchestration in the Lakehouse? Watch this demo about [Workflows](https://www.youtube.com/watch?v=H2FS4ijpFZA)
## 🍿 Divy Bikes 🚲 🚴 🚲 🚴
Another great end-to-end demo about [Divvy bike rentals in Chicago](https://databricks.com/blog/2022/05/19/how-i-built-a-streaming-analytics-app-with-sql-and-delta-live-tables.html). [Recording](https://www.youtube.com/watch?v=BIxwoO65ylY&feature=youtu.be) 

# 🤝 Feedback and contributing



## 🙏 Credits
A friend of mine, [Srijith](https://www.linkedin.com/in/srijith-rajamohan-ph-d-4242b9a/) provided a very first version of the Tweepy code. Some design ideas of this page are adapted from @pyr0gan's README. 
