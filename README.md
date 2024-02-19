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

**Pre-Requisite:**

Open [ChatGPT](https://chat.openai.com/) and navigate to your account settings.

Click "Data Controls and then "Export" under "Export data".

For help, run:

    chatgpt-to-sqlite --help

You can also use:

    python -m chatgpt_to_sqlite --help

Export ChatGPT data into a SQLite Data:

    chatgpt-to-sqlite path/to/chatGPT_conversations.json chatgpt.db

**Database Schema:**

    CREATE TABLE [conversations] (
        [chat_id] TEXT PRIMARY KEY,
        [title] TEXT,
        [create_time] TEXT,
        [update_time] TEXT
    );
    CREATE TABLE "messages" (
        [message_id] TEXT PRIMARY KEY,
        [sender] TEXT,
        [create_time] TEXT,
        [status] TEXT,
        [weight] FLOAT,
        [text] TEXT,
        [model] TEXT,
        [chat_id] TEXT REFERENCES [conversations]([chat_id])
    );

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd chatgpt-to-sqlite
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
