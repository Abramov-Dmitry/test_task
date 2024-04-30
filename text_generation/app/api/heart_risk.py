import requests
from dotenv import dotenv_values


class ErrorMessages:
    def get_422_message(self):
        return {'Error': """При обращении к сервису прогнозирования 
                         сердечного приступа возникло исключение: Указаны не 
                         все необходимые поля в отправленной json"""}
    
    def get_200_message(self, request):
        if request.ok:
            return {'data': request.json()} | {'status_code': 200}
        else:
            return {'status_code': request.status_code}


class ClassifierClient:
    envs = dotenv_values("/app/.env")
    error_messages = ErrorMessages()

    def get_host(self):
        """
        Получение хоста сервиса определения рисков сердечного заболевания
        """
        return f"http://{self.envs['CLASSIFIER_HOST']}:{self.envs['CLASSIFIER_PORT']}/api"

    def heart_risk(self, data):
        request = requests.post(f'{self.get_host()}/heart-risk',
                                 json=data,
                                 timeout=10)
        return self.error_messages.get_200_message(request)
