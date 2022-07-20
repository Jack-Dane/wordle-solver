
import argparse
import sys

from wordle.wordProcessing.wordle import Wordle
from wordle.common.guessAlogrithms import GuessAlgorithm


def main():
    parser = argparse.ArgumentParser(description="Wordle")
    parser.add_argument(
        "-C", "--cheat",
        action="store_true",
        help="Add this argument to get the answer first time"
    )
    parser.add_argument(
        "-FG", "--firstGuess",
        help="Use this value as the first guess"
    )
    parser.add_argument(
        "-GT", "--guessingType",
        help="The guessing type to use",
        choices=[
            GuessAlgorithm.GENERIC_GUESS_ALGORITHM, GuessAlgorithm.ELIMINATION_2_GUESS_ALGORITHM,
            GuessAlgorithm.ELIMINATION_3_GUESS_ALGORITHM
        ],
        default=GuessAlgorithm.GENERIC_GUESS_ALGORITHM
    )
    parser.add_argument(
        "-LR", "--logResult", action="store_true",
        help="Log the results to the database"
    )
    parser.add_argument(
        "--headless", action="store_true",
        help="Run without visible Chrome window"
    )
    parser.add_argument(
        "-CDP", "--chromeDriverPath",
        help="Set a custom driver"
    )

    options = parser.parse_args(sys.argv[1:])

    wordle = Wordle(options.guessingType, options.logResult, firstGuess=options.firstGuess)
    wordle.start(options.headless, cheat=options.cheat, chromeDriverPath=options.chromeDriverPath)


if __name__ == "__main__":
    main()
