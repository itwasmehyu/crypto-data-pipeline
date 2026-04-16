from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'huynguyen',
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'crypto_daily_pipeline',
    default_args=default_args,
    description='A pipeline to fetch crypto data and run dbt',
    schedule_interval='*/15 * * * *', # Chạy vào các phút: 0, 15, 30, 45 mỗi giờ
    start_date=datetime(2025, 12, 1),
    catchup=False,
) as dag:

    task_fetch_data = BashOperator(
        task_id='fetch_crypto_data',
        bash_command='python3 /opt/airflow/fetch_crypto.py'
    )

# Task 2: Chạy dbt run
    task_dbt_run = BashOperator(
        task_id='dbt_run',
        # Chúng ta gộp 3 lệnh: Khai báo PATH -> Di chuyển thư mục -> Chạy dbt
        bash_command=(
            'export PATH=$PATH:/home/airflow/.local/bin && '
            'cd /opt/airflow/my_crypto_project && '
            'dbt run --profiles-dir .'
        )
    )

    # Task 3: Chạy dbt test
    task_dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=(
            'export PATH=$PATH:/home/airflow/.local/bin && '
            'cd /opt/airflow/my_crypto_project && '
            'dbt test --profiles-dir .'
        )
    )
    task_fetch_data >> task_dbt_run >> task_dbt_test
