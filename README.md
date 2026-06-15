TEMPORARY NOTES:



UNDERSTANDING THE PROJECT

    SETUP-
    - QWEN IS DOWNLOADED AND CACHED IN GOINFRE AFTER CALLING THE PLATFORM (huggingface)
    - VENV IS STILL IN THE SAME DIRECTORY


    ACTUAL TASK:
        - ENCODING MY FUNCTION DEFINITIONS SO WE CAN VERIFY THE NAMES OF THE FUNCTION
        DURING JSON BUILDING
        - CRAFT A STRING THAT CONTAINS THE ENCODED FUNCTION NAMES AS WELL AS THE 
        INITIAL PROMPT



UNDERSTANDING THE LLM:


hey_how_arey4ou

The LLM analyzes a prompt, but instead of responding with text or concrete content, it only speaks in logits.
The llm doesnt compute results, it only gives predictions on the next tokens.

Building a json with the function and parameters would then allow me to compute.



DEFINITIONS:

TENSOR = A TENSOR IS A MULTIDIMENSIONAL ARRAY THAT CAN BE STORED IN DIFFERENT
PLACES IN MEMORY SUCH AS CPU, GPU, RAM...ETC/ IT NEEDS TO BE CONVERTED IN ORDER TO BE
READ BY PYTHON

LOGITS = PROBABILITY RATE GIVEN TO EACH TOKEN




LLM PIPELINE:
    - INITIAL PROMPT
        - Build a string combining the function definitions and the user prompt
    - Prompt Tokenization
        - encode the string into Token IDs
            encode()
    - first llm call
        get_logits_from_input_id()
        set invalid tokens to -inf