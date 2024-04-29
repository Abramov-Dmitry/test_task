"""
Сервис прогнозирования температуры на основе Prophet
Используется модель Prophet, настройка гиперпараметров которой выполнялось
с помощью Optuna, для оптимизации используется метрика rmse

@author Dmitry Abramov
"""
from fastapi.responses import JSONResponse
from fastapi import FastAPI
import mlflow

from models import Data

app = FastAPI()

mlflow.set_tracking_uri("http://mlflow:5000")
exp_id = mlflow.get_experiment_by_name('prophet').experiment_id
_id = mlflow.search_runs(exp_id).sort_values('metrics.rmse').run_id.iloc[0]
model = mlflow.prophet.load_model(f'runs:/{_id}/prophet')


@app.post("/api")
def forecasting(request: Data):
    """
    Принимает:
    {
        'steps': int - Количество недель прогнозирования
    }
    Возвращает:
    {
        'ds': List[str] - дата,
        'yhat': List[int] - прогнозируемая температура
    }
    """
    future = model.make_future_dataframe(request.steps,
                                include_history=False,
                                freq='7D')
    forecast = model.predict(future)[['ds', 'yhat']]
    forecast['ds'] = forecast.ds.astype('str')
    forecast['yhat'] = forecast['yhat'].astype('int')
    return JSONResponse(forecast.to_dict(orient='list'))
