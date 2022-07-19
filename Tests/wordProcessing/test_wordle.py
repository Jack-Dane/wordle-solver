
from unittest import TestCase
from unittest.mock import MagicMock, patch

from wordle.wordProcessing.wordle import Wordle
from wordle.common.guessAlogrithms import GuessAlgorithm


class WordleTest(TestCase):

    def setUp(self):
        self.wordle = Wordle(GuessAlgorithm.GENERIC_GUESS_ALGORITHM, False)


@patch("wordle.wordProcessing.wordle.DriverObject")
class Test_Wordle_start(WordleTest):

    def setUp(self):
        super(Test_Wordle_start, self).setUp()
        self.wordle._run = MagicMock()
        self.wordle._runCheat = MagicMock()

    def test_standard_start(self, driverObject):
        self.wordle.start()

        self.wordle._run.assert_called_once_with()
        self.wordle._runCheat.assert_not_called()

    def test_cheat_start(self, driverObject):
        self.wordle.start(cheat=True)

        self.wordle._runCheat.assert_called_once_with()
        self.wordle._run.assert_not_called()


@patch("wordle.wordProcessing.wordle.WordProcessor")
class Test_Wordle__run(WordleTest):

    def setUp(self):
        super(Test_Wordle__run, self).setUp()
        self.wordle.driver = MagicMock()
        self.wordle.nextGuess = "crane"

    def test_stop_correct_answer(self, wordProcessor):
        wordProcessor.return_value = MagicMock(totalCorrectLetters=5)

        self.wordle._run()

        self.wordle.driver.makeGuess.assert_called_once_with("crane")
        wordProcessor.getNextGuess.assert_not_called()
        self.assertTrue(self.wordle.correctAnswer)

    def test_max_guesses_reached(self, wordProcessor):
        self.wordle._run()

        self.assertEqual(6, self.wordle.driver.makeGuess.call_count)
        self.assertEqual(6, self.wordle.guesses)
        self.assertEqual("UNKNOWN", self.wordle.correctAnswer)

    def test_correct_on_third_attempt(self, wordProcessor):
        wordProcessor.side_effect = [
            MagicMock(totalCorrectLetters=0),
            MagicMock(totalCorrectLetters=4),
            MagicMock(totalCorrectLetters=5)
        ]

        self.wordle._run()

        self.assertEqual(3, self.wordle.driver.makeGuess.call_count)
        self.assertEqual(3, self.wordle.guesses)
        self.assertTrue(self.wordle.correctAnswer)


class Test_Wordle__runCheat(WordleTest):

    def setUp(self):
        super(Test_Wordle__runCheat, self).setUp()
        self.wordle.driver = MagicMock()

    def test_ok(self):
        self.wordle.driver.getAnswer.return_value = "chant"

        self.wordle._runCheat()

        self.wordle.driver.makeGuess.assert_called_once_with("chant")
