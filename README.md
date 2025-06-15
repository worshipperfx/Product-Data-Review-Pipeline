# Product-Data-Review-Pipeline
Product Review Streaming Pipeline


#  Real-Time Product Review Streaming Pipeline

A full-scale data pipeline that ingests product reviews from e-commerce systems, streams them in real-time via Google Pub/Sub, stores them in Google Cloud Storage (GCS), and processes them in Databricks using PySpark.

---

##  Project Overview

This project simulates how modern businesses can track and analyze product feedback in near real-time using scalable data engineering tools.

The pipeline architecture includes:

Python Script (Review Generator) → Google Pub/Sub → GCS Bucket → Databricks (PySpark Analytics)


---

##  Components

###  Publisher (Python)
- Simulates real-time product reviews in JSON format.
- Streams data to a **Google Pub/Sub topic** named `product-review`.

###  Subscriber (Python)
- Subscribes to the `product-review` topic.
- Saves incoming messages as individual `.json` files into the `reviews/` folder inside the `product-review-bucket` on **Google Cloud Storage**.

### ☁ GCS Bucket
- Bucket Name: `product-review-bucket`
- Acts as the landing zone for all incoming product review data.
- Proper service account permissions set (e.g., Storage Object Creator).

###  Databricks (PySpark)
- Reads and analyzes the review data using **PySpark**.
- Key analytics: review counts per product, average rating distribution, identification of top-performing products.

---

##  Databricks Integration Challenge

When attempting to read directly from the GCS bucket:
```python
spark.read.json("gs://product-review-bucket/reviews/")
An error occurred:


java.lang.ClassNotFoundException: com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem
This happens because Databricks Community Edition does not support custom JARs — including the required GCS connector.

```
 Workaround
To maintain the pipeline's integrity:

Review data was manually downloaded from the GCS bucket.

Files were uploaded to Databricks File System (DBFS).

Data was then loaded and analyzed in PySpark:


df = spark.read.json("/FileStore/reviews/")
While not the original approach, the workaround preserved the pipeline's end-to-end flow and allowed full data analysis.

Analysis Performed
Loaded and parsed product reviews

Grouped reviews by product ID

Calculated average ratings

Identified products with the highest feedback volume

Used PySpark DataFrame APIs for scalable transformation and aggregation

Folder Structure

├── publisher.py               # Simulates streaming of product reviews
├── subscriber.py              # Saves streamed data to GCS
├── /sample_reviews/           # Sample JSON files from GCS
├── README.md                  # Project documentation
⚙ Tech Stack
Python

Google Pub/Sub

Google Cloud Storage (GCS)

Databricks (Community Edition)

PySpark

 Key Learnings
Designing and wiring real-time data pipelines using GCP services

Managing service account authentication securely

Overcoming connector limitations within Databricks Community Edition

Understanding file-based ingestion workflows in DBFS

Using PySpark for scalable, cloud-based data analysis

 Use Case
This pipeline reflects how e-commerce companies or SaaS platforms can stream product feedback, ingest it into cloud storage, and perform near real-time analytics to monitor sentiment, performance, and quality issues.

 Future Work
Automate GCS → DBFS ingestion with Databricks REST API

Add Delta Lake for versioned review history

Integrate visualization with Databricks SQL or Google Looker

Add monitoring for Pub/Sub + data freshness
