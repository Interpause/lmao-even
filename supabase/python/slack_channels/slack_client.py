from __future__ import annotations

"""Thin wrappers around the Slack Web API using the official Python SDK."""

from typing import Any

from slack_sdk import WebClient

DEFAULT_MESSAGE_LIMIT = 100
DEFAULT_CONVERSATION_LIMIT = 1000


def _client(token: str) -> WebClient:
    return WebClient(token=token)


def get_conversations(token: str, *, limit: int = DEFAULT_CONVERSATION_LIMIT) -> list[dict[str, Any]]:
    """Return all accessible conversations (public, private, IM, and MPIM).

    Mirrors https://docs.slack.dev/tools/python-slack-sdk/web/#conversations
    """

    response = _client(token).conversations_list(
        types="public_channel,private_channel,mpim,im",
        exclude_archived=True,
        limit=limit,
    )
    return list(response.get("channels", []))


def get_messages(token: str, channel_id: str, *, limit: int = DEFAULT_MESSAGE_LIMIT) -> list[dict[str, Any]]:
    """Return recent messages for a conversation via conversations.history."""

    response = _client(token).conversations_history(channel=channel_id, limit=limit)
    return list(response.get("messages", []))
