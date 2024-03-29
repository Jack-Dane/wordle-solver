
from unittest import TestCase
from unittest.mock import MagicMock, patch

from wordle.wordProcessing.wordle import Wordle
from wordle.common.guessAlogrithms import GuessAlgorithm


class WordleTest(TestCase):

    def setUp(self):
        self.wordle = Wordle(GuessAlgorithm.GENERIC_GUESS_ALGORITHM, False)


@patch("wordle.wordProcessing.wordle.ConsolePrinter")
@patch("wordle.wordProcessing.wordle.ChromeDriverDocker")
class Test_Wordle_start(WordleTest):

    def setUp(self):
        super(Test_Wordle_start, self).setUp()
        self.wordle._run = MagicMock()
        self.wordle._runCheat = MagicMock()

    def test_standard_start(self, ChromeDriverDocker, _ConsolePrinter):
        self.wordle.start()

        self.wordle._run.assert_called_once_with()
        self.wordle._runCheat.assert_not_called()
        ChromeDriverDocker.return_value.kill.assert_called_once_with()

    def test_cheat_start(self, ChromeDriverDocker, _ConsolePrinter):
        self.wordle.start(cheat=True)

        self.wordle._runCheat.assert_called_once_with()
        self.wordle._run.assert_not_called()
        ChromeDriverDocker.return_value.kill.assert_called_once_with()

    def test_exception(self, ChromeDriverDocker, _ConsolePrinter):
        self.wordle._run.side_effect = Exception("Boom!")

        with self.assertRaises(Exception):
            self.wordle.start()

        ChromeDriverDocker.return_value.kill.assert_called_once_with()


@patch("wordle.wordProcessing.wordle.ConsolePrinter")
@patch("wordle.wordProcessing.wordle.WordProcessor")
class Test_Wordle__run(WordleTest):

    def setUp(self):
        super(Test_Wordle__run, self).setUp()
        self.wordle.driver = MagicMock()
        self.wordle.nextGuess = "crane"

    def test_stop_correct_answer(self, wordProcessor, _ConsolePrinter):
        wordProcessor.return_value.checkWon.return_value = True

        self.wordle._run()

        self.wordle.driver.makeGuess.assert_called_once_with("crane")
        wordProcessor.getNextGuess.assert_not_called()
        self.assertTrue(self.wordle.correctAnswer)

    def test_max_guesses_reached(self, wordProcessor, _ConsolePrinter):
        wordProcessor.return_value.checkWon.return_value = False

        self.wordle._run()

        self.assertEqual(6, self.wordle.driver.makeGuess.call_count)
        self.assertEqual(6, self.wordle.guesses)
        self.assertEqual(None, self.wordle.correctAnswer)

    def test_correct_on_third_attempt(self, wordProcessor, _ConsolePrinter):
        wordProcessor.return_value.checkWon.side_effect = [
            False, False, True
        ]

        self.wordle._run()

        self.assertEqual(3, self.wordle.driver.makeGuess.call_count)
        self.assertEqual(3, self.wordle.guesses)
        self.assertTrue(self.wordle.correctAnswer)


@patch("wordle.wordProcessing.wordle.ConsolePrinter")
@patch("wordle.wordProcessing.wordle.date")
@patch("wordle.wordProcessing.wordle.requests")
class Test_Wordle__runCheat(WordleTest):

    def setUp(self):
        super(Test_Wordle__runCheat, self).setUp()
        self.wordle.driver = MagicMock()

    def test_ok(self, requests, date, _ConsolePrinter):
        requests.get.return_value = MagicMock()
        requests.get.return_value.json.return_value = {
            "solution": "chant"
        }
        date.today.return_value = "2023-01-15"

        self.wordle._runCheat()

        self.wordle.driver.makeGuess.assert_called_once_with("chant")
        requests.get.assert_called_once_with(
            "https://www.nytimes.com/svc/wordle/v2/2023-01-15.json"
        )
