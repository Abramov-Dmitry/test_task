import os
from pathlib import Path
import pickle

import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

os.chdir('artifacts')

for model in os.listdir():
    exp_id = mlflow.create_experiment(Path(model).stem)
    mlflow.set_experiment(exp_id)

    sk_model = pickle(open(model, 'rb'))
    with mlflow.start_run():
        mlflow.sklearn.log_model(sk_model=sk_model, artifact_path="model")

print("Модели загружены в MLFlow")