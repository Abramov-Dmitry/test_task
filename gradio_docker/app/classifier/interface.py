"""
Демонстрационный интерфейс сервиса определения инфаркта

@author Dmitry Abramov
"""
import requests
import gradio as gr
from dotenv import dotenv_values

envs = dotenv_values("/app/.env")


def classifier(age, sex, trestbps, chol, fbs, thalach, exang):
    """
    Отправка запроса API модели определения сердечных рисков
    """
    result = requests.post(f"http://{envs['CLASSIFIER_HOST']}:{envs['CLASSIFIER_PORT']}/api/heart-risk",
                            json={
                                  'age': age,
                                  'sex': sex,
                                  'trestbps': trestbps, 
                                  'chol': chol, 
                                  'fbs': fbs,
                                  'thalach': thalach, 
                                  'exang': exang
                                },
                            timeout=10)
    if result.ok:
        result = result.json()
    else:
        raise gr.Error(f"При обрещении к сервису классификации (http://classifier:5001/api/heart-risk) "
                    f"статус код: {result.status_code}")
    return result['heart_risk']


def gr_classifier_interface():
    """
    Интерфейс сервиса определения рисков сердечного приступа
    """
    return gr.Interface(title='Определение рисков приступов',
                        fn=classifier,
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
                                ],
                        outputs=[gr.Number(label='Вероятность сердечного приступа')],
                        examples=[[42, 1, 120, 231, 14, 166, 0]])