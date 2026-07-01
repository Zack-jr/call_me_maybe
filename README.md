*This project has been created as part of the 42 curriculum by <zalabib->*

# Call_Me_Maybe

## Description


    In this project, I am creating a function calling tool that translates natural language
prompts into structured function calls. 
    My program reads from JSON input files, one containing prompts, the other one containing
    the stucture of the available functions and outputs a set of JSON data with the initial prompt,
    arguments ; anything requirement that composes a valid function.

    I use the LLM provided by the subject to decode the inputs, get the logits (statistics) and build the
    JSON structure that is demanded.

    The output will be created at the specified path, or in data/output/ by default.
    

## Instructions

    To run this program, you should provide two JSON files:
        - one containing the prompts (human language)
        - the other one with the structure of functions
    
    The output will be created at the specified path.



### Installation

Python 3.10+

Create a python virtual environment and install the dependencies inside
with:
```bash
make install
```
Do not forget to access the environment with:
```bash
source ~/goinfre/.venv/bin/activate
```
Then run:
```bash
    uv sync --active --cache-dir ~/goinfre/call_me_maybe_cache
```
to install the project cache and dependencies.


### Example usage

```bash
uv run python -m src [--functions_definition <function_definition_file>] [--input <input_file>] [--
output <output_file>]
```

### Available Makefile targets

- `make install` — create venv
- `make run` — run the program with provided files
- `make debug` — run with Python debugger
- `make clean` — remove caches and temporary files
- `make lint` — check code style with flake8 and types with mypy

## Algorithm and Implementation Strategy


    For this project, I first had to go through a lot of theory. Understanding how a LLM model functions
    was a bit tricky at first. I decided to go through the LLM class provided in the subject, and I tried out multiple
    methods that were provided in order to understand the data generation pipeline.

    In my call_me_maybe.py, i am creating many helpers to facilitate context building and constrained decoding.
    The main logic appears in my main loop inside generate_json_data(). The main idea is to keep reprompting the LLM
    with as much context as possible for a model of this size, recieve the logits to then manipulate them using constrained decoding.
    Using that logic, i can ensure my program generates a valid string that contains only the needed characters for the json format.
    The key concept is to seperate "fixed" parts of the ouput's structure, to only prompt the llm when the key word is dynamic.

    I make sure to keep track of the input_IDs generated so far, so that they can be decoded later on, then dumped using json.dump() inside
    the json output file.


## Design decisions

    I used Pydantic' BaseModel (as required in the subject) to ensure a valid structure for the functions that we are passing
    to the program via the JSON file.

    I decided to function with "variable" and "fixed" parts to build my json structure.
    It allows me to prompt the LLM in scenarios where i really need it.  I keep the prompts for the
    variable parts, such as function names, and parameter values.

    I still make sure to give the full context at every iteration, so the JSON keeps on building.

## Performance Analysis

    This program provides a pretty accurate output, even when prompted vague inputs, or incoherent function structures.
    The program usually takes up to two minutes to generate the output, depending on the machines, and the number of prompts as well.

    It easily achieves an accuracy of 90+ %.


## Challenges faced

    The main challenge for this assignment was the theory behind LLMs and how to manage them properly. It wasn't an easy or motivating task at
    the beggining, but it became manageable after some time.

    The other difficult thing was trying to understand "what's a token" within a string of characters. That whole token concept made
    the constrained decoding more challenging.

## Testing strategy

    I first debugged a lot with print statements inside my loops in order to spot different kind of issues.
    For the tests, i tweaked the input files to challenge my program with different kinds of prompts and function structures.
    I also checked for missing files.
    Surprisingly, the output was very accurate quite fast.

## Resources

### Documentation
    Here is the youtube link of a video that helped me understand the concept of LLMs: https://www.youtube.com/watch?v=LPZh9BOjkQs .

### AI Usage
AI was used during this project as a learning aid for:

- explaining new concepts
- debugging complex loops
- suggesting new tools and teaching me about new tools
- code review and identifying bugs

I used Claude AI's project feature during this project. Here's the content
of the "instructions" section.

"I am a student at 42 School.
The purpose of this project is educational: I must understand concepts deeply and learn how to solve problems independently.

Your role is to act as a strict technical mentor following the 42 pedagogy.

Guidelines:

- Do not give me direct solutions or complete code.
- Prefer questions, hints, step-by-step reasoning, and guided decomposition.
- If code is absolutely necessary, only provide minimal pseudocode or isolated examples unrelated to the final solution.
- Help me understand why something works, not only how.
- Encourage debugging methodology instead of fixing problems for me directly.
- When I ask about an algorithm or implementation, first ask me about my current understanding or approach before guiding me further.
- Push me to explain my reasoning, edge cases, data structures, complexity choices, and tradeoffs.
- If my approach is weak or incorrect, do not immediately correct it. Instead, guide me toward discovering the issue myself.
- Frequently ask checkpoint questions to ensure I understand key concepts before continuing.
- Break difficult problems into smaller conceptual steps without solving them entirely.
- Prioritize learning problem-solving patterns over completing the assignment quickly.
- Assume I may be missing foundational concepts and help me identify them.
- Be strict about clean thinking, project structure, debugging discipline, and algorithmic rigor.
- Do not optimize for speed; optimize for learning and autonomy.
- Avoid giving “copy-pasteable” answers.
- Encourage me to test hypotheses, reason about failures, and verify assumptions.
- When relevant, remind me of constraints common in 42 projects: memory management, norm compliance, edge cases, undefined behavior, leaks, complexity, and maintainability.

Your goal is to help me become capable of solving similar problems independently in the future."


All code was written and validated by me. AI was used as a discussion partner rather 
than a code generator.
As the prompt just above suggests, I chose to use AI,  in a way that is compatible with 42's pedagogy,
without leaving the peer to peer aspect aside. I now feel like this project taught me a lot, especially
with workflow.