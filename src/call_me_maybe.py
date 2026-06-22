from src.llm_sdk.llm_sdk import Small_LLM_Model
from src.models.classes import FunctionDefinitions
from typing import List, Dict, Any
import json

def load_functions() -> list[FunctionDefinitions]:
    """loads the json file to return a list of FunctionDefinitions"""

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
    """loads the json file to return a list of prompt strings"""

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
    """Creates a prompt containing the formatted functions definitions
    , some instructions and the initial prompt. Returns a new prompt string."""

    functions = format_functions()
    final_prompt = ("Given the user's request and the list of available functions"
    ", determine which function applies and what argument values to use. \n")

    for func in functions:
        final_prompt += func
    final_prompt += initial_prompt

    return final_prompt

def encode_function_names(functions: List[FunctionDefinitions], model: Small_LLM_Model) -> Dict[str, Any]:
    """creates a dict with the function names as keys and their corresponding
    encoded values as values"""

    encoding = {}

    for f in functions:
        code = model.encode(f.name)
        code = code[0].tolist()
        encoding.update({f.name: code})

    return encoding

def get_valid_token_ids(current_tokens: list, encoded_function_names: dict) -> list[int]:

    valid_tokens = []
    for name in encoded_function_names.keys():
        if encoded_function_names[name] == current_tokens:
            continue

        if encoded_function_names[name][:len(current_tokens)] == current_tokens:
            valid_tokens.append(encoded_function_names[name][len(current_tokens)])

    return valid_tokens
# [12 34 234]
# [12 143 513]


# when appending fixed tokens to the input_ids -> no LLM call
# otherwise -> llm call
def run():

    model = Small_LLM_Model()
    prompts = load_prompts()
    functions = load_functions()

    prefix = model.encode('{"name": "')[0].tolist()
    bridge = model.encode('", "parameters": {"')[0].tolist()
    prefix4 = model.encode(', "')[0].tolist()
    prefix6 = model.encode("}}")[0].tolist()

    function_names = encode_function_names(functions, model)


    # for every prompt
    for prompt in prompts:
        current_tokens = []
    
        # create a new prompt, append it to the input IDs
        re_prompt = create_prompt(prompt)
        input_IDs = model.encode(re_prompt)[0].tolist()
        input_IDs += prefix

        while current_tokens not in function_names.values():
            logits = model.get_logits_from_input_ids(input_IDs)
            valid_input_IDS = get_valid_token_ids(current_tokens, function_names)
            logits = [value if i in valid_input_IDS else float('-inf') for i, value in enumerate(logits)]
            max_log_index = logits.index(max(logits))
            current_tokens.append(max_log_index)
            input_IDs.append(max_log_index)
        
        current_function_name = (key for key, value in function_names.items() if value == current_tokens)
        input_IDs += bridge
    """

    {"name": "fn_add_numbers", "parameters": {"a": 2.0, "b": 3.0}}





    # encode the prompt string and make it a list
    code = model.encode(prompt)
    input = code[0].tolist()

    
   # token = [key for key, value in vocab.items() if key == "{"]
   # print(vocab[token[0]])
   # print(token)


    for _ in range(50):

        logits = model.get_logits_from_input_ids(input)

        # "mask", or "filter"
        logits = [value if i == 90 else float('-inf') for i, value in enumerate(logits)]
    
        max_log_index = logits.index(max(logits))

        res = [key for key, value in vocab.items() if value == max_log_index]
        #input.append(logits.index(max_log_index))
        print(res)

"""

