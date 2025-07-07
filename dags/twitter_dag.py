from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from main import fetch_data_etl


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['test@mail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='twitter_etl_to_s3_dag',
    default_args=default_args,
    description='ETL Twitter data and upload to S3',
    schedule_interval='30 12 * * 6',
    start_date=days_ago(1),
    catchup=False,
    tags=['twitter', 'etl', 's3']
) as dag:

    run_etl = PythonOperator(
        task_id='fetch_and_process_twitter_data',
        python_callable=fetch_data_etl
    )

    run_etl



