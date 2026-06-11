from typing import Dict
import json
from src.models.classes import FunctionDefinitions

def load_functions() -> list[FunctionDefinitions]:

    functions = []
    try:
        with open('data/input/functions_definition.json') as file:
            data = json.load(file)

            for dict in data:
                functions.append(FunctionDefinitions.model_validate(dict))
        return(functions)
    except FileNotFoundError:
        raise("File does not exist")
    

def load_prompts() -> list[str]:
    
    prompts = []
    try:
        with open('data/input/function_calling_tests.json') as file:
            data = json.load(file)
        
        for dict in data:
            prompts.append(dict["prompt"])

        print(prompts)
        return prompts

    except FileNotFoundError:
        raise("File does not exist")