import random
from unittest.mock import patch
from unittest import TestCase

from wordle.wordProcessing.wordList import (
    WordList, RandomFromSample, Elimination2GuessAlgorithm, Elimination3GuessAlgorithm
)
from wordle.common.guessAlogrithms import GuessAlgorithm

MODULE_PATH = "wordle.wordProcessing.wordList."


class Test_WordList_getWordList(TestCase):

    def test_GENERIC_GUESS_ALGORITHM(self):
        wordAlgorithm = WordList.getWordlist(
            GuessAlgorithm.GENERIC_GUESS_ALGORITHM
        )

        self.assertIsInstance(wordAlgorithm, RandomFromSample)

    def test_ELIMINATION_2_GUESS_ALGORITHM(self):
        wordAlgorithm = WordList.getWordlist(
            GuessAlgorithm.ELIMINATION_2_GUESS_ALGORITHM
        )

        self.assertIsInstance(wordAlgorithm, Elimination2GuessAlgorithm)

    def test_ELIMINATION_3_GUESS_ALGORITHM(self):
        wordAlgorithm = WordList.getWordlist(
            GuessAlgorithm.ELIMINATION_3_GUESS_ALGORITHM
        )

        self.assertIsInstance(wordAlgorithm, Elimination3GuessAlgorithm)

    def test_exception(self):
        with self.assertRaises(NotImplementedError):
            WordList.getWordlist("Not Implemented")


@patch.object(WordList, "removeWord")
class Test_EliminationCommon_removeWord(TestCase):

    def setUp(self):
        self.eliminationGuessAlgorithm = Elimination2GuessAlgorithm()

    def test_first_guess(self, WordList_removeWord):
        self.eliminationGuessAlgorithm.guessCount = 1

        self.eliminationGuessAlgorithm.removeWord("guess")

        WordList_removeWord.assert_called_once_with("guess")
        self.assertIn("guess", self.eliminationGuessAlgorithm.eliminatedWords)

    def test_less_than_elimination(self, WordList_removeWord):
        self.eliminationGuessAlgorithm.guessCount = 3

        self.eliminationGuessAlgorithm.removeWord("guess")

        WordList_removeWord.assert_called_once_with("guess")
        self.assertIn("guess", self.eliminationGuessAlgorithm.eliminatedWords)

    def test_normal_guess(self, WordList_removeWord):
        self.eliminationGuessAlgorithm.guessCount = 2

        self.eliminationGuessAlgorithm.removeWord("random")

        WordList_removeWord.assert_not_called()


@patch(MODULE_PATH + "random")
class Test_EliminationCommon_nextWord(TestCase):

    def setUp(self):
        self.eliminationGuessAlgorithm = Elimination2GuessAlgorithm()
        self.eliminationGuessAlgorithm.eliminatedWords = ["tests"]
        self.eliminationGuessAlgorithm.wordList = ["guess"]

    def test_first_guess(self, random):
        self.eliminationGuessAlgorithm.nextWord()

        random.sample.assert_called_once_with(["guess"], 1)

    def test_less_than_elimination(self, random):
        self.eliminationGuessAlgorithm.guessCount = 1

        self.eliminationGuessAlgorithm.nextWord()

        random.sample.assert_called_once_with(["tests"], 1)

    def test_random_guess(self, random):
        self.eliminationGuessAlgorithm.guessCount = 2

        self.eliminationGuessAlgorithm.nextWord()

        random.sample.assert_called_once_with(["guess"], 1)
