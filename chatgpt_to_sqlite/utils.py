from datetime import UTC, datetime
from typing import Optional


def convert_timestamp(timestamp: float | None) -> datetime | None:
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp, tz=UTC)


# source https://github.com/duarteocarmo/mistral-doc/blob/1f909bb4e23c4ae487890072192722c2e86da1f3/process_gpt_export.py#L16
def concatenate_rows(message: dict, chat_id: str) -> Optional[dict]:
    if not message:
        return None

    # sender (user, assistant, and system)
    sender = message["author"]["role"] if message["author"] else "unknown"

    if "parts" not in message["content"]:
        return None

    metadata = message.get("metadata", {})
    is_user_system_message = metadata.get("is_user_system_message", False)

    # System message
    if is_user_system_message is True:
        user_about_message = metadata.get("user_context_message_data", "").get(
            "about_user_message", ""
        )
        about_model_message = metadata.get("user_context_message_data", "").get(
            "about_model_message", ""
        )
        total_system_message = f"ABOUT YOU:\n{about_model_message}\n\nABOUT YOUR USER:\n{user_about_message}\n\nFIRST MESSAGE FROM THE USER:\n\n"
        return {
            "message_id": message["id"],
            "sender": "system",
            "create_time": convert_timestamp(message["create_time"]),
            "status": message["status"],
            "weight": message["weight"],
            "text": total_system_message,
            "model": None,
            "chat_id": chat_id,
        }

    # User and assistant messages
    text = message["content"]["parts"][0]

    if text == "":
        return None

    model = message["metadata"].get("model_slug")

    return {
        "message_id": message["id"],
        "sender": sender,
        "create_time": convert_timestamp(message["create_time"]),
        "status": message["status"],
        "weight": message["weight"],
        "text": text,
        "model": model,
        "chat_id": chat_id,
    }


# source: https://github.com/duarteocarmo/mistral-doc/blob/1f909bb4e23c4ae487890072192722c2e86da1f3/process_gpt_export.py#L44
def load_documents(data: dict) -> list[list[dict]]:
    documents = []
    for d in data:
        messages = d["mapping"]
        messages = [
            concatenate_rows(messages[key]["message"], d["id"])
            for _, key in enumerate(messages)
        ]
        messages = [message for message in messages if message]
        document = {
            "chat_id": d["id"],
            "title": d["title"],
            "create_time": convert_timestamp(d["create_time"]),
            "update_time": convert_timestamp(d["update_time"]),
            "messages": messages,
        }
        documents.append(document)
    return documents
