# wordle-solver
A web driver application that will solve Wordle. 

## How to setup
1. Clone the repository `git clone git@github.com:Jack-Dane/worlde-solver.git`
2. Change into the created directory `cd wordle-solver`
3. Create a new virtual environment for the project `python3 -m venv venv`
4. Use the new created virtual environment `source venv/bin/activate`
5. Install the relevant packages `pip install -e .`

## How to run
There are two modes which can be run, one mode is a cheat mode which will get the correct 
answer straight away. The other way will work out the correct answer by reading the reducing 
a wordlist based on the results of the words guessed. 

To start wordle solver with a cheat method:
```
wordleRun -c
```

To start the method without the cheat mode:
```
wordleRsun
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

You can save results to a sqlite database using the `-LR` or `--logResult` argument. You first need
to run the `createTables` command first to create the database and tables. 

## WebDriver
The application creates a selenium container with a chrome browser installed. It would be better to first pull this image: 
`docker pull selenium/standalone-chrome`

## Prerequisite
1. That docker is installed onto the system you are trying to run the wordle solver on.
