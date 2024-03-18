"""weather_ETL_pipeline.py: airflow_pipeline file"""

__author__ = "Aryaroop Majumder"



from datetime import datetime, timedelta
import json
import os
import numpy as np
import requests

from service.getWeather import get_weather
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.operators.http import HttpOperator
from airflow.utils.dates import days_ago
from airflow.hooks.postgres_hook import PostgresHook

def get_weather_data():
    return get_weather()


def load_data(ds, **kwargs):
    """
    Processes the json data, checks the types and enters into the
    Postgres database.
    """

    pg_hook  = PostgresHook(postgres_conn_id='weather_id')

    file_name = str(datetime.now().date()) + '.json'
    tot_name = os.path.join(os.path.dirname(__file__),'service/data', file_name)

    # open the json datafile and read it in
    with open(tot_name, 'r') as inputfile:
        doc = json.load(inputfile)

    # transform the data to the correct types and convert temp to celsius
    city        = str(doc['name'])
    country     = str(doc['sys']['country'])
    lat         = float(doc['coord']['lat'])
    lon         = float(doc['coord']['lon'])
    humid       = float(doc['main']['humidity'])
    press       = float(doc['main']['pressure'])
    min_temp    = float(doc['main']['temp_min']) - 273.15
    max_temp    = float(doc['main']['temp_max']) - 273.15
    temp        = float(doc['main']['temp']) - 273.15
    weather     = str(doc['weather'][0]['description'])
    todays_date = datetime.now().date()

    # check for nan's in the numeric values and then enter into the database
    valid_data  = True
    for valid in np.isnan([lat, lon, humid, press, min_temp, max_temp, temp]):
        if valid is False:
            valid_data = False
            break;

    row  =  (city, country, lat, lon, todays_date, humid, press, min_temp,
            max_temp, temp, weather)

    insert_cmd = """INSERT INTO dnd_weather_table 
                    (city, country, latitude, longitude,
                    todays_date, humidity, pressure, 
                    min_temp, max_temp, temp, weather)
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    if valid_data is True:
        pg_hook.run(insert_cmd, parameters=row)

default_args = {
    'owner': 'Aryaroop',
    'depends_on_past': False,
    'email': ['aryaroop_majumder@prescience.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'start_date': days_ago(0),
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    dag_id='weather_ETL_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(minutes=30)
)

task1 = PythonOperator(
    task_id='get_weather_data',
    python_callable=get_weather_data,
    provide_context=True,
    dag=dag
)

task2 = PythonOperator(
    task_id='transform_load',
    python_callable=load_data,
    provide_context=True,
    dag=dag
)

task1 >> task2  # Set task dependencies correctly

