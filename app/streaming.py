from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("device", StringType(), False),
    StructField("heart_rate", StringType(), False),
    StructField("timestamp", StringType(), False),
    StructField("topic", IntegerType(), False),
    StructField("value", IntegerType(), False),
])

# Initialisation de la SparkSession
spark = SparkSession \
    .builder \
    .appName("streaming-iot") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Récupération des données
df = spark \
    .readStream \
    .option("header", "true") \
    .schema(schema) \
    .csv("hdfs://namenode:9000/iot")
# stream = spark \
#     .readStream \
#     .schema(schema) \
#     .json("hdfs://namenode:9000/iot")
# Query n°1 : Lire sans les données traitement
query1 = df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()
print(query1)