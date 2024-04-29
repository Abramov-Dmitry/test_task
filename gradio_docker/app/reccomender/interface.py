"""
Демонстрационный интерфейс общего сервиса

@author Dmitry Abramov
"""
import requests
import gradio as gr
from pandas import DataFrame


def recommendations(age, sex, trestbps, chol, fbs, thalach, exang, steps):
    """
    Отправка запроса основному сервису
    """
    result = requests.post('http://generation:5003/api',
                            json={
                                  'age': age,
                                  'sex': sex,
                                  'trestbps': trestbps, 
                                  'chol': chol, 
                                  'fbs': fbs,
                                  'thalach': thalach, 
                                  'exang': exang,
                                  'steps': steps
                                },
                            timeout=10)
    if result.ok:
        result = result.json()
    else:
        raise gr.Error(f"При обращении к общему сервису (http://generation:5003/api)"
                    f"статус код: {result.status_code}")
    return result['heart_risk'], DataFrame(result['temp_frst']), result['chat_recommendation']


def gr_rec_interface():
    """
    Демонстрационный интерфейс core сервиса
    """
    return gr.Interface(fn=recommendations,
                        inputs=[gr.Number(label='Возраст', precision=0),
                                gr.Radio([1, 0], value=1, label='Мужской пол'),
                                gr.Number(label='Артериальное давление в покое',
                                          precision=0),
                                gr.Number(label='Холестерин', precision=0),
                                gr.Number(label='Количество сахара в крови',
                                          precision=0),
                                gr.Number(label='Максимальное зафиксированное значение пульса',
                                          precision=0),
                                gr.Radio([0, 1], value=0, label='Наличие боли после физической нагрузки'),
                                gr.Number(label='Количество недель для построения прогноза',
                                          precision=0),
                                ],
                        outputs=[gr.Number(label='Вероятность сердечного приступа'), 
                                 gr.Dataframe(headers=['Дата', 'Прогноз'],
                                              label='Прогноз температуры'), 
                                 gr.Text(label='Рекомендация GigaChat')],
                        examples=[[42, 1, 120, 231, 14, 166, 0, 12]])