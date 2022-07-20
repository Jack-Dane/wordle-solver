
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from wordle.common.letterResult import LetterResult


class DriverObject:

    def __init__(self, headless, chromeDriverPath="./wordle/drivers/chromedriver"):
        chromeOptions = Options()
        if headless:
            chromeOptions.add_argument("--headless")
        driverService = Service(executable_path=chromeDriverPath)
        self.driver = webdriver.Chrome(service=driverService, options=chromeOptions)
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
        self.driver.maximize_window()
        self.closeCookiesNotification()
        self.closeModalDialog()

    def _waitForElement(self, selector, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(selector)
        )

    def closeModalDialog(self):
        closeElement = self._waitForElement(
            (By.XPATH, "//div[@class='Modal-module_closeIcon__b4z74']/*[name()='svg']")
        )
        closeElement.click()

    def closeCookiesNotification(self):
        acceptCookies = self._waitForElement((By.ID, "pz-gdpr-btn-accept"))
        acceptCookies.click()
        # hide the ok popup window, stops us from clicking on the letter keys
        self._waitForElement((By.CLASS_NAME, "pz-snackbar"))
        self.driver.execute_script(
            "document.querySelector('.pz-snackbar').style.display = 'None';"
        )

    def __del__(self):
        self.stop()

    def stop(self):
        self.driver.close()

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
        row = self.driver.find_elements(
            By.CLASS_NAME, "Row-module_row__dEHfN"
        )[guessNumber]
        return self._readResults(row)

    def _readResults(self, row):
        """
        Read the results from the driver, return the results with the correct letters first
        :param row: The row element of the last guess
        :return: LetterResult object list
        """
        result = []
        for index, element in enumerate(
                row.find_elements(By.CLASS_NAME, "Tile-module_tile__3ayIZ")
        ):
            evaluation = element.get_attribute("data-state")
            letter = element.text.lower()
            letterResult = LetterResult(letter, evaluation, index)
            if evaluation == "correct":
                result.insert(0, letterResult)
            else:
                result.append(letterResult)
        return result

    def getAnswer(self):
        return self.driver.execute_script(
            "return JSON.parse(localStorage.getItem(\"nyt-wordle-state\"))[\"solution\"];"
        )
