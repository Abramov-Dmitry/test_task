import requests
from dotenv import dotenv_values


class ErrorMessages:
    def get_200_message(self, request):
        if request.ok:
            return {'data': request.json()} | {'status_code': 200}
        else:
            return {'message': f"""При обращении к сервису прогнозирования 
                    температуры возвращен статус код: {request.status_code}""",
                    'status_code': request.status_code}


class ForecasterClient:
    envs = dotenv_values("/app/.env")
    error_messages = ErrorMessages()
    
    def get_host(self):
        return f"http://{self.envs['FORECASTING_HOST']}:{self.envs['FORECASTING_PORT']}/api"

    def temperature(self, steps):
        forecast = requests.post(f'{self.get_host()}/temperature',
                                 json={"steps": steps},
                                 timeout=10)
        return self.error_messages.get_200_message(forecast)
