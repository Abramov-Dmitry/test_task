"""
Сервис описания результатов с помощью Gigachat, входная точка 
для сервисов определения вероятности приступа и прогнозирования температур

Токен доступа и системный промт хранятся в артефакте json

@author Dmitry Abramov
"""
import json

from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse
import httpx

import mlflow

from models import Data
from api.forecaster import ForecasterClient
from api.heart_risk import ClassifierClient
from api.giga import GigaChatService


app = FastAPI()


@app.post("/api/recommendations")
async def generating(data: Data):
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
            'forecast': [
                {
                    'ds': list[str],
                    'yhat': list[float]
                }
            ] - прогноз на steps недель,
            'chat_recommendation': str - предупреждение оснвове прогноза и вероятности приступа от LLM
            }
        )
    """
    heart_risk = ClassifierClient().heart_risk(json.loads(data.model_dump_json()))

    if heart_risk['status_code'] == 422:
        return ClassifierClient().error_messages.get_422_message()

    forecast = ForecasterClient().temperature(data.steps)

    if forecast['status_code'] != 200:
        return JSONResponse(content=forecast,
                            status_code=forecast['status_code'])

    data = {'forecast': forecast['data'], 
            'heart_risk': heart_risk['data']['heart_risk']}

    return JSONResponse(content=GigaChatService().get_chat_recommendation(data))

if __name__ == "__main__":
    uvicorn.run("service:app", host="0.0.0.0", port=5003, reload=True)
