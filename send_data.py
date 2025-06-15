

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/chitengamarvellous/nadt-453113-6f397b691ca6.json"

import json
import random
import time
import google.auth
from google.cloud import pubsub_v1

creds, _ = google.auth.default()
print("Authenticated as:", creds.service_account_email)


# Optional: set the path to your JSON key if needed
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/your-username/path-to-your-key.json"

project_id = "nadt-453113"
topic_id = "product-review"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

products =  ["P001", "P002", "P003", "P004","P005", "P006",
     "P007", "P008", "P009", "P0010", "P0012",
      "P0013", "P0014", "P0015"]
reviews = ["Absolutely amazing product!",
    "Works as expected. No complaints.",
    "Not what I expected. Disappointed.",
    "Great quality and value for money.",
    "It's okay, not the best, not the worst.",
    "Terrible. Do not buy this.",
    "I liked it. Decent performance.",
    "Love it! Will definitely buy again.",
    "Stopped working after a week.",
    "Solid product with good features.",
    "Exceeded all expectations!",
    "Average experience overall.",
    "Worst product I’ve ever used.",
    "Top-notch quality. Highly recommend.",
    "Happy with my purchase."]

ratings = [5, 4, 2, 5, 3,
    1, 4, 5, 2, 4,
    5, 3, 1, 5, 4]

while True:
    data_review = {
        "product_id": random.choice(products),
        "review": random.choice(reviews),
        "rating": random.choice(ratings)
    }

    message_json = json.dumps(data_review)
    message_bytes = message_json.encode("utf-8")

    print("About to send message to:", topic_path)
    try:
        future = publisher.publish(topic_path, data=message_bytes)
        message_id = future.result()  # <-- This line waits for confirmation
        print("✅ Sent! Message ID:", message_id)
    except Exception as e:
        print("❌ Failed to publish:", e)

    time.sleep(1)
