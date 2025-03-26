import sqlite3
from datetime import datetime

import pytest

# -- FIXTURE: Load conversations and messages into usable Python dicts --


@pytest.fixture
def get_most_active_conversation_with_messages(db_path="chatgpt.db", message_limit=10):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the chat_id of the conversation with most messages
    cursor.execute(
        """
        SELECT c.chat_id, c.title, c.create_time, c.update_time, COUNT(m.message_id) as msg_count
        FROM conversations c
        JOIN messages m ON c.chat_id = m.chat_id
        GROUP BY c.chat_id
        ORDER BY msg_count DESC
        LIMIT 1
    """
    )
    top_convo = cursor.fetchone()

    if not top_convo:
        print("No conversations found.")
        return None

    chat_id = top_convo[0]
    conversation = {
        "chat_id": chat_id,
        "title": top_convo[1],
        "create_time": top_convo[2],
        "update_time": top_convo[3],
        "messages": [],
    }

    # Get messages for that conversation
    cursor.execute(
        """
        SELECT message_id, sender, create_time, status, weight, text, model
        FROM messages
        WHERE chat_id = ?
        ORDER BY create_time
        LIMIT ?
    """,
        (chat_id, message_limit),
    )

    messages = cursor.fetchall()

    for msg in messages:
        conversation["messages"].append(
            {
                "message_id": msg[0],
                "sender": msg[1],
                "create_time": msg[2],
                "status": msg[3],
                "weight": msg[4],
                "text": msg[5],
                "model": msg[6],
            }
        )

    conn.close()
    return conversation


def test_preview_documents(get_most_active_conversation_with_messages):
    documents = get_most_active_conversation_with_messages
    if not documents:
        print("No conversations found.")
        return

    convo = documents
    print(f"\n📘 Conversation: {convo['title']}")
    print("-" * 60)
    for msg in convo["messages"]:
        sender = msg["sender"]
        text = msg["text"]
        print(f"[{sender.upper()}]: {text}\n")


def test_sanity_check_db():
    db_path = "chatgpt.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM conversations")
    conv_count = cursor.fetchone()[0]
    print(f"🗂️  Total conversations: {conv_count}")

    cursor.execute("SELECT COUNT(*) FROM messages")
    msg_count = cursor.fetchone()[0]
    print(f"💬 Total messages: {msg_count}")

    cursor.execute(
        """
        SELECT c.title, c.chat_id, COUNT(m.message_id) as message_count
        FROM conversations c
        LEFT JOIN messages m ON c.chat_id = m.chat_id
        GROUP BY c.chat_id
        ORDER BY message_count DESC
        LIMIT 20
    """
    )
    rows = cursor.fetchall()
    print("\n📊 Top 20 conversations by message count:")
    for title, chat_id, count in rows:
        print(f"   - {title[:40]:40} | ID: {chat_id[:8]}... | {count} messages")

    conn.close()


def test_sanity_check_db():
    db_path = "chatgpt.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM conversations")
    conv_count = cursor.fetchone()[0]
    print(f"🗂️  Total conversations: {conv_count}")

    cursor.execute("SELECT COUNT(*) FROM messages LIMIT(10)")
    msg_count = cursor.fetchone()[0]
    print(f"💬 Total messages: {msg_count}")

    cursor.execute(
        """
        SELECT c.title, c.chat_id, COUNT(m.message_id) as message_count
        FROM conversations c
        LEFT JOIN messages m ON c.chat_id = m.chat_id
        GROUP BY c.chat_id
        ORDER BY message_count DESC
        LIMIT 20
    """
    )
    rows = cursor.fetchall()
    print("\n📊 Top 20 conversations by message count:")
    for title, chat_id, count in rows:
        print(f"   - {title[:40]:40} | ID: {chat_id[:8]}... | {count} messages")

    conn.close()
