*This project has been created as part of the 42 curriculum by <zalabib->*

# Call_Me_Maybe

## Description


## Instructions

### Installation

Python 3.10+

Create a python virtual environment and install the dependencies inside
with:
```bash
make install
```
Do not forget to access the environment with:
```bash
source env/bin/activate
```

### Running

```bash
python3 fly-in.py <path_to_map.txt>
```

Example:
```bash
python3 fly-in.py maps/easy/01_linear_path.txt
```

### Available Makefile targets

- `make install` — install dependencies in a venv
- `make run` — run on a sample map
- `make debug` — run with Python debugger
- `make clean` — remove caches and temporary files
- `make lint` — check code style with flake8 and types with mypy
- `make invalid` — runs a set of invalid maps for parsing check (if provided)
- `make easy` / `make medium` / `make hard` / `make challenger` — run all maps of a difficulty level

## Algorithm and Implementation Strategy



## Resources

### Documentation
- [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Python heapq module](https://docs.python.org/3/library/heapq.html)
- [Explanations on Graph theory](https://www.youtube.com/watch?v=4jyESQDrpls)

### AI Usage
AI was used during this project as a learning aid for:
- Discussing algorithmic concepts (Dijkstra, path penalization, multi-agent coordination)
- Debugging complex turn-based simulation logic
- Suggesting Python idioms and OOP design patterns
- Code review and identifying bugs

I used Claude AI's project feature during this project. Here's the content
of the "instructions" section.

"The project i am working on is there for educational purposes, I must work on this assignment while learning new things. I will need guidance on most algorithmic notions and on ways to approach problems I haven't seen before. You should not give me direct answers but rather lead me to them.  I should ideally figure things out by myself, but you should be able to help me build a concrete structure while still helping me follow the 42 school pedagogy. You should ask me some questions often enough to make sure I don't skip key notions. You should not give me code, or if you do, only in the form of pseudocode. You should be as strict as possible in order for me to learn."


All code was written and validated by me. AI was used as a discussion partner rather 
than a code generator.
I first discussed the Fly-in with peers, trying to absorb different perspectives on a subject
that wasn't approached in 42 before the change of common-core program.
As the prompt just above suggests, I chose to use AI,  in a way that is compatible with 42's pedagogy,
without leaving the peer to peer aspect aside. I now feel like this project taught me a lot, especially
with workflow.