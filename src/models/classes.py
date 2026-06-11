from typing import Any, Dict
from pydantic import BaseModel

class DataType(BaseModel):
    type: str = ""

class FunctionDefinitions(BaseModel):
    name: str = ""
    description: str = ""
    parameters: Dict[str, DataType] = {}
    returns: DataType
