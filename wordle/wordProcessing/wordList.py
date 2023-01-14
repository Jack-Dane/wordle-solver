
from abc import ABC, abstractmethod
import random

from wordle.common.guessAlogrithms import GuessAlgorithm


class WordList(ABC):

    def __init__(self):
        self.wordList = set()
        with open("wordleList.txt", "r") as wordList:
            for word in wordList:
                self.wordList.add(word.strip())

    def removeWord(self, word):
        self.wordList.remove(word)

    @staticmethod
    def getWordlist(guessAlgorithm):
        if guessAlgorithm == GuessAlgorithm.GENERIC_GUESS_ALGORITHM:
            return RandomFromSample()
        elif guessAlgorithm == GuessAlgorithm.ELIMINATION_2_GUESS_ALGORITHM:
            return Elimination2GuessAlgorithm()
        elif guessAlgorithm == GuessAlgorithm.ELIMINATION_3_GUESS_ALGORITHM:
            return Elimination3GuessAlgorithm()
        raise NotImplementedError

    @abstractmethod
    def nextWord(self):
        pass


class RandomFromSample(WordList):

    def nextWord(self):
        return random.sample(self.wordList, 1)[0]


class EliminationCommon(WordList, ABC):
    eliminatedWords = []
    guessCount = 0

    @property
    @abstractmethod
    def randomLimit(self):
        pass

    @property
    def isFirstGuess(self):
        return self.guessCount == 1

    @property
    def isLessThanEliminationCount(self):
        return self.guessCount <= self.randomLimit

    def removeWord(self, word):
        if self.isFirstGuess or not self.isLessThanEliminationCount:
            super().removeWord(word)
            self.eliminatedWords.append(word)

    def nextWord(self):
        self.guessCount += 1
        if not self.isFirstGuess and self.isLessThanEliminationCount:
            return random.sample(self.eliminatedWords, 1)[0]
        else:
            return random.sample(self.wordList, 1)[0]


class Elimination2GuessAlgorithm(EliminationCommon):

    @property
    def randomLimit(self):
        return 2


class Elimination3GuessAlgorithm(EliminationCommon):

    @property
    def randomLimit(self):
        return 3
