
import argparse
import sys

from wordle.wordProcessing.wordle import Wordle


def main():
    parser = argparse.ArgumentParser(description="Start Wordle")
    parser.add_argument("-C", "--cheat", action="store_true", help="Add this argument to get the answer first time")

    options = parser.parse_args(sys.argv[1:])

    wordle = Wordle()
    wordle.start(cheat=options.cheat)


if __name__ == "__main__":
    main()
