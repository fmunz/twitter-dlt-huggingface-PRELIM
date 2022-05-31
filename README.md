# 👋🏼 What is this Delta Live Table demo?

I built this Delta Live Tables (DLT) demo to have a more realistic data engineering end-to end demo using Databricks Delta Live Tables. 
DLT is the first ETL framework that uses a simple declarative approach to building reliable data pipelines and automatically managing your infrastructure at scale. Data analysts and engineers can spend less time on tooling and focus on getting value from data. With DLT, engineers are able to treat their data as code and apply modern software engineering best practices like testing, error handling, monitoring and documentation to deploy reliable pipelines at scale.


## The gist

Reading a live Twitter stream, ingestion with schema detection, cleansing and transformation of the data, and applying a bit of ML to it.



<img src="https://github.com/fmunz/twitter-dlt-huggingface/blob/main/markup/twitterstream.jpeg?raw=true" width="800">


## Ingredients
### 📔 The [Twitter-Stream-S3.py notebook](Twitter-Stream-S3.py) uses **[Tweepy](https://www.tweepy.org/)** 👩‍💻

In this demo, I use Tweepy for ingesting a live Twitter stream based on search criteria that can be be defined, such as "DLT" and "data engineering". The ingested Twitter data is streamed to an S3 bucket. Imagine this S3 bucket as your data lake. With Databricks I can use DBFS to abstract the cloud object store as a folder (DBFS is multicloud, it will work the same on ADFS2 and GCS too)  

### 📔 The [Twitter-Dataflow.sql notebook](Twitter-DataFlow.sql) uses **[Delta Live Tables](https://databricks.com/product/delta-live-tables) in SQL with Autoloader** 

What matters in DLT is the "P". "P" for "pipeline". In this example DLT is used together with Databricks Autoloader. Autoloader ingests streaming data and detects the schema. DLT creates a Bronze table for the raw data, then filters the 40 columns per tweet and cleans the data to ensure only tweets in English are contained. Cleaning data is done with SQL constraints (we like to call them Expectations in DLT lingo).   


<img src="https://raw.githubusercontent.com/fmunz/twitter-dlt-huggingface/main/markup/lineage.jpg" width="800">



### 📔 The [Twitter-SentimentAnalysis.py Notebook](Twitter-SentimentAnalysis.py) uses  **Hugging Face Sentiment Analysis Pipelines**

For sentiment analysis, I picked Hugging Face because I could (the Databricks platform is open and flexible, any ML will work). It doesn't get much easier than using a pretrained Hugging Face language model that is even optized for tweets (it detects :-), 😀, 🥲 and so on). The goal here was to show how almost any kind of ML can be used within the Lakehouse with emphasis on simplicity.


<img src="https://raw.githubusercontent.com/fmunz/twitter-dlt-huggingface/main/markup/sentiment.jpg" width="800">

For a much more advanced discussion of [Hugging Face with Databricks see the this blog](https://databricks.com/blog/2021/10/28/gpu-accelerated-sentiment-analysis-using-pytorch-and-huggingface-on-databricks.html). 


### ✅ **Databricks Workflow**

If you have see a recording of this demo, you will understand how I struggle to switch between the different notebooks for the Twitter Stream, DLT, and ML. Of course this needs to be automated. I am using Databricks Workflows for this and simply create three tasks: one for ingestion with the notebook that is using Tweepy, one task that runs the DLT pipeline, and a third task for the sentiment analysis. This is a workflow example that uses different task types, such as Python notebooks and DLT pipelines. 
<img src="https://github.com/fmunz/twitter-dlt-huggingface/blob/main/markup/matrix.jpg?raw=true" width="800">

So if the Workflow is not part of this repository, how can you create your own workflow? Watch this demo about [Databricks Workflows](https://www.youtube.com/watch?v=H2FS4ijpFZA) to get started.



## Run the Demo 🚀 yourself
### 🐑 Clone the Repo
Use [Databricks Repos](https://docs.databricks.com/repos/index.html#clone-a-remote-git-repository) from your workspace to clone the repo and get started with this demo. The repo consists of the notebooks listed above. The workflow is not part of the repo.

### Requirements

* Since the data is streamed live from twitter you have to create Twitter credentials. Ideally you should store them as a Databricks secret and read the from the Twitter-Stream-S3 notebook. Since I experiment a lot with my demo, I added the credentials directly but externalized this step into a separate notebook that is not on githuib, to keep the code simple. 
* Create a directory in DBFS to store the streamed tweets. The helper functions that I use for that are at the bottom of the Twitter-Stream-S3 notebook. 
* Define the Tweepy search expression to something that you enjoy. Note for the sake of this demo I include Spanish and German tweets. Later I use Delta Live Table expectations to ensure the ML pipeline will only work with EN tweets.
* You can stop the data collection at any time if you like. The code will work with old tweets from the DBFS directory. 


### DBR Version
The features used in the notebooks were tested on DBR 10.1 ML. Make sure to use a ML runtime, otherwise the notebook with the Sentiment Analysis will complain about missing libraries (which you could of course install manually, but it is not worth the effort).



### 🤝 Feedback and contributing

* I am happy to accept pull requests but please keep in mind that the focus of this demo is on DLT and simplicity. So I am not looking for more complexity in the ingestion or ML part, however I'd appreciate some cool visualizations of the final data. 
* A friend of mine, [Srijith](https://www.linkedin.com/in/srijith-rajamohan-ph-d-4242b9a/) provided a very first version of the Tweepy code. Some design ideas of this page are adapted from @pyr0gan's README. 
