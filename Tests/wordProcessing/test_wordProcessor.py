
from unittest import TestCase
from unittest.mock import MagicMock, call

from wordle.wordProcessing.wordProcessor import WordProcessor
from wordle.common.letterResult import LetterValue


class WordProcessorTests(TestCase):

    def setUp(self):
        self.wordList = MagicMock(wordList=["apple", "juice", "uncle"])
        self.wordProcessor = WordProcessor(self.wordList, [])


class Test_WordProcessor__checkResults(WordProcessorTests):

    def setUp(self):
        super(Test_WordProcessor__checkResults, self).setUp()
        self.wordProcessor._absentLetter = MagicMock()
        self.wordProcessor._presentLetter = MagicMock()
        self.wordProcessor._correctLetter = MagicMock()

    def checkCall(self, noCall1, noCall2, allCalls):
        self.assertEqual(0, noCall1.call_count)
        self.assertEqual(0, noCall2.call_count)
        self.assertEqual(5, allCalls.call_count)

    def test_absent_letter(self):
        self.wordProcessor._results = [
            MagicMock(result=LetterValue.ABSENT), MagicMock(result=LetterValue.ABSENT),
            MagicMock(result=LetterValue.ABSENT), MagicMock(result=LetterValue.ABSENT),
            MagicMock(result=LetterValue.ABSENT)
        ]

        self.wordProcessor._checkResults()

        self.checkCall(
            self.wordProcessor._correctLetter, self.wordProcessor._presentLetter, self.wordProcessor._absentLetter
        )

    def test_present_letter(self):
        self.wordProcessor._results = [
            MagicMock(result=LetterValue.PRESENT), MagicMock(result=LetterValue.PRESENT),
            MagicMock(result=LetterValue.PRESENT), MagicMock(result=LetterValue.PRESENT),
            MagicMock(result=LetterValue.PRESENT)
        ]

        self.wordProcessor._checkResults()

        self.checkCall(
            self.wordProcessor._correctLetter, self.wordProcessor._absentLetter, self.wordProcessor._presentLetter
        )

    def test_correct_letter(self):
        self.wordProcessor._results = [
            MagicMock(result=LetterValue.CORRECT), MagicMock(result=LetterValue.CORRECT),
            MagicMock(result=LetterValue.CORRECT), MagicMock(result=LetterValue.CORRECT),
            MagicMock(result=LetterValue.CORRECT)
        ]

        self.wordProcessor._checkResults()

        self.checkCall(
            self.wordProcessor._absentLetter, self.wordProcessor._presentLetter, self.wordProcessor._correctLetter
        )


class Test_WordProcessor__doubleLetterCheck(WordProcessorTests):

    def test_doesnt_have_double_letter(self):
        self.wordProcessor._doubleLetter = {"p"}

        self.wordProcessor._doubleLetterCheck()

        self.assertEqual({"juice", "uncle"}, self.wordProcessor.wordsToRemove)

    def test_has_double_letter(self):
        self.wordProcessor._notDoubleLetter = {"p"}

        self.wordProcessor._doubleLetterCheck()

        self.assertEqual({"apple"}, self.wordProcessor.wordsToRemove)

    def test_no_double_letter_check(self):
        self.wordProcessor._doubleLetterCheck()

        self.assertEqual(set(), self.wordProcessor.wordsToRemove)


class Test_WordProcessor__absentLetter(WordProcessorTests):

    def test_not_already_seen_in_word(self):
        self.wordProcessor._alreadySeenBeforeInWord = MagicMock(return_value=False)

        self.wordProcessor._absentLetter(0, "u")

        self.assertEqual({"juice", "uncle"}, self.wordProcessor.wordsToRemove)

    def test_seen_in_word_same_index(self):
        self.wordProcessor._alreadySeenBeforeInWord = MagicMock(return_value=True)

        self.wordProcessor._absentLetter(1, "u")

        self.assertEqual({"juice"}, self.wordProcessor.wordsToRemove)

    def test_double_letter_word(self):
        self.wordProcessor._alreadySeenBeforeInWord = MagicMock(return_value=False)
        self.wordProcessor._guessWord = "unsure"

        self.wordProcessor._absentLetter(1, "u")

        self.assertEqual({"u"}, self.wordProcessor._notDoubleLetter)


class Test_WordProcessor__correctLetter(WordProcessorTests):

    def test_ok(self):
        self.wordProcessor._correctLetter(1, "u")

        self.assertEqual({"apple", "uncle"}, self.wordProcessor.wordsToRemove)


class Test_WordProcessor__presentLetter(WordProcessorTests):

    def test_ok(self):
        self.wordProcessor._presentLetter(3, "u")

        self.assertEqual({"apple"}, self.wordProcessor.wordsToRemove)


class Test_WordProcessor__reduceWordList(WordProcessorTests):

    def test_ok(self):
        self.wordProcessor._guessWord = "tests"
        self.wordList.removeWord = MagicMock()
        self.wordProcessor.wordsToRemove = {"audio", "juice"}

        self.wordProcessor._reduceWordList()

        self.wordList.removeWord.assert_has_calls(
            [call("audio"), call("juice")], True
        )
        self.assertEqual(set(), self.wordProcessor.wordsToRemove)


class Test_WordProcessor_addCorrectLetterWordToSet(WordProcessorTests):

    def test_present_double_letter(self):
        self.wordProcessor._presentOrCorrectLetters = {"a"}

        self.wordProcessor.addCorrectLetterWordToSet("a")

        self.assertEqual({"a"}, self.wordProcessor._presentOrCorrectLetters)
        self.assertEqual({"a"}, self.wordProcessor._doubleLetter)

    def test_present_letter(self):
        self.wordProcessor._presentOrCorrectLetters = set()

        self.wordProcessor.addCorrectLetterWordToSet("a")

        self.assertEqual({"a"}, self.wordProcessor._presentOrCorrectLetters)
        self.assertEqual(set(), self.wordProcessor._doubleLetter)


class Test_WordProcessor_checkWon(WordProcessorTests):

    def test_won(self):
        self.wordProcessor._results = [
            MagicMock(result=LetterValue.CORRECT), MagicMock(result=LetterValue.CORRECT),
            MagicMock(result=LetterValue.CORRECT), MagicMock(result=LetterValue.CORRECT),
            MagicMock(result=LetterValue.CORRECT)
        ]

        won = self.wordProcessor.checkWon()

        self.assertTrue(won)

    def test_lost(self):
        self.wordProcessor._results = [
            MagicMock(result=LetterValue.ABSENT), MagicMock(result=LetterValue.PRESENT),
            MagicMock(result=LetterValue.CORRECT), MagicMock(result=LetterValue.ABSENT),
            MagicMock(result=LetterValue.CORRECT)
        ]

        won = self.wordProcessor.checkWon()

        self.assertFalse(won)
