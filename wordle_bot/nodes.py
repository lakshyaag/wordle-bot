from textwrap import dedent

from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
import logging
from .state import AgentState, Attempt, LetterAttemptFeedback

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_guess(state: AgentState) -> AgentState:
    messages = state["messages"]
    attempt_count = state["attempt_count"]

    messages += [HumanMessage(f"Attempt {attempt_count} | Guess a 5-letter word.")]

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.8,
    ).with_structured_output(Attempt)

    # Print the messages to the log
    logger.debug("-" * 80)
    logger.debug("Messages to LLM:")
    for message in messages:
        logger.debug(f"{message}")
    logger.debug("-" * 80)

    response = llm.invoke(messages)

    attempt = "".join(letter.letter for letter in response.letters)
    ai_message = AIMessage(
        dedent(f"""<attempt key={attempt_count}>{attempt}</attempt>""")
    )

    logger.info(f"Attempt {attempt_count}: {attempt}")

    return {
        "messages": ai_message,
        "attempts": [response],
        "attempt_count": attempt_count + 1,
    }


def check_attempt(state: AgentState) -> AgentState:
    target_word = state["target_word"]
    attempt = state["attempts"][-1]

    feedback = [
        LetterAttemptFeedback.from_letter_attempt(
            letter_attempt=letter,
            status=(
                "green"
                if letter.letter == target_word[letter.position]
                else "yellow"
                if letter.letter in target_word
                else "red"
            ),
        )
        for letter in attempt.letters
    ]

    feedback_message = "\n".join(
        f"{i},{fb.attempt.letter},{fb.status}" for i, fb in enumerate(feedback)
    )

    ai_message = AIMessage(
        dedent(
            f"""<feedback key="{state["attempt_count"] - 1}">
{feedback_message}
</feedback>"""
        )
    )

    return {
        "messages": ai_message,
        "feedbacks": [feedback],
    }


def next_guess(state: AgentState) -> AgentState:
    feedbacks = state["feedbacks"]
    attempt_count = state["attempt_count"]

    if state["attempt_limit"]:
        # If the attempt limit is enabled, check if the user has run out of attempts
        if attempt_count > 6:
            logger.info("You have run out of attempts.")
            return "timeout"

    feedback = feedbacks[-1]

    if all([fb.status == "green" for fb in feedback]):
        logger.info(
            f'Word "{state["target_word"]}" guessed in {attempt_count} attempts!'
        )
        return "success"

    return "continue"
