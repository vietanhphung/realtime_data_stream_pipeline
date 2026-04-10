from datetime import datetime
import logging
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'connor_phung',
    'start_date': datetime(2026, 4, 6, 00,00),
}


def get_data():
    """
    get data from api
    :return: json
    """
    import requests

    res = requests.get("https://randomuser.me/api/")
    res.raise_for_status()

    payload = res.json()
    result = payload.get('results', [])

    if not result:
        logging.error("Data_stream: get data return empty results: %s", payload)
        raise ValueError("Data_stream: get data return empty results: {}".format(payload))
    return result[0]


def format_data(res):
    data = {}
    location = res['location']
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " + f"{location['city']}, {location['state']}, {location['country']}"
    data['postcode'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

def stream_data():
    import json
    from kafka import KafkaProducer
    import time


    producer = KafkaProducer(bootstrap_servers=['broker:29092'],max_block_ms=5000) #address for running in airflow container
    #producer = KafkaProducer(bootstrap_servers=['localhost:9092'], max_block_ms=5000)
    current_time = time.time()

    try:
        while time.time() <= current_time + 60: # 1 minute:

            data = get_data()
            formated_data = format_data(data)

            producer.send(topic='user_created', value=json.dumps(formated_data).encode('utf-8'))
            producer.flush()
            logging.info("Data_stream: sent message to user_created")
            time.sleep(1)

    except Exception as e:
        logging.exception("Error while streaming data: %s", e)
        raise
    finally:
        producer.close()


#dag creation
with DAG(
    'user_automation',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
) as dag:

    stream = PythonOperator(
        task_id='stream_data_from_api',
        python_callable = stream_data
    )

