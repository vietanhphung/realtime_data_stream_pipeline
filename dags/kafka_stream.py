from datetime import datetime
from ftplib import print_line

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from dateutil.rrule import DAILY

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
    res = res.json()
    res = res["results"][0]
    return res


def format_data(res):
    data = {}
    location = res['location']
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']["number"])} {location['street']['name']}, " + f"{location['city']}, {location['state']}, {location['country']}"
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
    data = get_data()
    formated_data = format_data(data)
    print_line(json.dumps(formated_data, indent=3))


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

stream_data()