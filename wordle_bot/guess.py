import typer
import logging

import typer.cli
from .state import AgentState
from .agent import graph
from langchain_core.messages import SystemMessage, HumanMessage
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

A status of:
- `red` means that the letter does not appear in the word in any position - you should not use this letter in any future guesses
- `yellow` means that the letter appears in the word, but not in that position - you should try this letter in a different position
- `green` means that the letter appears in the word in that position - you should keep this letter in that position in future guesses."""
    )
)


@app.command()
def guess(target_word: str, attempt_limit: bool = True, recursion_limit: int = 50):
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
        "messages": [SYSTEM_PROMPT, HumanMessage("Begin by guessing a 5-letter word.")],
        "attempt_count": 0,
        "attempt_limit": attempt_limit,
        "target_word": target_word,
        "attempts": [],
        "feedbacks": [],
    }

    logger.info("Starting Wordle game with initial state: %s", initial_state)

    result = graph.invoke(initial_state, config)

    logger.info("Game result: %s", result)
