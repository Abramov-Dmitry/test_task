"""
Сервис определения рисков сердечного приступа

@author Dmitry Abramov
"""
import json

from fastapi import FastAPI
import mlflow
from fastapi.responses import JSONResponse

from models import Data


KEYS_ORDER = ['age', 'sex', 'trestbps', 'chol', 'fbs', 'thalach', 'exang']

app = FastAPI()

mlflow.set_tracking_uri("http://mlflow:5000")
exp_id = mlflow.get_experiment_by_name('rf_model').experiment_id
_id = mlflow.search_runs(exp_id).sort_values('metrics.accuracy').run_id.iloc[0]
model = mlflow.sklearn.load_model(f'runs:/{_id}/sklearn')

@app.post("/api")
def disease_classifier(request: Data):
    """
    Принимает:
    {
        'age': int - Возвраст наблюдаемого,
        'sex': int - Пол, 1 мужской, 0 женский,
        'trestbps': int - Артериальное давление в покое, 
        'chol': int - Холестерин, 
        'fbs': int - Количество сахара в крови,
        'thalach': int - Максимальное зафиксированное ЧДД, 
        'exang': int - Боль в груди после физическое нагрузки, 1 да, 0 нет,
    }

    Возвращает:
        json({
            'heart_risk': float - вероятность сердечного приступа,
            }
        )
    """
    request_data = json.loads(request.model_dump_json())
    print(request_data)
    data = [[request_data.get(col, 0) for col in KEYS_ORDER]]
    prob = model.predict_proba(data)

    return JSONResponse({'heart_risk': prob[0][1]})

