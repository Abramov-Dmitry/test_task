"""
Модель данных сервиса прогнозирования
"""
from pydantic import BaseModel


class Data(BaseModel):
    steps: int | None = 12
