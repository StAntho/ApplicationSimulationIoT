from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *

# Creer la session Spark
spark = SparkSession.builder.appName("TemperatureSensorStreaming").getOrCreate()

# Mute les logs inferieur au niveau Warning
spark.sparkContext.setLogLevel("WARN")

# Define the schema of the JSON messages
schema = StructType(
    [
        StructField("sensor_id", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("temperature", FloatType(), True),
        StructField("humidity", FloatType(), True),
        StructField("heart_rate", StringType(), True),
        StructField("value", IntegerType(), True),
        StructField("distance", FloatType(), True),
    ]
)

# Selectionner mon topic
kafka_topic_name = "topic1"

# Selectionner mon server
kafka_bootstrap_servers = 'kafka:9092'

# Recuperation de mes data de mon stream kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
  .option("subscribe", kafka_topic_name) \
  .load()


# Parse the JSON messages
kafkaStream = df.selectExpr("CAST(value AS STRING) as json")
parsed = kafkaStream.select(from_json(col("json"), schema).alias("data")).select(
    "data.*"
)

# Convert timestamp to TimestampType
parsed = parsed.withColumn("timestamp", col("timestamp").cast(TimestampType()))

# Show the DataFrame
query = parsed.writeStream.outputMode("append").format("console").start()

# parsed.show()
# try:
#     df.write.option("header", "true").mode("append").csv("hdfs://namenode:9000/kafkaIot")
#     print("Le DataFrame a été enregistré avec succès en tant que fichiers CSV.")
# except Exception as e:
#     print(f"Erreur lors de l'écriture des données dans HDFS : {e}")

# query = parsed.writeStream \
#     .outputMode("append") \
#     .format("csv") \
#     .option("path", "/app/data") \
#     .option("checkpointLocation", "/myhadoop") \
#     .option("header", "true") \
#     .option("truncate", "false") \
#     .start()

# Save the DataFrame to HDFS
query = (
    parsed.writeStream.outputMode("append")
    .format("parquet")
    .option("path", "hdfs://namenode:9000/user/anthony/sensor_data_parquet")
    .option("checkpointLocation", "hdfs://namenode:9000/user/anthony/sensor_data_checkpoint")
    .start()
)

query.awaitTermination()
