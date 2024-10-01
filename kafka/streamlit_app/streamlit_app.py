import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *
import time
import io
import json
from hdfs import InsecureClient
import pyarrow.parquet as pq
import pandas as pd

# schema = StructType(
#     [
#         StructField("sensor_id", StringType(), True),
#         StructField("timestamp", StringType(), True),
#         StructField("temperature", FloatType(), True),
#         StructField("humidity", FloatType(), True),
#         StructField("heart_rate", StringType(), True),
#         StructField("value", IntegerType(), True),
#         StructField("distance", FloatType(), True),
#     ]
# )

# # Initialisation de la SparkSession
# spark = SparkSession.builder \
#     .appName("streaming-velib") \
#     .master("local[*]") \
#     .getOrCreate()

# spark.sparkContext.setLogLevel("ERROR")

# # Récupération des données
# df = spark \
#     .readStream \
#     .option("header", "true") \
#     .schema(schema) \
#     .csv("hdfs://namenode:9000/user/anthony/sensor_data_parquet")

# if 'query1' in locals() and query1.isActive:
#     query1.stop()
#     print("La requête velib_table a été arrêtée.")

# query1 = df \
#     .writeStream \
#     .outputMode("append") \
#     .format("memory") \
#     .queryName("velib_table") \
#     .start()

# query1.awaitTermination(2)

# state = True
# while query1.isActive:
#     df_pandas = spark.sql("SELECT * FROM velib_table").toPandas()
#     st.write(df_pandas)

st.title('Kafka Streamlit App')

hdfs_url = "http://namenode:9870"  # URL du service Web HDFS
hdfs_user = "your_hdfs_username"   # Nom d'utilisateur HDFS
client = InsecureClient(hdfs_url, user=hdfs_user)

def read_parquet_files_from_hdfs(hdfs_directory):
    """Lire tous les fichiers Parquet dans un répertoire HDFS et les combiner en un DataFrame pandas."""
    
    # Lister tous les fichiers Parquet dans le répertoire
    files = client.list(hdfs_directory)
    
    # Lire et combiner les fichiers Parquet
    dfs = []
    for file in files:
        if file.endswith('.parquet'):
            hdfs_path = f"{hdfs_directory}/{file}"
            with client.read(hdfs_path) as reader:
                buffer = io.BytesIO(reader.read())
                table = pq.read_table(buffer)
                df = table.to_pandas()
                dfs.append(df)
    
    # Combiner tous les DataFrames en un seul
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()

def start_streaming():
    placeholder = st.empty()

    while True:
        # Lire les fichiers Parquet dans le répertoire HDFS
        df = read_parquet_files_from_hdfs('/user/anthony/sensor_data_parquet')
        
        # Afficher les données dans Streamlit
        if not df.empty:
            placeholder.write(df)
        
        # Pause pour éviter de surcharger le système
        time.sleep(5)


start_streaming()