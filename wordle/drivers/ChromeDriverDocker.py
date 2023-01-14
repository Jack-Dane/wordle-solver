
import time

import docker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from wordle.common.letterResult import LetterResult


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

    def createContainer(self):
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

    def remove(self):
        if not self._container:
            return

        self._container.remove(force=True)

    def __del__(self):
        self.remove()


class _ChromeDriver:

    def __init__(self, headless, driverContainer):
        chromeOptions = Options()
        if headless:
            chromeOptions.add_argument("--headless")
        self.driver = webdriver.Remote(
            f"http://{driverContainer.host}:{driverContainer.driverPort}/wd/hub",
            options=chromeOptions
        )
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
        self.driver.maximize_window()
        self.closeCookiesNotification()
        self.closeModalDialog()

    def _waitForElement(self, selector, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(selector)
        )

    def closeModalDialog(self):
        self._waitForElement(
            (By.XPATH, "//button[@class='Modal-module_closeIcon__TcEKb']/*[name()='svg']")
        ).click()
        # TODO: wait for the modal dialog to disappear
        time.sleep(5)

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
            letterElement = self.driver.find_element(By.XPATH, f"//button[@data-key='{letter}']")
            letterElement.click()
        self.driver.find_element(By.XPATH, "//button[@data-key='\u21B5']").click()
        time.sleep(2)  # wait for the elements to calculate

    def collectResults(self, guessNumber):
        """
        Read the results from the driver, return the results with the correct letters first
        :param row: The row element of the last guess
        :return: LetterResult object list
        """
        result = []
        for index in range(guessNumber * 5, guessNumber * 5 + 5):
            element = self.driver.find_elements(
                By.XPATH, f"//div[@class='Tile-module_tile__UWEHN']"
            )[index]
            # example ariel-label = "e correct"
            letter, evaluation = element.get_attribute("aria-label").split(" ")
            letterResult = LetterResult(letter, evaluation, index % 5)
            if evaluation == "correct":
                result.insert(0, letterResult)
            else:
                result.append(letterResult)
        return result

    def getAnswer(self):
        return self.driver.execute_script(
            "return JSON.parse(localStorage.getItem(\"nyt-wordle-state\"))[\"solution\"];"
        )


class ChromeDriverDocker(_ChromeDriver):

    def __init__(self, headless):
        self._seleniumDocker = _SeleniumDocker()
        self._seleniumDocker.createContainer()
        # TODO: poll to see if it can connect
        time.sleep(10)
        super().__init__(headless, self._seleniumDocker)