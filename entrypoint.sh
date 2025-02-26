#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

source /home/shldev/.venv/bin/activate

streamlit run main.py &

airflow db migrate

airflow users create \
    --username admin \
    --password admin \
    --role Admin \
    --firstname Admin \
    --lastname User \
    --email admin@example.com

airflow webserver --port 8080 &

airflow scheduler

