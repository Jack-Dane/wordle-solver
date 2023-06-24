
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from requests.exceptions import ConnectionError

from wordle.drivers.ChromeDriverDocker import (
    _ChromeDriver, _SeleniumDocker, FailedToStartSeleniumException
)
from wordle.common.letterResult import LetterValue, LetterResult


class SeleniumDockerTest(TestCase):

    def setUp(self):
        with patch("wordle.drivers.ChromeDriverDocker.docker") as dockerMock:
            self.dockerEnvMock = MagicMock()
            dockerMock.from_env.return_value = self.dockerEnvMock
            self.driverDocker = _SeleniumDocker()


class Test__SeleniumDocker__createContainer(SeleniumDockerTest):

    def test_ok(self):
        self.driverDocker._createContainer()

        self.dockerEnvMock.containers.run.assert_called_once_with(
            "selenium/standalone-chrome:114.0",
            ports={
                "4444": 4444,
                "7900": 7900,
                "5900": 5900
            },
            detach=True,
            shm_size="2g"
        )


@patch("wordle.drivers.ChromeDriverDocker.time")
@patch("wordle.drivers.ChromeDriverDocker.requests")
class Test__SeleniumDocker__waitForSelenium(SeleniumDockerTest):

    def _createMockResponse(self, jsonValue):
        response = MagicMock()
        response.json.return_value = jsonValue
        return response

    def test_started_ok(self, requests, time):
        requests.get.side_effect = [
            ConnectionError,
            ConnectionError,
            self._createMockResponse({}),
            self._createMockResponse({"value": {}}),
            self._createMockResponse({"value": {"ready": False}}),
            self._createMockResponse({"value": {"ready": True}})
        ]

        self.driverDocker._waitForSelenium()

        self.assertEqual(5, len(time.sleep.mock_calls))

    def test_failed_to_start(self, requests, time):
        requests.get.side_effect = ConnectionError

        with self.assertRaises(FailedToStartSeleniumException):
            self.driverDocker._waitForSelenium()

        self.assertEqual(20, len(time.sleep.mock_calls))


class Test__SeleniumDocker_remove(SeleniumDockerTest):

    def test_ok(self):
        container = MagicMock()
        self.driverDocker._container = container

        self.driverDocker.remove()

        container.remove.assert_called_once_with(force=True)
        self.assertIsNone(self.driverDocker._container)


class ChromeDriverTest(TestCase):

    def setUp(self):
        with patch("wordle.drivers.ChromeDriverDocker.webdriver.Remote"):
            self.chromeDriver = _ChromeDriver(MagicMock(host="localhost", driverPort=4444))


@patch.object(_ChromeDriver, "_getEvaluation")
class Test__ChromeDriver_collectResults(ChromeDriverTest):

    def createWebElement(self, letter, evaluation):
        result = MagicMock(text=letter)
        result.get_attribute.return_value = evaluation
        return result

    def test_ok(self, _ChromeDriver_getEvaluation):
        _ChromeDriver_getEvaluation.side_effect = [
            ("b", "present"), ("a", "correct"), ("c", "absent"), ("e", "present"), ("f", "correct")
        ]

        results = self.chromeDriver.collectResults(0)

        self.assertEqual(
            [
                LetterResult("f", LetterValue.CORRECT, 4),
                LetterResult("a", LetterValue.CORRECT, 1),
                LetterResult("b", LetterValue.PRESENT, 0),
                LetterResult("c", LetterValue.ABSENT, 2),
                LetterResult("e", LetterValue.PRESENT, 3)
            ],
            results
        )


@patch("wordle.drivers.ChromeDriverDocker.time")
@patch.object(_ChromeDriver, "_waitForElement")
class Test__ChromeDriver_closeModalDialog(ChromeDriverTest):

    def test_ok(self, ChromeDriver_waitForElement, time):
        self.chromeDriver.driver.find_elements.side_effect = [
            True, True, True, False
        ]

        self.chromeDriver.closeModalDialog()

        ChromeDriver_waitForElement.assert_called_once_with(
            ("xpath", "//button[@class='Modal-module_closeIcon__TcEKb']/*[name()='svg']")
        )
        ChromeDriver_waitForElement.return_value.click.assert_called_once_with()
        self.assertEqual(3, len(time.sleep.mock_calls))

    def test_timeout(self, ChromeDriver_waitForElement, time):
        self.chromeDriver.driver.find_elements.return_value = True

        self.chromeDriver.closeModalDialog()

        ChromeDriver_waitForElement.assert_called_once_with(
            ("xpath", "//button[@class='Modal-module_closeIcon__TcEKb']/*[name()='svg']")
        )
        ChromeDriver_waitForElement.return_value.click.assert_called_once_with()
        self.assertEqual(10, len(time.sleep.mock_calls))
