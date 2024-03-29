![Tests](https://github.com/Jack-Dane/wordle-solver/actions/workflows/run-tests.yml/badge.svg)

# wordle-solver
A web driver application that will solve Wordle. 

## Prerequisite
* Has only been tested on a linux machine. 
* Needs to have vinagre installed. `apt install vinagre`

## How to setup
1. Clone the repository `git clone git@github.com:Jack-Dane/worlde-solver.git`
2. Change into the created directory `cd wordle-solver`
3. Create a new virtual environment for the project `python3 -m venv venv`
4. Use the new created virtual environment `source venv/bin/activate`
5. Install wheel and setuptools `pip install wheel setuptools`
6. Install the relevant packages `pip install -r requirements.txt`

## Example
![Wordle](assets/wordle.gif)

## How to run
There are two modes which can be run, one mode is a cheat mode which will get the correct 
answer straight away. The other way will work out the correct answer by reading the reducing 
a wordlist based on the results of the words guessed. 

To start wordle solver with a cheat method:
```
wordleRun -C
```

To start the method without the cheat mode:
```
wordleRun
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

You can also run with a VNC viewer argument for your machine to automatically open a window to view the Chrome application running. 
```
wordleRun --VNC
```
You could also view from a browser `http://localhost:7900/?autoconnect=1&resize=scale&password=secret` when running. It may take a couple of seconds after running 
the command for the page to be accessible. 

Use `wordleRun --help` to see all commands.

## WebDriver
The application creates a selenium container with a chrome browser installed. It would be better to first pull this image: 
`docker pull selenium/standalone-chrome`.

## Prerequisite
1. That docker is installed onto the system you are trying to run the wordle solver on.
2. If running with the VNC viewer option, the application expects that [vinagre](https://linux.die.net/man/1/vinagre) is installed on your machine. 
