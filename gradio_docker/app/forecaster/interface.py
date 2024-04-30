"""
Демонстрационный интерфейс сервиса прогнозирования температуры

@author Dmitry Abramov
"""
import requests
import gradio as gr
from pandas import DataFrame
from dotenv import dotenv_values


envs = dotenv_values("/app/.env")

def forecaster(steps):
    """
    Отправка запроса API модели прогнозирования температуры
    """
    result = requests.post(f"http://{envs['FORECASTING_HOST']}:{envs['FORECASTING_PORT']}/api/temperature",
                            json={
                                  'steps': steps
                                },
                            timeout=10)
    if result.ok:
        result = result.json()
    else:
        raise gr.Error(f"При обращении к сервису прогнозирования (http://forecaster:5002/api/temperature) "
                    f"статус код: {result.status_code}")
    return DataFrame(result)


def gr_forecaster_interface():
    """
    Интерфейс сервиса прогнозирования температуры
    """
    return gr.Interface(title='Сервис прогнозирования температуры',
                        fn=forecaster,
                        inputs=[gr.Number(label='Количество недель для построения прогноза',
                                          precision=0),
                                ],
                        outputs=[gr.Dataframe(label='Прогноз погоды',
                                              headers=['Дата', 'Прогноз'])],
                        examples=[[12]])