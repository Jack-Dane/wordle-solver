
from .wordProcessor import WordProcessor
from wordle.drivers.driverObject import DriverObject
from .wordList import WordList


class Wordle:

    def __init__(self, firstGuess=None):
        self.driver = None
        self.nextGuess = firstGuess or "audio"
        self.guesses = 0
        self._wordList = WordList()
        self.correctAnswer = False

    def start(self, cheat=False):
        self.driver = DriverObject()
        if cheat:
            self._runCheat()
        else:
            self._run()

    def _run(self):
        while not self.correctAnswer and self.guesses < 6:
            self.driver.makeGuess(self.nextGuess)
            results = self.driver.collectResults(self.guesses)

            wordProcessor = WordProcessor(self._wordList)
            wordProcessor.processResults(self.nextGuess, results)
            if wordProcessor.totalCorrectLetters == 5:
                self.correctAnswer = True
            else:
                self.nextGuess = wordProcessor.getNextGuess()
                self.guesses += 1

    def _runCheat(self):
        correctAnswer = self.driver.getAnswer()
        self.driver.makeGuess(correctAnswer)
