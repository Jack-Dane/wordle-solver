
from unittest import TestCase
from unittest.mock import patch

from wordle.common.letterResult import LetterResult, LetterValue
from wordle.output import ConsolePrinter


class Test_ConsolePrinter_printResults(TestCase):

    @patch("wordle.output.ConsolePrinter.print")
    def test_ok(self, print_):
        results = [
            LetterResult("a", LetterValue.CORRECT, 4),
            LetterResult("b", LetterValue.CORRECT, 1),
            LetterResult("c", LetterValue.ABSENT, 0),
            LetterResult("d", LetterValue.PRESENT, 2),
            LetterResult("e", LetterValue.ABSENT, 3),
        ]

        ConsolePrinter.printResults(results, 20)

        print_.assert_called_once_with(
            "\u001b[37mc\u001b[32mb\u001b[33md\u001b[37me\u001b[32ma\u001b[0m Words remaining 20"
        )
