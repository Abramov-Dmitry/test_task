"""
Модель данных сервиса прогнозирования
"""
from pydantic import BaseModel


class Data(BaseModel):
    age: int
    sex: int
    trestbps: int | None = 0
    chol: int | None = 0
    fbs: int | None = 0
    thalach: int | None = 0
    exang: int | None = 0
    steps: int = 12