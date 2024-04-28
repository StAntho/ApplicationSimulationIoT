# Simulation IoT - Spark Streaming

> Suivi des données en direct d'un capteur fictif en python

## Tech Stack

- [Pyhton](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Spark](https://spark.apache.org/)
- [Hadoop](https://hadoop.apache.org/)
- [Streamlit](https://streamlit.io/)

## Launch project

Load docker images

```bash
  docker compose up -d
```

Get token for docker notebook

```bash
    docker exec -it pyspark-notebook jupyter server list
```

Open jupyter lab server and namenode server

- [jupyter lab server](http://localhost:8888/)
- [namenode server](http://localhost:9870/)

## Execute the code in terminal lab

Install Streamlit

```bash
  pip install streamlit
```

Launch app

```bash
  streamlit run app.py
```

Open Streamlit server

- [Streamlit server](http://localhost:8501/)
