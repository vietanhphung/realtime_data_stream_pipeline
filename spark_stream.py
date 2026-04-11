import logging
from datetime import datetime

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col

def create_keyspace(session):
    # create keyspace here

def create_table(session):
    # create tabel here

def insert_data(session):
    # insert data here

def create_spark_connection():
    try:
        #package on mvnrepository; version pattern -> scala:version
        s_conn = SparkSession.builder \
            .appName('SparkDataStreaming') \
            .config('spark.jars.packages', "com.datastax.spark:spark-cassandra-connector_2.13:3:41,"
                    "org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.1")\
            .config('spark.cassandra.connection.host', 'locahost') \
            .getOrCreate()
    except Exception as e:
        logging.error("Error creating spark connection: " + str(e))



def create_cassandra_connection():
    # create cassandra connection

if __name__ == "__main__":
    spark_connection = create_cassandra_connection()