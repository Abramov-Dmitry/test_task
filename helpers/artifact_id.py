import os

import mlflow
from dotenv import dotenv_values


def get_artifacts_id(exp_name, sort_val):
    envs = dotenv_values("/app/.env")
    mlflow.set_tracking_uri(f"http://{envs['MLFLOW_HOST']}:{envs['MLFLOW_PORT']}")
    exp_id = mlflow.get_experiment_by_name(exp_name).experiment_id
    return mlflow.search_runs(exp_id).sort_values(sort_val).run_id.iloc[0]
