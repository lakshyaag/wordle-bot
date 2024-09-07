import typer
import logging

import typer.cli
from .state import AgentState
from .agent import graph
from langchain_core.messages import SystemMessage
from textwrap import dedent
from dotenv import load_dotenv, find_dotenv
import uuid

app = typer.Typer()

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

SYSTEM_PROMPT = SystemMessage(
    dedent(
        """You are playing Wordle. You have a limited number of attempts to guess a 5-letter English word. 
After each guess, you will receive feedback on each letter in your guess, which you can use to refine your next guess. 

This feedback will be in a comma-separated format: position,letter,status.

A status of:
- `red` means that the letter does not appear in the word in any position - this letter should not be used in any future guesses
- `yellow` means that the letter appears in the word, but not in that position - this letter should be tried in a different position in future guesses
- `green` means that the letter appears in the word in that position - this letter is correct and should not be moved in future guesses
"""
    )
)


@app.command()
def guess(
    target_word: str, attempt_limit: bool = True, recursion_limit: int = 50
) -> AgentState:
    """
    Play a game of Wordle by attempting to guess a target word.

    This function initiates a Wordle game where the player has a limited number of attempts
    to guess a 5-letter target word. After each guess, feedback is provided on the accuracy
    of each letter in the guess, which can be used to refine subsequent guesses.

    Args:
        target_word (str): The 5-letter word that the player is attempting to guess.
        attempt_limit (bool, optional): Whether to limit the number of attempts. Defaults to True.
        recursion_limit (int, optional): The maximum recursion depth for the guessing algorithm. Defaults to 50.

    Returns:
        result: The final state of the game
    """
    if len(target_word) != 5:
        raise typer.BadParameter(
            "The target word must be 5 letters long.", param_hint="target_word"
        )

    config = {
        "recursion_limit": recursion_limit,
        "configurable": {
            "thread_id": str(uuid.uuid4()),
        },
    }

    initial_state: AgentState = {
        "messages": [SYSTEM_PROMPT],
        "attempt_count": 0,
        "attempt_limit": attempt_limit,
        "target_word": target_word,
        "attempts": [],
        "feedbacks": [],
    }

    logger.info("Starting Wordle game with initial state: %s", initial_state)

    result = graph.invoke(initial_state, config)

    logger.info("Game result: %s", result)

    return result


@app.command()
def test(
    file_path: str, attempt_limit: bool = True, recursion_limit: int = 50
) -> dict[str, AgentState]:
    """
    Test the Wordle guessing algorithm with a list of target words from a file.

    This function reads a file containing a list of 5-letter target words, one per line,
    and attempts to guess each word using the Wordle guessing algorithm. The results of
    each attempt are logged and returned in a dictionary.

    Args:
        file_path (str): The path to the file containing the target words.
        attempt_limit (bool, optional): Whether to limit the number of attempts. Defaults to True.
        recursion_limit (int, optional): The maximum recursion depth for the guessing algorithm. Defaults to 50.

    Returns:
        dict: A dictionary where the keys are the target words and the values are the final game states.
    """

    with open(file_path, "r") as f:
        targets = f.readlines()

    results = {}

    for target in targets:
        logger.info(f'Guessing target word: "{target.strip()}"')
        results[target.strip()] = guess(target.strip(), attempt_limit, recursion_limit)

    return results
