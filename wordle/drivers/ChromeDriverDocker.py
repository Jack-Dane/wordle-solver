
import time

import docker
import requests
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from wordle.common.letterResult import LetterResult, LetterValue
from wordle.vnc.VNCViewer import VNCViewer


class FailedToStartSeleniumException(Exception):
    pass


class _SeleniumDocker:
    _SELENIUM_IMAGE_NAME = "selenium/standalone-chrome"

    def __init__(self):
        self._container = None
        self._driverPort = 4444
        self._host = "localhost"
        self._client = docker.from_env()

    @property
    def driverPort(self):
        return self._driverPort

    @property
    def host(self):
        return self._host

    def run(self):
        self._createContainer()
        self._waitForSelenium()

    def _createContainer(self):
        self._container = self._client.containers.run(
            self._SELENIUM_IMAGE_NAME,
            ports={
                "4444": 4444,
                "7900": 7900,
                "5900": 5900
            },
            detach=True,
            shm_size="2g"
        )

    def _waitForSelenium(self):
        timeout = 20
        attempt = 0
        while attempt < timeout:
            try:
                response = requests.get("http://localhost:4444/wd/hub/status")
                if response.json().get("value", {}).get("ready"):
                    return
            except ConnectionError:
                # Selenium hasn't started yet
                pass
            attempt += 1
            time.sleep(.5)
        else:
            raise FailedToStartSeleniumException(
                "Selenium failed to start in container after 10 seconds"
            )

    def remove(self):
        if not self._container:
            return

        self._container.remove(force=True)
        self._container = None

    def __del__(self):
        self.remove()


class _ChromeDriver:

    def __init__(self, driverContainer):
        chromeOptions = Options()
        self.driver = webdriver.Remote(
            f"http://{driverContainer.host}:{driverContainer.driverPort}/wd/hub",
            options=chromeOptions
        )

    def start(self):
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
        self.driver.maximize_window()
        self.closeCookiesNotification()
        self.closeModalDialog()

    def _waitForElement(self, selector, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(selector)
        )

    def closeModalDialog(self):
        modalDialogXpath = "//button[@class='Modal-module_closeIcon__TcEKb']/*[name()='svg']"
        self._waitForElement((By.XPATH, modalDialogXpath)).click()

        timeout = 10
        attempt = 0
        while attempt < timeout:
            if not self.driver.find_elements(By.XPATH, modalDialogXpath):
                break

            attempt += 1
            time.sleep(.5)

    def closeCookiesNotification(self):
        self._waitForElement((By.ID, "pz-gdpr-btn-accept")).click()
        # hide the ok popup window, stops us from clicking on the letter keys
        self._waitForElement((By.CLASS_NAME, "pz-snackbar"))
        self.driver.execute_script(
            "document.querySelector('.pz-snackbar').style.display = 'None';"
        )

    def makeGuess(self, word):
        """
        Input the guess into the wordle
        :param word: the word to guess
        """
        for letter in word:
            letterElement = self.driver.find_element(
                By.XPATH, f"//button[@data-key='{letter}']"
            )
            letterElement.click()
        self.driver.find_element(By.XPATH, "//button[@data-key='\u21B5']").click()
        time.sleep(2)  # wait for the elements to calculate

    def collectResults(self, guessNumber):
        """
        Read the results from the driver, return the results with the correct letters first
        :param guessNumber: The number of guesses that has now been made
        :return: LetterResult object list
        """
        result = []
        for index in range(guessNumber * 5, guessNumber * 5 + 5):
            letter, evaluation = self._getEvaluation(index)
            letterResult = LetterResult(letter, LetterValue.fromString(evaluation), index % 5)
            if letterResult.result == LetterValue.CORRECT:
                # Correct letters need to go first when being returned for easier processing.
                # A correct letter will always be in the correct place and present.
                # If an absent letter was recorded at index 0 but the same correct letter was at index 3.
                # We need to pass the correct letter first rather than read index 0 first and assume that the word
                # doesn't have that letter in it.
                # EG: guess word: zoppa correct word: adopt
                # without putting correct letters first, the processor assumes that there isn't a p as the first guessed
                # p is absent.
                result.insert(0, letterResult)
            else:
                result.append(letterResult)
        return result

    def _getEvaluation(self, index):
        element = self.driver.find_elements(
            By.XPATH, f"//div[@class='Tile-module_tile__UWEHN']"
        )[index]
        # example ariel-label = "e correct"
        return element.get_attribute("aria-label").split(" ")


class ChromeDriverDocker(_ChromeDriver):

    def __init__(self, vnc):
        self._seleniumDocker = _SeleniumDocker()
        self._seleniumDocker.run()
        self._vnc = None
        if vnc:
            self._vnc = VNCViewer()
        super().__init__(self._seleniumDocker)
        self.start()

    def kill(self):
        """ clean up processes created by this object
        """
        if self._vnc:
            self._vnc.kill()
        self._seleniumDocker.remove()
