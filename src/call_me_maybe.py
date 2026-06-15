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

        return prompts

    except FileNotFoundError:
        raise("File does not exist")

def format_functions() -> str:
    """returns a list of formated string of the function_definitons"""

    prompts = []
    parts = []

    functions = load_functions()

    for func in functions:
        
        for name, type in func.parameters.items():
            parts.append(f"{name}: {type.type}")
        
        arguments = ", ".join(parts)
        parts.clear()
        prompts.append(f"{func.name}({arguments}) -> {func.returns.type}: {func.description}\n")

    return prompts

def create_prompt(initial_prompt: str) -> str:

    functions = format_functions()
    final_prompt = "placeholder: \n"

    for func in functions:
        final_prompt += func
    final_prompt += initial_prompt

    return final_prompt
    



