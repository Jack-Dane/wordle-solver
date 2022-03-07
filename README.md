# wordle-solver
A web driver application that will solve Wordle. 

## How to setup
1. Clone the repository `git clone git@github.com:Jack-Dane/worlde-solver.git`
2. Change into the created directory `cd wordle-solver`
3. Create a new virtual environment for the project `python3 -m venv venv`
4. Use the new created virtual environment `source venv/bin/activate`
5. Install the setup.py file `python3 setup.py install`

## How to run
There are two modes which can be run, one mode is a cheat mode which will get the correct 
answer straight away. The other way will work out the correct answer by reading the reducing 
a wordlist based on the results of the words guessed. 

To start wordle solver with a cheat method:
```
worldRun -c
```

To start the method without the cheat mode:
```
worldRun
```

This will run the wordle with a random word from the wordlist. You can add another argument onto
the command which will allow you to select the starting word. This is an example of using "audio" 
as the first guess word
```
wordleRun -FG audio
```
or 
```
wordleRun --firstGuess audio
```

## WebDriver
This implementation specifically uses a Chrome webdriver to run wordle solver application, the driver
in the repository is currently on version 98. If your browser is on another version you can download 
other version from https://chromedriver.chromium.org/home and replace the file `world-solve/drivers/chromedriver`
with the new driver you downloaded. 
