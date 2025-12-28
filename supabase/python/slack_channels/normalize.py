from __future__ import annotations

"""Message normalization helpers mirroring the original TypeScript implementation."""

from typing import Literal, Sequence, TypedDict


class MessageReference(TypedDict):
    message_id: str
    ref_type: Literal["parent", "reply"]


class NormalizedMessage(TypedDict):
    message_id: str
    conversation_id: str
    text: str
    user: str
    timestamp: str
    ref_message_ids: list[MessageReference]


class SlackMessage(TypedDict, total=False):
    ts: str
    thread_ts: str
    text: str
    user: str


def normalize_messages(
    messages: Sequence[SlackMessage],
    conversation_id: str,
) -> list[NormalizedMessage]:
    """Normalize Slack history responses into a flat, reference-friendly shape."""

    normalized: list[NormalizedMessage] = []

    for message in messages:
        ts = message.get("ts")
        if not ts:
            # Slack history responses always include ts, but we defensively skip invalid rows.
            continue

        ref_message_ids: list[MessageReference] = []
        thread_ts = message.get("thread_ts")
        if thread_ts and thread_ts != ts:
            ref_message_ids.append({"message_id": thread_ts, "ref_type": "parent"})

        normalized.append(
            {
                "message_id": ts,
                "conversation_id": conversation_id,
                "text": message.get("text", ""),
                "user": message.get("user", ""),
                "timestamp": ts,
                "ref_message_ids": ref_message_ids,
            }
        )

    return normalized


def get_parent_id(message: NormalizedMessage) -> str | None:
    """Return the parent message ID when present."""

    for reference in message["ref_message_ids"]:
        if reference["ref_type"] == "parent":
            return reference["message_id"]
    return None


def get_reply_ids(message: NormalizedMessage, all_messages: Sequence[NormalizedMessage]) -> list[str]:
    """Return the message IDs that reference the provided message as their parent."""

    target_id = message["message_id"]
    return [msg["message_id"] for msg in all_messages if get_parent_id(msg) == target_id]
