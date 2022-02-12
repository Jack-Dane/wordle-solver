
class WordProcessor:

    def __init__(self, wordList):
        self._wordList = wordList
        self._guessWord = ""
        self._presentOrCorrectLetters = set()
        self._doubleLetter = set()
        self.wordsToRemove = set()
        self.totalCorrectLetters = 0
        self._latestResult = None

    def processResults(self, guessWord, results):
        self._guessWord = guessWord
        self._latestResult = results
        self._checkResults()
        self._reduceWordList()

    def _checkResults(self):
        for letterResult in self._latestResult:
            if letterResult.result == "absent":
                self._absentLetter(letterResult.letter)
            elif letterResult.result == "present":
                self._presentLetter(letterResult.index, letterResult.letter)
            else:
                self.totalCorrectLetters += 1
                self._correctLetter(letterResult.index, letterResult.letter)
        self._doubleLetterCheck()

    def _doubleLetterCheck(self):
        if not self._doubleLetter:
            return

        for word in self._wordList.wordList:
            for letter in self._doubleLetter:
                if word.count(letter) != 2:
                    self.wordsToRemove.add(word)
        self._doubleLetter = set()

    def getNextGuess(self):
        return self._wordList.nextWord()

    def _absentLetter(self, letter):
        for word in self._wordList.wordList:
            if letter in word and not self._alreadySeenBeforeInWord(letter):
                self.wordsToRemove.add(word)

    def _correctLetter(self, index, letter):
        if letter in self._presentOrCorrectLetters:
            self._doubleLetter.add(letter)

        for word in self._wordList.wordList:
            if word[index] != letter:
                self.wordsToRemove.add(word)
        self._presentOrCorrectLetters.add(letter)

    def _alreadySeenBeforeInWord(self, letter):
        return letter in self._presentOrCorrectLetters

    def _presentLetter(self, index, letter):
        if letter in self._presentOrCorrectLetters:
            self._doubleLetter.add(letter)

        for word in self._wordList.wordList:
            if word[index] == letter or letter not in word:
                self.wordsToRemove.add(word)
        self._presentOrCorrectLetters.add(letter)

    def _reduceWordList(self):
        for word in self.wordsToRemove:
            self._wordList.removeWord(word)
