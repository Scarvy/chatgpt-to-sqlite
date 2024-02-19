import json

import click
import sqlite_utils
from click_default_group import DefaultGroup
from funcy import omit

from chatgpt_to_sqlite import utils


@click.group(cls=DefaultGroup, default="export", default_if_no_args=True)
@click.version_option()
def cli():
    "Import ChatGPT conversations into a SQLite database"


@cli.command(name="export")
@click.argument(
    "filename",
    type=click.File(),
)
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.option(
    "-n",
    "--num",
    type=int,
    default=None,
    help="Number of conversations to load",
)
def export(filename, db_path, num):
    """Import ChatGPT conversations into a SQlite database."""
    data = json.load(filename)[:num] if num else json.load(filename)
    click.echo(f"Loaded {len(data)} conversations.")

    db = sqlite_utils.Database(db_path)

    conversations = utils.load_documents(data)

    # All Chat details except messages
    convo_details = [omit(convo, "messages") for convo in conversations]

    chatgpt_table = db.table("conversations")
    chatgpt_table.upsert_all(convo_details, pk="chat_id")

    # Store all chat messages
    all_messages = []
    for convo in conversations:
        messages = convo["messages"]
        for message in messages:
            all_messages.append(message)

    # Build messages tables
    messages_table = db.table("messages")
    messages_table.upsert_all(messages, pk="message_id")
    messages_table.add_foreign_key("chat_id", "conversations", "chat_id", ignore=True)
