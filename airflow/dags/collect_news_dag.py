from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

default_args = {
  'owner': 'duc',
  'depends_on_past': False,
  'start_date': datetime(2025,2,3),
  'retries': 0
}

with DAG('collect_news' , default_args= default_args, schedule= '@once') as dag :


    collect_news = BashOperator(
        task_id = "collect_news",
        bash_command = "cd web_crawler && python3 web_crawler_from_start.py",
        cwd = "/home/shldev/airflow"
    )

    end = EmptyOperator(
        task_id= 'done',
        trigger_rule= 'all_success'
    )

    collect_news  >> end
