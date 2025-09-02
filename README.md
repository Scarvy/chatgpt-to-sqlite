# chatgpt-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/chatgpt-to-sqlite.svg)](https://pypi.org/project/chatgpt-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/Scarvy/chatgpt-to-sqlite?include_prereleases&label=changelog)](https://github.com/Scarvy/chatgpt-to-sqlite/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/Scarvy/chatgpt-to-sqlite/blob/master/LICENSE)

Import ChatGPT conversations into a SQLite database

## Installation

The easiest way to use this tool is to install it using `uv`:

    uvx chatgpt-to-sqlite conversations.json chat.db

Or, you can install it as a tool:

    uv tool install chatgpt-to-sqlite

## Usage

**Pre-Requisite:**

Open [ChatGPT](https://chat.openai.com/) and navigate to your account settings.

Click "Data Controls and then "Export" under "Export data".

For help, run:

    chatgpt-to-sqlite --help

You can also use:

    chatgpt_to_sqlite --help

Export ChatGPT data into a SQLite Data:

    chatgpt-to-sqlite path/to/chatGPT_conversations.json chat.db

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
    uv sync --dev

To run the tests:

    pytest
