import pendulum
import glob
import io
import os
import pandas as pd
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import dag, task

@dag(
    dag_id="data_pipeline_postgres",
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    max_active_tasks=5,
    max_active_runs=1
)
def ProcessData():

    create_sensor_log_table = SQLExecuteQueryOperator(
        task_id="create_sensor_log_table",
        conn_id="postgres_default",
        sql="/sql/create_sensor_log.sql",
    )

    @task.bash(task_id="generate_data")
    def generate_data():
        return "python3 /opt/airflow/scripts/sampledata.py"

    @task(task_id="list_date")
    def list_date() -> list[str]:
        date = set()
        for p in glob.glob("/opt/airflow/scripts/data_sample/*.parquet"):
            base = os.path.basename(p)
            day = base.split(" ")[0]
            date.add(day)
        return list(date)

    @task(task_id="ingest_data")
    def ingest_data(date: str):
        print(f"Ingesting data for date: {date}")

        cols = ["department_name", "sensor_serial", "create_at", "product_name", "product_expire"]
        files = sorted(glob.glob(f"/opt/airflow/scripts/data_sample/{date}*.parquet"))
        if not files:
            return

        csv_buffer = io.StringIO()
        for fp in files:
            df = pd.read_parquet(fp, columns=cols)
            if df.empty:
                continue
            df.to_csv(csv_buffer, index=False, header=False)
        csv_buffer.seek(0)

        hook = PostgresHook(postgres_conn_id="postgres_default")
        with hook.get_conn() as conn, conn.cursor() as cur:
            cur.copy_expert(
                f"""
                COPY sensor_log ({",".join(cols)})
                FROM STDIN WITH (FORMAT CSV, DELIMITER ',')
                """,
                csv_buffer,
            )
            conn.commit()

    @task.bash(task_id="cleanup_data_sample")
    def cleanup_data_sample():
        return f"rm -rf /opt/airflow/scripts/data_sample"

    dates = list_date()
    ingested = ingest_data.expand(date=dates)

    create_sensor_log_table >> generate_data() >> dates >> ingested >> cleanup_data_sample()

dag = ProcessData()
