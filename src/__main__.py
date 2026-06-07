from src.llm_sdk.llm_sdk import Small_LLM_Model



def main():

    model = Small_LLM_Model()

    code = model.encode("hello")
    input_ids = code[0].tolist()

    logits = model.get_logits_from_input_ids(input_ids)
    print(logits)
    vocab_path = model.get_path_to_vocab_file()
    with open(vocab_path) as f:
        for line in f:
            print(line)


if __name__ == '__main__':
    main()