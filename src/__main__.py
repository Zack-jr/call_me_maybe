from src.llm_sdk.llm_sdk import Small_LLM_Model
from src.models.classes import FunctionDefinitions
from src.call_me_maybe import load_functions, load_prompts, format_functions, create_prompt
import json


def main():

    

    funcs = load_prompts()
    print(create_prompt(funcs[0]))

    # THEORY/ STRUCTURE
    """
    model = Small_LLM_Model()

    code = model.encode("What is the addition between 2 and 3?")
    input = code[0].tolist()
    vocab_path = model.get_path_to_vocab_file()
    with open(vocab_path) as f:
        vocab = json.load(f)

    for _ in range(21):

        logits = model.get_logits_from_input_ids(input)
        max_log = max(logits)

        res = [key for key, value in vocab.items() if value == logits.index(max_log)]
        input.append(logits.index(max_log))
        print(res)
    """
    


if __name__ == '__main__':
    main()