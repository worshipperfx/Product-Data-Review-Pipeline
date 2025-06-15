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


## Workaround

While everything was functional, the Databricks Community Edition does not support the required GCS connector JAR (`com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem`). This prevented direct access to `gs://` paths from Databricks.

After several configuration attempts, a workaround was used to preserve the pipeline:

- Review data was manually downloaded from the GCS bucket.
- Files were uploaded to the Databricks File System (DBFS).
- Data was then read and analyzed using PySpark.

```python
df = spark.read.json("/FileStore/reviews/")
```

This wasn't the original plan, but the workaround allowed the pipeline to continue functioning and enabled full analysis of the data.

## Analysis Performed

- Loaded and parsed product review JSON files
- Grouped reviews by product ID
- Calculated average product ratings
- Identified products with the highest number of reviews
- Used PySpark DataFrame APIs to perform scalable data transformation and aggregation

## Folder Structure

```
├── publisher.py          # Simulates streaming of product reviews
├── subscriber.py         # Saves streamed data to GCS
├── /sample_reviews/      # Sample JSON files manually uploaded to DBFS
├── README.md             # Project documentation
```

## Tech Stack

- Python
- Google Pub/Sub
- Google Cloud Storage (GCS)
- Databricks (Community Edition)
- PySpark

## Key Learnings

- Designing and wiring real-time data pipelines using Google Cloud services
- Managing service account authentication and secure access to GCS
- Working around limitations of cloud platforms like Databricks CE
- Using DBFS as an alternative file ingestion path
- Applying PySpark for cloud-scale data analysis

## Use Case

This project reflects a common use case for e-commerce or SaaS companies: streaming product feedback into cloud storage and performing near real-time analytics to monitor performance, sentiment, or quality issues.

## Future Work

- Automate ingestion from GCS to DBFS using Databricks REST API
- Introduce Delta Lake for versioned review history and rollback support
- Add interactive dashboards via Databricks SQL or external BI tools like Google Looker
- Add monitoring tools for Pub/Sub and end-to-end pipeline freshness
