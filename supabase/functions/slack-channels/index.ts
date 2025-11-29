/**
 * Slack Conversations Edge Function
 *
 * Retrieves all conversations from a Slack workspace including:
 * - Public channels
 * - Private channels
 * - Direct messages (DMs)
 * - Multi-party direct messages (MPDMs)
 *
 * Also supports fetching messages from a specific conversation
 */
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { getConversations, getMessages } from "./slack.ts";
import { normalizeMessages } from "./normalize.ts";
import { corsPreflightResponse, jsonResponse } from "./response.ts";

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return corsPreflightResponse();
  }

  const slackToken = Deno.env.get("SLACK_USER_TOKEN");

  if (!slackToken) {
    return jsonResponse({ error: "SLACK_USER_TOKEN not configured" }, 500);
  }

  const url = new URL(req.url);
  const channelId = url.searchParams.get("channel_id");

  if (channelId) {
    const messages = await getMessages(slackToken, channelId);
    const normalizedMessages = normalizeMessages(messages, channelId);

    return jsonResponse({
      messages: normalizedMessages,
      count: normalizedMessages.length,
    });
  }

  const conversations = await getConversations(slackToken);

  return jsonResponse({
    conversations,
    count: conversations.length,
  });
});