
import requests
from datetime import datetime
from datetime import date

from wordle.wordProcessing.wordProcessor import WordProcessor
from wordle.drivers.ChromeDriverDocker import ChromeDriverDocker
from wordle.wordProcessing.wordList import WordList
from wordle.models.results import insertResult


class Wordle:

    def __init__(self, guessingAlgorithm, logResults, firstGuess=None):
        self._guessingAlgorithm = guessingAlgorithm
        self._logResults = logResults
        self._startDateTime = None
        self.driver = None
        self.guesses = 0
        self._wordList = WordList.getWordlist(self._guessingAlgorithm)
        self.nextGuess = firstGuess or self._wordList.nextWord()
        self.correctAnswer = "UNKNOWN"
        self._firstGuess = None

    def start(self, headless, cheat=False, vnc=False):
        self._startDateTime = datetime.now()
        self.driver = ChromeDriverDocker(headless, vnc)
        if cheat:
            self._runCheat()
        else:
            self._run()

    def _run(self):
        """
        Run the standard Wordle guessing
        """
        while self.correctAnswer == "UNKNOWN" and self.guesses < 6:
            self.driver.makeGuess(self.nextGuess)
            if not self._firstGuess:
                self._firstGuess = self.nextGuess
            results = self.driver.collectResults(self.guesses)

            wordProcessor = WordProcessor(self._wordList)
            wordProcessor.processResults(self.nextGuess, results)
            if wordProcessor.totalCorrectLetters == 5:
                self.guesses += 1
                self.correctAnswer = self.nextGuess
            else:
                self.nextGuess = wordProcessor.getNextGuess()
                self.guesses += 1
        if self._logResults:
            self._captureResults()
        self.driver.kill()

    def _captureResults(self):
        insertResult(
            self.guesses, self._guessingAlgorithm, self._startDateTime,
            self._firstGuess, self.correctAnswer
        )

    def _runCheat(self):
        """
        Run wordle but guess the word first time
        """
        solutionURL = f"https://www.nytimes.com/svc/wordle/v2/{date.today()}.json"
        response = requests.get(solutionURL)
        correctAnswer = response.json()["solution"]
        self.driver.makeGuess(correctAnswer)
