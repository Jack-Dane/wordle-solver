
import os
from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine, insert
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


def getEngine():
    return create_engine(f"sqlite:///{os.getcwd()}/wordleResults.db")


class Result(Base):
    __tablename__ = "Result"

    id = Column(Integer, primary_key=True)
    numberOfGuesses = Column(Integer)
    algorithmType = Column(String)
    runDateTime = Column(DateTime)
    firstGuess = Column(String)
    correctAnswer = Column(String)


def insertResult(numberOfGuesses, guessingAlgorithm, runDateTime, firstGuess, correctAnswer):
    with Session(getEngine()) as session:
        result = Result(
            numberOfGuesses=numberOfGuesses, algorithmType=guessingAlgorithm,
            runDateTime=runDateTime, firstGuess=firstGuess, correctAnswer=correctAnswer
        )

        session.add(result)

        session.commit()


def createTables():
    engine = getEngine()
    Base.metadata.create_all(engine)
