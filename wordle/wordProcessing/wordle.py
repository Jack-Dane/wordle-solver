
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
        """
        Run the standard Wordle guessing
        """
        while not self.correctAnswer and self.guesses < 6:
            self.driver.makeGuess(self.nextGuess)
            results = self.driver.collectResults(self.guesses)

            wordProcessor = WordProcessor(self._wordList)
            wordProcessor.processResults(self.nextGuess, results)
            if wordProcessor.totalCorrectLetters == 5:
                self.guesses += 1
                self.correctAnswer = True
            else:
                self.nextGuess = wordProcessor.getNextGuess()
                self.guesses += 1

    def _runCheat(self):
        """
        Run wordle but guess the word first time
        """
        correctAnswer = self.driver.getAnswer()
        self.driver.makeGuess(correctAnswer)
