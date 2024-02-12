# chatgpt-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/chatgpt-to-sqlite.svg)](https://pypi.org/project/chatgpt-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/Scarvy/chatgpt-to-sqlite?include_prereleases&label=changelog)](https://github.com/Scarvy/chatgpt-to-sqlite/releases)
[![Tests](https://github.com/Scarvy/chatgpt-to-sqlite/actions/workflows/test.yml/badge.svg)](https://github.com/Scarvy/chatgpt-to-sqlite/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/Scarvy/chatgpt-to-sqlite/blob/master/LICENSE)

Import ChatGPT conversations into a SQLite database

## Installation

Install this tool using `pip`:

    pip install chatgpt-to-sqlite

## Usage

For help, run:

    chatgpt-to-sqlite --help

You can also use:

    python -m chatgpt_to_sqlite --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd chatgpt-to-sqlite
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
