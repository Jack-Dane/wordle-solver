
from datetime import datetime

from wordle.wordProcessing.wordProcessor import WordProcessor
from wordle.drivers.driverObject import DriverObject
from wordle.wordProcessing.wordList import WordList
from wordle.models.results import insertResult


class Wordle:

    def __init__(self, guessingAlgorithm, logResults, firstGuess=None):
        self._logResults = logResults
        self._startDateTime = None
        self.driver = None
        self.guesses = 0
        self._guessingAlgorithm = guessingAlgorithm
        self._wordList = WordList.getWordlist(self._guessingAlgorithm)
        self.nextGuess = firstGuess or self._wordList.nextWord()
        self.correctAnswer = False
        self._firstGuess = None

    def start(self, cheat=False):
        self._startDateTime = datetime.now()
        self.driver = DriverObject()
        if cheat:
            self._runCheat()
        else:
            self._run()

    def _run(self):
        """
        Run the standard Wordle guessing
        """
        while not self.correctAnswer and self.guesses < 6:
            self.driver.makeGuess(self.nextGuess)
            if not self._firstGuess:
                self._firstGuess = self.nextGuess
            results = self.driver.collectResults(self.guesses)

            wordProcessor = WordProcessor(self._wordList)
            wordProcessor.processResults(self.nextGuess, results)
            if wordProcessor.totalCorrectLetters == 5:
                self.guesses += 1
                self.correctAnswer = True
            else:
                self.nextGuess = wordProcessor.getNextGuess()
                self.guesses += 1
        if self._logResults:
            self._captureResults()

    def _captureResults(self):
        correctAnswer = self.nextGuess if self.correctAnswer else "UNKNOWN"
        insertResult(
            self.correctAnswer, self.guesses, self._guessingAlgorithm, self._startDateTime,
            self._firstGuess, correctAnswer
        )

    def _runCheat(self):
        """
        Run wordle but guess the word first time
        """
        correctAnswer = self.driver.getAnswer()
        self.driver.makeGuess(correctAnswer)
