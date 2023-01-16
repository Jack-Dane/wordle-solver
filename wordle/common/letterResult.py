
from enum import Enum
from dataclasses import dataclass


@dataclass
class LetterResult:
    letter: str
    result: "LetterValue"
    index: int


class LetterValue(Enum):
    CORRECT = "correct"
    PRESENT = "present"
    ABSENT = "absent"

    @staticmethod
    def fromString(value):
        if value == "correct":
            return LetterValue.CORRECT
        if value == "present":
            return LetterValue.PRESENT
        if value == "absent":
            return LetterValue.ABSENT
        raise NotImplementedError(f"Value: {value} not found in LetterValue")
