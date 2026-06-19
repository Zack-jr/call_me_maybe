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

def encode_function_names(functions: List[FunctionDefinitions]) -> Dict[str, Any]:
    """creates a dict with the function names as keys and their corresponding
    encoded values as values"""

    encoding = {}
    model = Small_LLM_Model()

    for f in functions:
        code = model.encode(f.name)
        code = code[0].tolist()
        encoding.update({f.name: code})

    return encoding

def get_valid_token_ids(current_tokens: list) -> list[int]:
     
    functions = load_functions()
    encoded_function_names = encode_function_names(functions)

    
    tokens = []



def run():

    model = Small_LLM_Model()
    prompts = load_prompts()

    prefix1 = model.encode('{"name": "')[0].tolist()
    prefix3 = model.encode('": ')[0].tolist()
    prefix4 = model.encode(', "')[0].tolist()
    prefix6 = model.encode("}}")[0].tolist()

    # get path for vocab file (str: ID)
    vocab_path = model.get_path_to_vocab_file()
    with open(vocab_path) as f:
        vocab = json.load(f)

    for prompt in prompts:
        re_prompt = create_prompt(prompt)
        input_IDs = model.encode(re_prompt)[0].tolist()
        input_IDs += prefix1

        logits = model.get_logits_from_input_ids(input_IDs)

        valid_input_IDS = get_valid_token_ids()




    """

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



