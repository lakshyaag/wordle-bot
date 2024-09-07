# Wordle Bot

## Overview

The Wordle Bot is a Python-based application designed to simulate playing a Wordle-like game.

## Key Components

### Modules

This package contains the core logic for the Wordle Bot. It includes modules for managing game state and interacting with the language model.

- **state.py**: Manage agent state
- **agent.py**: Contains the graph logic
- **nodes.py**: Defines the nodes for the graph
- **guess.py**: Main script for running the Wordle Bot

### Environment and Dependencies

The project uses Poetry for dependency management. Ensure you have Python 3.10 or higher installed, and use Poetry to install dependencies:

```bash
poetry install
```

### Running the Bot

To run the Wordle Bot on a single word, use the following command:

```bash
wordle_bot guess <TARGET_WORD> [--no-attempt-limit]
```

To run the Wordle Bot on a file containing multiple words, use the following command:

```bash
wordle_bot test <FILE_PATH> [--no-attempt-limit]
```

This will start the application and allow you to interact with the Wordle Bot through the command line.

## Contribution

Contributions to the Wordle Bot are welcome. Please follow the standard GitHub workflow for submitting pull requests and issues.

## License

The Wordle Bot is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions or issues, please contact the author:

- Lakshya Agarwal: <lakshya.agarwal@mail.mcgill.ca>
