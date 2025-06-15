import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/chitengamarvellous/nadt-453113-6f397b691ca6.json"
import time
import json
import google.auth
creds, project = google.auth.default()
print("Authenticated as:", creds.service_account_email)
from google.cloud import pubsub_v1
from google.cloud import storage

project_id = "nadt-453113"
subscription_id = "sub-review"
topic_id = "product-review"
bucket_name = "product-review-bucket"

subscriber = pubsub_v1.SubscriberClient()
subscriber_path = subscriber.subscription_path(project_id, subscription_id)
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

def callback(message):
    try:
        review_json = message.data.decode("utf-8")
        review_dict = json.loads(review_json)

        timestamp = int(time.time() * 1000)
        filename = f"reviews/review{timestamp}.json"
        blob = bucket.blob(filename)
        blob.upload_from_string(review_json, content_type="applicaton/json")
        print(f"Saved review to bucket: {filename}")
        message.ack()
    except Exception as e:
        print("Error processing message", e)
        message.ack()

print("Listening to messages:", subscriber_path)
streaming_pull_future = subscriber.subscribe(subscriber_path, callback=callback)
try:
    streaming_pull_future.result()
except Exception as e:
    streaming_pull_future.cancel()
    print("Stopped listening to messages", e)
