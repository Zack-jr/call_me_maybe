from typing import Dict
from pydantic import BaseModel


class DataType(BaseModel):
    """Class for datatype validation"""
    type: str = ""


class FunctionDefinitions(BaseModel):
    """class defining the structure of a function"""
    name: str = ""
    description: str = ""
    parameters: Dict[str, DataType] = {}
    returns: DataType
