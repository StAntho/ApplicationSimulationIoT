import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from time import sleep
from functions import *
import pandas as pd

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

# Arrêter la requête iot_table si elle est active
if 'query1' in locals() and query1.isActive:
    query1.stop()
    print("La requête iot_table a été arrêtée.")

query1 = df \
    .writeStream \
    .outputMode("append") \
    .format("memory") \
    .queryName("iot_table") \
    .start()

query1.awaitTermination(2)

st.title("Simulation de d'analyse de données par capteur avec Spark")

# Afficher les données à intervalles réguliers
state = True
age_1 = 22
age_2 = 25
age_3 = 31
age_4 = 24
age_5 = 35
height_1 = 182
height_2 = 177
height_3 = 181
height_4 = 179
height_5 = 190
weight_1 = 85
weight_2 = 80
weight_3 = 79
weight_4 = 77
weight_5 = 95

while query1.isActive:
    # Convertir le DataFrame Spark en DataFrame Pandas
    df_pandas = spark.sql("SELECT * FROM iot_table").toPandas()
    df_pandas
    devices = spark.sql("SELECT DISTINCT(device) FROM iot_table").toPandas()
    if len(df_pandas.device) > 0:
         devices = devices[(devices['device'] != 'false')].dropna(subset=['device'])
         state = False
         query1.stop()
         device = st.selectbox("Sélectionnez une device", devices)
         if device != '':
            df_filtered = df_pandas[df_pandas['device'] == device]
            df_filtered = df_filtered.drop(columns=['topic'])
            df_filtered['heart_rate'] = df_filtered.apply(lambda row: f"{int(row['heart_rate'])}", axis=1)
            df_filtered['value'] = df_filtered.apply(lambda row: f"{int(row['value'])}", axis=1)
            df_filtered['timestamp'] = pd.to_datetime(df_filtered['timestamp'])

            df_filtered = df_filtered[['device', 'heart_rate', 'value', 'timestamp']]

            df_filtered.rename(columns={'heart_rate': 'Fréquence cardiaque'}, inplace=True)
            df_filtered.rename(columns={'value': 'Value'}, inplace=True)
            # df_filtered.rename(columns={'timestamp': 'time'}, inplace=True)
            df_filtered.rename(columns={'device': 'device'}, inplace=True)

            st.markdown(df_filtered.style.hide().to_html(), unsafe_allow_html=True)              
        # col1, col2, col3, col4, col5 = st.columns(5)
        # with col1:
            df_filtered1 = df_pandas[df_pandas['device'] == 'device-1']
            st.subheader('Données de la table pour le sportif 1')
            # st.data_editor(df_filtered1)
        # with col2:
            df_filtered2 = df_pandas[df_pandas['device'] == 'device-2']
            st.subheader('Données de la table pour le sportif 2')
            # st.data_editor(df_filtered2)
        # with col3:
            df_filtered3 = df_pandas[df_pandas['device'] == 'device-3']
            st.subheader('Données de la table pour le sportif 3')
            # st.data_editor(df_filtered3)
        # with col4:
            df_filtered4 = df_pandas[df_pandas['device'] == 'device-4']
            st.subheader('Données de la table pour le sportif 4')
            # st.data_editor(df_filtered4)
        # with col5:
            df_filtered5 = df_pandas[df_pandas['device'] == 'device-5']
            st.subheader('Données de la table pour le sportif 5')
            # st.data_editor(df_filtered5)
        # break  
    sleep(2)