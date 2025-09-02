from datetime import datetime
from typing import Optional


def convert_timestamp(timestamp: float | None) -> datetime | None:
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp)


# source https://github.com/duarteocarmo/mistral-doc/blob/1f909bb4e23c4ae487890072192722c2e86da1f3/process_gpt_export.py#L16
def concatenate_rows(message: dict, chat_id: str) -> Optional[dict]:
    if not message:
        return None

    sender = message.get("author", {}).get("role", "unknown")
    content = message.get("content", {})
    parts = content.get("parts")

    # Make sure parts is a list with at least one valid string
    if not isinstance(parts, list) or not parts:
        print(f"SKIPPED: NO PARTS: {chat_id}")
        return None

    # Grab the first non-empty string part
    first_valid_part = next(
        (p for p in parts if isinstance(p, str) and p.strip()), None
    )
    if not first_valid_part:
        return None

    metadata = message.get("metadata", {})
    is_user_system_message = metadata.get("is_user_system_message", False)

    if is_user_system_message:
        context_data = metadata.get("user_context_message_data", {})
        user_about_message = context_data.get("about_user_message", "")
        about_model_message = context_data.get("about_model_message", "")
        total_system_message = (
            f"ABOUT YOU:\n{about_model_message}\n\n"
            f"ABOUT YOUR USER:\n{user_about_message}\n\n"
            f"FIRST MESSAGE FROM THE USER:\n\n"
        )
        return {
            "message_id": message.get("id"),
            "sender": "system",
            "create_time": convert_timestamp(message.get("create_time")),
            "status": message.get("status"),
            "weight": message.get("weight"),
            "text": total_system_message,
            "model": None,
            "chat_id": chat_id,
        }

    model = metadata.get("model_slug")

    return {
        "message_id": message.get("id"),
        "sender": sender,
        "create_time": convert_timestamp(message.get("create_time")),
        "status": message.get("status"),
        "weight": message.get("weight"),
        "text": first_valid_part.strip(),
        "model": model,
        "chat_id": chat_id,
    }


def walk_conversation(mapping: dict, current_node_id: str) -> list[dict]:
    """Walks the mapping from current_node back to root and returns messages in order."""
    ordered_nodes = []

    while current_node_id:
        node = mapping.get(current_node_id)
        if not node:
            break
        message = node.get("message")
        if message:
            ordered_nodes.append((message, current_node_id))
        current_node_id = node.get("parent")

    # Reverse to get oldest → newest
    return list(reversed(ordered_nodes))


def load_documents(data: dict) -> list[dict]:
    documents = []
    for d in data:
        mapping = d["mapping"]
        current_node = d.get("current_node")
        path = walk_conversation(mapping, current_node)

        messages = [concatenate_rows(message, d["id"]) for message, _ in path]
        messages = [m for m in messages if m]

        document = {
            "chat_id": d["id"],
            "title": d["title"],
            "create_time": convert_timestamp(d["create_time"]),
            "update_time": convert_timestamp(d["update_time"]),
            "messages": messages,
        }
        documents.append(document)
    return documents
