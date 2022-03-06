
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from wordle.drivers.driverObject import DriverObject


@patch("wordle.drivers.driverObject.Service")
@patch("wordle.drivers.driverObject.webdriver.Chrome")
@patch("wordle.drivers.driverObject.LetterResult")
class Test_DriverObject__readResults(TestCase):

    def createShadowRoot(self, letter, evaluation):
        result = MagicMock()
        result.get_attribute.side_effect = [evaluation, letter]
        return result

    def test_ok(self, LetterResult, webdriver_Chrome, Service):
        row = MagicMock()
        row.shadow_root.find_elements.return_value = [
            self.createShadowRoot("b", "present"), self.createShadowRoot("a", "correct"),
            self.createShadowRoot("c", "absent"), self.createShadowRoot("e", "present"),
            self.createShadowRoot("f", "correct")
        ]
        driverObject = DriverObject()

        results = driverObject._readResults(row)

        self.assertEqual(
            [
                call("b", "present", 0),
                call("a", "correct", 1),
                call("c", "absent", 2),
                call("e", "present", 3),
                call("f", "correct", 4)
            ],
            LetterResult.mock_calls
        )
        self.assertEqual(
            [
                LetterResult("f", "correct", 4),
                LetterResult("a", "correct", 1),
                LetterResult("b", "present", 0),
                LetterResult("c", "absent", 2),
                LetterResult("e", "present", 3)
            ],
            results
        )
