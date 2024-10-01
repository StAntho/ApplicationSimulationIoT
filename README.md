# Simulation IoT - Spark Streaming

> Suivi des données en direct d'un capteur fictif en python

## Tech Stack

- [Pyhton](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Spark](https://spark.apache.org/)
- [Hadoop](https://hadoop.apache.org/)
- [Streamlit](https://streamlit.io/)

## Launch project app

Load docker images

```bash
  docker compose up -d
```

Get token for docker notebook

```bash
    docker exec -it pyspark-notebook jupyter server list
```

Create hadoop.env like:

```bash
    # Environment settings for Hadoop
    CORE_CONF_fs_defaultFS=
    CORE_CONF_hadoop_http_staticuser_user=
    CORE_CONF_fs_permissions_umask-mode=

    # HDFS settings
    HDFS_CONF_dfs_replication=
    HDFS_CONF_dfs_permissions_enabled=

    # YARN settings
    YARN_CONF_yarn_resourcemanager_hostname=
    YARN_CONF_yarn_resourcemanager_address=
    YARN_CONF_yarn_resourcemanager_scheduler_address=
    YARN_CONF_yarn_resourcemanager_resource_tracker_address=
    YARN_CONF_yarn_resourcemanager_webapp_address=

    # MapReduce settings
    MAPRED_CONF_mapreduce_framework_name=
    MAPRED_CONF_mapreduce_jobhistory_address=
```

Open jupyter lab server and namenode server

- [jupyter lab server](http://localhost:8888/)
- [namenode server](http://localhost:9870/)

### Execute the code in terminal lab

Install dotenv

```bash
  pip install python-dotenv
```

Launch capteur.py to make data:

```bash
    python capteur.py
```

Install Streamlit

```bash
  pip install streamlit
```

Launch app in terminal's jupyter

```bash
  streamlit run app.py
```

Open Streamlit server

- [Streamlit server](http://localhost:8501/)

## Launch project kafka

Load docker images

```bash
  docker compose up -d
```

Ouverture du bash spark-master

```bash
  docker exec -it spark-master /bin/bash
```

Ajout des bibliothèques dans le bash spark

```bash
  pip install kafka-python
  pip install pyspark
```

Execution du producer et du sparkStreaming sur des terminaux distincts dans le bash spark

```bash
  python app/data_producer.py
```

```bash
  /spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 /app/scriptStreamingMessages.py
```

Ajout des bibliothèques dans le bash streamlit

```bash
  pip install pyspark
```

Open Streamlit server

- [Streamlit server](http://localhost:8501/)
