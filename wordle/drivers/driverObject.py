
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from wordle.common.letterResult import LetterResult


class DriverObject:

    def __init__(self):
        driverService = Service(executable_path="./wordle/drivers/chromedriver")
        self.driver = webdriver.Chrome(service=driverService)
        self.driver.get("https://www.powerlanguage.co.uk/wordle/")
        self.closeModalDialog()

    def closeModalDialog(self):
        time.sleep(2)
        self.driver.execute_script(
            "document.querySelector(\"game-app\")"
            ".shadowRoot.querySelector(\"game-modal\")"
            ".shadowRoot.querySelector(\"game-icon\")"
            ".click();"
        )
        time.sleep(1)

    def __del__(self):
        self.stop()

    def stop(self):
        self.driver.close()

    def makeGuess(self, word):
        body = self.driver.find_element(By.XPATH, "//body")
        body.send_keys(word)
        body.send_keys(Keys.RETURN)
        time.sleep(2)

    def collectResults(self, guessNumber):
        row = self.driver.execute_script(
            f"return document.querySelector(\"game-app\")"
            f".shadowRoot.querySelector(\"game-theme-manager\")"
            f".querySelectorAll(\"game-row\")[{guessNumber}];")
        return self._readResults(row)

    def _readResults(self, row):
        result = []
        for index, element in enumerate(
                row.shadow_root.find_elements(By.CSS_SELECTOR, "game-tile")
        ):
            evaluation = element.get_attribute("evaluation")
            letter = element.get_attribute("letter")
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
