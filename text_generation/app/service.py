"""
Сервис описания результатов с помощью Gigachat, входная точка 
для сервисов определения вероятности приступа и прогнозирования температур

Токен доступа и системный промт хранятся в артефакте json

@author Dmitry Abramov
"""
import json

from fastapi import FastAPI
import uvicorn
import requests
from fastapi.responses import JSONResponse
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import GigaChat
from gigachat import exceptions
import httpx

import mlflow

from models import Data

app = FastAPI()

mlflow.set_tracking_uri("http://mlflow:5000")
exp_id = mlflow.get_experiment_by_name('gigachat').experiment_id
_id = mlflow.search_runs(exp_id).sort_values('start_time').run_id.iloc[0]
artifacts = mlflow.artifacts.load_dict(f'runs:/{_id}/data.json')


@app.post("/api")
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
            'forecasting': [
                {
                    'ds': list[str],
                    'yhat': list[float]
                }
            ] - прогноз на steps недель,
            'recommendation': str - предупреждение оснвове прогноза и вероятности приступа от LLM
            }
        )
    """
    chat = GigaChat(credentials=artifacts['token'],
                verify_ssl_certs=False,
                temperature=0.6,
                model = 'GigaChat')
    heart_risk = requests.post('http://classifier:5001/api',
                        json=json.loads(data.model_dump_json()),
                        timeout=10)
    
    if heart_risk.status_code == 422:
        return JSONResponse(content={'Error': """При обращении к сервису прогнозирования 
                                     сердечного приступа возникло исключение: Указаны не 
                                     все необходимые поля в отправленной json"""},
                                     status_code=422)
    
    if heart_risk.ok:
        heart_risk = heart_risk.json()


    forecast = requests.post('http://forecaster:5002/api',
                            json={"steps": data.steps},
                            timeout=10)
    
    if forecast.ok:
        forecast = forecast.json()

    messages = [
        SystemMessage(content=artifacts['system_promt']),
        HumanMessage(content=f"""В течение следующих {len(forecast['ds'])} недель температура
                      будет меняться так: {forecast['yhat']}, вероятность сердечного приступа
                      у человека {heart_risk['heart_risk']}. Если у человека высокий риск 
                      сердечного приступа предупреди его о возможном недомогании. Если риск 
                      сердечного приступа низкий, скажи что погода может резко поменяться""")]
    try: 
        reccommendation = chat(messages).content
    except exceptions.ResponseError:
        JSONResponse(content={'Error': 'Ошибка с токеном доступа при обращении к GigaChat',
                              'temp_frst': forecast,
                              'heart_risk': heart_risk['heart_risk']},
                     status_code=500)

    # return JSONResponse({'chat_recommendation': 1})
    return JSONResponse({'chat_recommendation': reccommendation,
                         'temp_frst': forecast,
                         'heart_risk': heart_risk['heart_risk']})

if __name__ == "__main__":
    uvicorn.run("service:app", host="0.0.0.0", port=5003, reload=True)