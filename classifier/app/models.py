"""
Модель данных сервиса определения рисков инфаркта
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