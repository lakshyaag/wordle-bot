from operator import add
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.graph import add_messages


class LetterAttempt(BaseModel):
    position: int = Field(
        ..., description="The position of the letter (0-indexed)", ge=0, le=4
    )
    letter: str = Field(
        ...,
        description="The letter to attempt",
        min_length=1,
        max_length=1,
        regex="^[A-Z]$",
    )

    def __repr__(self):
        return f"Letter '{self.letter}' at position {self.position}"


class LetterAttemptFeedback(BaseModel):
    attempt: LetterAttempt = Field(..., description="The letter attempt")
    status: str = Field(
        ..., description="The status of the letter", regex="^(red|yellow|green)$"
    )

    @classmethod
    def from_letter_attempt(cls, letter_attempt: LetterAttempt, status: str):
        return cls(attempt=letter_attempt, status=status)

    def __repr__(self):
        return f"{self.attempt} is {self.status}"


class Attempt(BaseModel):
    letters: Sequence[LetterAttempt] = Field(..., description="The letters to attempt")

    def __repr__(self):
        return f"Attempt: {''.join(letter.letter for letter in self.letters)}"


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    attempt_count: int
    attempt_limit: bool
    target_word: str
    attempts: Annotated[list[Attempt], add]
    feedbacks: Annotated[list[LetterAttemptFeedback], add]
