from pydantic import BaseModel
from enum import Enum

class Item(BaseModel):
    key: str
    value: str

class OperationType(str, Enum):
    delete = 'delete'
    put = 'put'

class ItemBatch(Item):
    type: OperationType = OperationType.put

class User(BaseModel):
    api_key: str
