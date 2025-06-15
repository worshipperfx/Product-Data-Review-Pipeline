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


 ## 🔁 Workaround

To keep the pipeline functional despite connector limitations in Databricks Community Edition:

- The review data was manually downloaded from the GCS bucket.
- These JSON files were then uploaded to **Databricks File System (DBFS)**.
- From there, the data was read and analyzed using PySpark:


df = spark.read.json("/FileStore/reviews/")

Although this wasn't the original plan, the workaround ensured the pipeline ran end-to-end and gave full access to the data for analysis.

Analysis Performed

Parsed product review JSON files

Grouped reviews by product ID

Calculated average ratings per product

Identified products with the highest review counts

Used PySpark DataFrame APIs for efficient transformation and aggregation

Folder Structure

├── publisher.py          # Simulates streaming of product reviews
├── subscriber.py         # Saves streamed data to GCS
├── /sample_reviews/      # Sample JSON files manually uploaded to DBFS
├── README.md             # Project documentation
⚙ Tech Stack
Python

Google Pub/Sub

Google Cloud Storage (GCS)

Databricks (Community Edition)

PySpark


Key Learnings

Building real-time data pipelines using Google Cloud tools

Handling authentication and permissions for cloud services

Working around limitations in managed platforms (e.g., missing JAR support)

Using DBFS for local ingestion and analysis in Databricks

Applying PySpark for distributed data processing

Use Case

This pipeline demonstrates how an e-commerce platform or SaaS company could ingest and analyze product reviews in real-time, helping teams monitor product performance and customer sentiment quickly.

Future Work

Automate the GCS → DBFS ingestion with the Databricks REST API

Add Delta Lake for version control and historical queries

Build visual dashboards using Databricks SQL or Google Looker

Add pipeline monitoring to track message flow and data freshness



---

Let me know if you want the full README assembled with these or just this section updated in your w

