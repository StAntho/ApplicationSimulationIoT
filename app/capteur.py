import random
import os
from datetime import datetime
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Function to generate a random IoT device ID
def generate_device_id():
    return f"device-{random.randint(1, 5)}"

spark = SparkSession \
    .builder \
    .appName("get-data") \
    .master("local[*]") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()

data = []
for _ in range(10):  # Loop 10 times
    # for _ in range(5):  # Generate 5 data points per loop
    data.append({
        "topic": "iot",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "device": generate_device_id(),
        "value": random.randint(1, 5),
        "heart_rate": random.randint(70, 225)
    })
print(data)    

# Convert data to JSON string
# json_data = json.dumps(data)
# print(json_data)
# datas = json_data.json()
df = spark.createDataFrame(data)
print(df.show(5))
# df = df.withColumn("timestamp", current_timestamp())
df.write.option("header", "true").mode("overwrite").csv("hdfs://namenode:9000/iot")
print("Le DataFrame a été enregistré avec succès en tant que fichiers CSV.")
# Convert JSON string to a dictionary (assuming valid JSON)
# data_dict = json.loads(json_data)

    # csv_data = []
    # # Access data using dictionary keys
    # csv_row = [data_dict["timestamp"], data_dict["device"], str(data_dict["value"])]  # Convert value to string
    # csv_data.append(csv_row)
    # print(csv_data)

    # # Generate random filename (avoid potential collisions)
    # filename = f"/tmp/iot_{random.randint(10000, 99999)}.txt"

    # # with open(filename, "wb") as f:
    # #     f.write(file_content)

    # hdfs = hdfs3.HDFSMap("namenode", 9000)
    # with hdfs.open('iot/',filename, "w", encoding='utf-8') as hdfs_file:
    #     csv_writer = csv.writer(hdfs_file)
    #     csv_writer.writerow(["timestamp", "device", "value"])
    #     csv_writer.writerows(csv_data)

    # # Execute HDFS put command using subprocess
    # hdfs_put_command = f"hdfs://namenode:9000 dfs -put -f {filename} /iot/"
    # os.system(hdfs_put_command)

    # Optionally delete the temporary file (consider error handling)
    # os.remove(filename)