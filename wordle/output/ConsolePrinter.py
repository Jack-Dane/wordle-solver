
from wordle.common.letterResult import LetterValue


COLORS = {
    LetterValue.CORRECT: "\u001b[32m",
    LetterValue.PRESENT: "\u001b[33m",
    LetterValue.ABSENT: "\u001b[37m",
}
RESET = "\u001b[0m"

def printHeader():
    print(
        """
 __    __              _ _        __       _                 _ 
/ / /\ \ \___  _ __ __| | | ___  / _\ ___ | |_   _____ _ __ / \ 
\ \/  \/ / _ \| '__/ _` | |/ _ \ \ \ / _ \| \ \ / / _ \ '__/  /
 \  /\  / (_) | | | (_| | |  __/ _\ \ (_) | |\ V /  __/ | /\_/ 
  \/  \/ \___/|_|  \__,_|_|\___| \__/\___/|_| \_/ \___|_| \/  
        """
    )


def printResults(letterResults, wordlistLength):
    """ Print the guess word with the relevant colours
    :param letterResults: A list of letterResults from the last guess
    :param wordlistLength: The length of the remaining wordlist
    """
    # correctly order the letter results
    letterResults.sort(key=lambda lr: lr.index)

    resultLine = ""
    for letterResult in letterResults:
        resultLine += COLORS[letterResult.result] + letterResult.letter
    resultLine += RESET
    resultLine += f" Words remaining {wordlistLength}"
    print(resultLine)
