# Chess Engine
A chess engine I developed from scratch that is roughly 2000 elo on chess.com.

## Architecture
This engine is broken up into 3 main parts:

Frontend in (QML/Qt Quick)
- Displays the board and pieces
- Allows the user to interact with the board
- Displays the best move and evaluation found

Engine Manager (C++)
- The bridge between the frontend and the backend search algorithms
- Converts the Javascript positions dictionary into a C++ list
- Sends the list to C++ and starts the search

Search Engine (Python or C++)
- First prototyped in Python to get the search logic functioning properly, and then ported to C++ for speed and memory efficiency.

## Files
This repo contains three folders:
    - A python chess search engine
    - A C++ chess search engine
    - A frontent that includes the engine manager as a c++ file

## Current Engine Features
- Move generation
- Legal move validation
- Board state management
- Evaluation function
- Minmax search
- Alpha-beta pruning
- Move ordering: captures, promotions, killer moves, 
- Transposition tables
- PVS
- Null move pruning
- LMR pruning
- Iterative deepening


