from __future__ import annotations

"""FastAPI application that mirrors the original Slack Edge Function."""

import os
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from slack_sdk.errors import SlackApiError

from .constants import CORS_CONFIG
from .normalize import normalize_messages
from .slack_client import DEFAULT_MESSAGE_LIMIT, get_conversations, get_messages

app = FastAPI(title="Slack Conversations Service", version="0.1.0")
app.add_middleware(CORSMiddleware, **CORS_CONFIG)


def _require_token() -> str:
    token = os.getenv("SLACK_USER_TOKEN")
    if not token:
        raise HTTPException(status_code=500, detail={"error": "SLACK_USER_TOKEN not configured"})
    return token


def _raise_slack_error(error: SlackApiError) -> None:
    response = getattr(error, "response", None)
    status_code = getattr(response, "status_code", None) or 502
    detail: dict[str, Any] = {"error": "Slack API request failed"}

    if response is not None:
        slack_error = response.get("error")
        if slack_error:
            detail["slack_error"] = slack_error

    raise HTTPException(status_code=status_code, detail=detail)


@app.get("/slack/conversations")
def conversations_handler(
    channel_id: str | None = Query(
        default=None,
        description="When provided, returns normalized messages for the given channel.",
    ),
    limit: int = Query(
        default=DEFAULT_MESSAGE_LIMIT,
        ge=1,
        le=1000,
        description="Max messages to fetch when channel_id is supplied.",
    ),
):
    """Return either the workspace's conversations list or a channel's normalized messages."""

    token = _require_token()

    if channel_id:
        try:
            messages = get_messages(token, channel_id, limit=limit)
        except SlackApiError as error:
            _raise_slack_error(error)

        normalized = normalize_messages(messages, channel_id)
        return {"messages": normalized, "count": len(normalized)}

    try:
        conversations = get_conversations(token)
    except SlackApiError as error:
        _raise_slack_error(error)

    return {"conversations": conversations, "count": len(conversations)}
