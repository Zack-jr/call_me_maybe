from src.llm_sdk.llm_sdk import Small_LLM_Model
from src.models.classes import FunctionDefinitions, DataType
from typing import List, Dict, Any
import json
import argparse

def load_functions(path) -> list[FunctionDefinitions]:
    """loads the json file to return a list of FunctionDefinitions"""

    functions = []
    try:
        with open(path) as file:
            data = json.load(file)

            for dict in data:
                functions.append(FunctionDefinitions.model_validate(dict))
        return(functions)
    except FileNotFoundError:
        raise("File does not exist")
    

def load_prompts(path) -> list[str]:
    """loads the json file to return a list of prompt strings"""

    prompts = []
    try:
        with open(path) as file:
            data = json.load(file)
        
        for dict in data:
            prompts.append(dict["prompt"])

        return prompts

    except FileNotFoundError:
        raise("File does not exist")

def format_functions(functions: List[FunctionDefinitions]) -> str:
    """returns a list of formated string of the function_definitons"""

    prompts = []
    parts = []

    for func in functions:
        
        for name, type in func.parameters.items():
            parts.append(f"{name}: {type.type}")
        
        arguments = ", ".join(parts)
        parts.clear()
        prompts.append(f"{func.name}({arguments}) -> {func.returns.type} - description: {func.description}\n")

    return prompts

def create_prompt(initial_prompt: str, unformated_functions) -> str:
    """Creates a prompt containing the formatted functions definitions
    , some instructions and the initial prompt. Returns a new prompt string."""

    functions = format_functions(unformated_functions)
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

def get_parameter_format(function, model) -> list[Dict[int, bool]]:
    """check the function's parameters to return
    a dict with valid encoded character bridge and bool values
    that would change the format"""
    
    counter = 1
    param_count = len(function.parameters)
    dict_list = []

    for name, value in function.parameters.items():
        param_data = {}

        if value.type == "string":
            param_data.update({"encoded_bridge": model.encode(f'"{name}": "')[0].tolist()})
            param_data.update({"is_string": True})

        if value.type == "number":
            param_data.update({"encoded_bridge": model.encode(f'"{name}": ')[0].tolist()})
            param_data.update({"is_string": False})
        
        if counter == param_count:
            param_data.update({"is_last": True})
        else:
            param_data.update({"is_last": False})

        dict_list.append(param_data)
        counter += 1
        

    return dict_list

def is_valid_number_token(token_str: str) -> bool:
    try:
        float(token_str)
        return True
    except Exception:
        return False

def convert_to_float(parameters: dict):

    for key, value in parameters.items():
        try:
            if isinstance(parameters[key], int):
                parameters[key] = float(value)
        except Exception:
            continue
    return parameters

# when appending fixed tokens to the input_ids -> no LLM call
# otherwise -> llm call
def generate_json_data(model, prompts, functions):


    # reverse vocab
    with open(model.get_path_to_vocab_file()) as f:
        vocab = json.load(f)

    vocab = {value: key for key, value in vocab.items()}

    prefix = model.encode('{"name": "')[0].tolist()
    bridge = model.encode('", "parameters": {')[0].tolist()
    closer = model.encode("}}")[0].tolist()
    function_names = encode_function_names(functions, model)
    results = []

    # for every prompt
    for prompt in prompts:
        current_tokens = []
    
        # create a new prompt, append it to the input IDs
        re_prompt = create_prompt(prompt, functions)
        input_IDs = model.encode(re_prompt)[0].tolist()
        prompt_len = len(input_IDs)
        input_IDs += prefix

        while current_tokens not in function_names.values():
            logits = model.get_logits_from_input_ids(input_IDs)
            valid_input_IDS = get_valid_token_ids(current_tokens, function_names)
            logits = [value if i in valid_input_IDS else float('-inf') for i, value in enumerate(logits)]
            max_log_index = logits.index(max(logits))
            current_tokens.append(max_log_index)
            input_IDs.append(max_log_index)
        
        current_function_name = [key for key, value in function_names.items() if value == current_tokens][0]
        input_IDs += bridge
        function = [func for func in functions if func.name == current_function_name][0]
        parameters = get_parameter_format(function, model)


        # format the parameters section dynamically
        for param in parameters:
            parameter_tokens = []
            input_IDs += param["encoded_bridge"]

            # argument name building
            while True:
    
                logits = model.get_logits_from_input_ids(input_IDs)
                if not param["is_string"]:
                    logits = [value if is_valid_number_token(vocab.get(i, "")) or vocab.get(i, "") in ",}" else float ('-inf') for i, value in enumerate(logits)]

                max_log_index = logits.index(max(logits))
                parameter_tokens.append(max_log_index)
                input_IDs.append(max_log_index)

                if param["is_string"]:
                    token_str = vocab.get(max_log_index, "")
                    if '"' in token_str:
                        #double_quote_index = token_str.index['"']
                        clean_part = token_str[:(token_str.index('"'))]
                        input_IDs.pop()
                        if any(c in clean_part for c in '{},"'):
                            clean_part = ""
                        if clean_part:
                            input_IDs += model.encode(clean_part)[0].tolist()
                        input_IDs += model.encode('"')[0].tolist()
                        break
                else:
                    if vocab.get(max_log_index, "") in ",}":
                        input_IDs.pop()
                        parameter_tokens.pop()
                        break

            if param["is_last"] == False:
                input_IDs += model.encode(", ")[0].tolist()
        input_IDs += closer
        generated = input_IDs[prompt_len:]
        json_str = model.decode(generated)
        result = json.loads(json_str)
        result = {"prompt": prompt, "name": result["name"], "parameters": result["parameters"]}
        result["parameters"] = convert_to_float(result["parameters"])
        results.append(result)

    return results


def write_json_data(json_data: List[Dict[str, Any]], path):
    
    with open(path, 'w') as f:
        json.dump(json_data, f, indent=2)



def run():

    parser = argparse.ArgumentParser()

    parser.add_argument("--function_definition", default="data/input/functions_definition.json")
    parser.add_argument("--input", default="data/input/function_calling_tests.json")
    parser.add_argument("--output", default="data/output/function_calling_results.json")


    args = parser.parse_args()

    if not args.function_definition.endswith(".json") or not args.input.endswith(".json") or not args.output.endswith(".json"):
        raise ValueError("Please provide valid files and arguments.")

    model = Small_LLM_Model()
    prompts = load_prompts(args.input)
    functions = load_functions(args.function_definition)

    json_data = generate_json_data(model, prompts, functions)
    write_json_data(json_data, args.output)

