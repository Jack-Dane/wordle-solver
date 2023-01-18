from setuptools import setup, find_packages

setup(
    name="wordle",
    version="0.0.3",
    install_requires=[
        "selenium",
        "sqlalchemy",
        "docker",
        "requests",
        "sqlalchemy",
        "pysocks",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "wordleRun=wordle.main:main",
            "createTables=wordle.models.results:createTables"
        ]
    }
)
