from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import GigaChat
from gigachat import exceptions
import mlflow

from helpers.artifact_id import get_artifacts_id


_id = get_artifacts_id('gigachat', 'start_time')


class GigaChatService:
    artifacts = mlflow.artifacts.load_dict(f'runs:/{_id}/data.json')

    def get_chat(self):
        return GigaChat(credentials=self.artifacts['token'],
                        verify_ssl_certs=False,
                        temperature=0.6,
                        model='GigaChat')

    def get_message(self, data):
        return [
            SystemMessage(content=self.artifacts['system_promt']),
            HumanMessage(content=self.artifacts['human_promt'].format(len(data['forecast']['ds']),
                                                                      data['forecast']['yhat'],
                                                                      data['heart_risk']))
        ]

    def get_chat_recommendation(self, data):
        chat = self.get_chat()
        try:
            recommendation = chat(self.get_message(data)).content
        except exceptions.ResponseError:
            return  {'Error': 'Ошибка с токеном доступа при обращении к GigaChat',
                     **data}

        return {'chat_recommendation': recommendation,
                **data}
