
from wordle.common.letterResult import LetterValue


def presentCorrectLetter(presentCorrectFunc):
    def addElementsToList(model, index, letter):
        model.addCorrectLetterWordToSet(letter)
        return presentCorrectFunc(model, index, letter)
    return addElementsToList


class WordProcessor:

    def __init__(self, wordList, results):
        self._wordList = wordList
        self._guessWord = ""
        self._presentOrCorrectLetters = set()
        self._doubleLetter = set()
        self._notDoubleLetter = set()
        self.wordsToRemove = set()
        self._results = results

    def processResults(self, guessWord):
        """
        Process the results added and reduce the wordlist
        :param guessWord: The word that was guessed
        """
        # TODO not make it dependent on passing correct letters first
        self._guessWord = guessWord
        self._wordList.removeWord(self._guessWord)
        self._checkResults()

    def checkWon(self):
        return len(
            [
                letterResult for letterResult in self._results if
                letterResult.result == LetterValue.CORRECT
            ]
        ) == len(self._results)

    def _checkResults(self):
        """
        Check each result object to see then reduce the wordlist
        """
        for letterResult in self._results:
            if letterResult.result == LetterValue.ABSENT:
                self._absentLetter(letterResult.index, letterResult.letter)
            elif letterResult.result == LetterValue.PRESENT:
                self._presentLetter(letterResult.index, letterResult.letter)
            else:
                self._correctLetter(letterResult.index, letterResult.letter)
            self._reduceWordList()

        self._doubleLetterCheck()
        self._reduceWordList()

    def _doubleLetterCheck(self):
        """
        Check all words that:
        1. Have a double letter they shouldn't
        or
        2. Don't have a double letter that they should
        Mark words to remove
        """
        for word in self._wordList.wordList:
            for letter in self._doubleLetter:
                if word.count(letter) != 2:
                    self.wordsToRemove.add(word)

            for letter in self._notDoubleLetter:
                if word.count(letter) == 2:
                    self.wordsToRemove.add(word)
        self._notDoubleLetter = set()
        self._doubleLetter = set()

    def getNextGuess(self):
        return self._wordList.nextWord()

    def _absentLetter(self, index, letter):
        """
        Process an absent letter
        :param index: index of the letter in the guess word
        :param letter: letter to check
        """
        for word in self._wordList.wordList:
            if letter in word:
                if not self._alreadySeenBeforeInWord(letter):
                    self.wordsToRemove.add(word)
                elif word[index] == letter:
                    self.wordsToRemove.add(word)
                if self._guessWord.count(letter) > 1:
                    self._notDoubleLetter.add(letter)

    @presentCorrectLetter
    def _correctLetter(self, index, letter):
        """
        Process a correct letter
        :param index: index of the letter in the guess word
        :param letter: letter to check
        """
        for word in self._wordList.wordList:
            if word[index] != letter:
                self.wordsToRemove.add(word)

    @presentCorrectLetter
    def _presentLetter(self, index, letter):
        """
        Process a present letter, correct letter wrong place
        :param index: index of the letter in the guess word
        :param letter: letter to check
        """
        for word in self._wordList.wordList:
            if word[index] == letter or letter not in word:
                self.wordsToRemove.add(word)

    def _alreadySeenBeforeInWord(self, letter):
        return letter in self._presentOrCorrectLetters

    def _reduceWordList(self):
        """
        Remove the words in words to remove from the wordlist
        """
        for word in self.wordsToRemove:
            self._wordList.removeWord(word)
        self.wordsToRemove = set()

    def addCorrectLetterWordToSet(self, letter):
        """
        If the letter is correct or present use this decorator to add it to the set
        :param letter: letter to be added
        """
        if letter in self._presentOrCorrectLetters:
            self._doubleLetter.add(letter)

        self._presentOrCorrectLetters.add(letter)
