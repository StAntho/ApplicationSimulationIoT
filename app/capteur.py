import random
from time import sleep
import os
from datetime import datetime
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from dotenv import load_dotenv

load_dotenv()

# Function to generate a random IoT device ID
def generate_device_id():
    return f"device-{random.randint(1, 5)}"

nb_loops = 0

# Create a Spark session
spark = SparkSession \
    .builder \
    .appName("get-data") \
    .master("local[*]") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate() 

while nb_loops < 10:
    data = []
   # for _ in range(10):  # Loop 10 times
    for i in range(5):  # Generate 5 data points per loop
        data.append({
            "topic": "iot",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "device": "device-"+str(i+1),
            "distance": random.uniform(0.02, 0.25),
            "value": random.randint(1, 5),
            "heart_rate": random.randint(70, 225)
        })
    # print(data)    
    # Create a DataFrame from the data list
    df = spark.createDataFrame(data)
    df.show(5)
    try:
        df.write.option("header", "true").mode("append").csv("hdfs://namenode:9000/iot")
        print("Le DataFrame a été enregistré avec succès en tant que fichiers CSV.")
    except Exception as e:
        print(f"Erreur lors de l'écriture des données dans HDFS : {e}")
# df = df.withColumn("timestamp", current_timestamp())
    # df.write.option("header", "true").mode("append").csv("hdfs://namenode:9000/iot")
    # df.write.option("header", "true").mode("overwrite").csv("hdfs://namenode:9000/iot")
    # print("Le DataFrame a été enregistré avec succès en tant que fichiers CSV.")
    nb_loops += 1
    sleep(15)  # Sleep for 15 seconds