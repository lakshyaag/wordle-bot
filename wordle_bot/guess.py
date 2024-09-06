import logging
from .state import AgentState
from .agent import graph
from langchain_core.messages import SystemMessage, HumanMessage
from textwrap import dedent
from dotenv import load_dotenv, find_dotenv
import uuid

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

SYSTEM_PROMPT = SystemMessage(
    dedent(
        """You are playing Wordle. You have 6 attempts to guess a 5-letter English word. 
After each guess, you will receive feedback on each letter in your guess, which you can use to refine your next guess.

A status of:
- `red` means that the letter does not appear in the word in any position - you should not use this letter in any future guesses
- `yellow` means that the letter appears in the word, but not in that position - you should try this letter in a different position
- `green` means that the letter appears in the word in that position - you should keep this letter in that position in future guesses."""
    )
)


def main():
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    initial_state: AgentState = {
        "messages": [SYSTEM_PROMPT, HumanMessage("Begin by guessing a 5-letter word.")],
        "attempt_count": 0,
        "target_word": "WIDEN",
        "attempts": [],
        "feedbacks": [],
        "solved": False,
    }

    logger.info("Starting Wordle game with initial state: %s", initial_state)

    result = graph.invoke(initial_state, config)

    logger.info("Game result: %s", result)
