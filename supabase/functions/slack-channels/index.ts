/**
 * Slack Conversations Edge Function
 *
 * Retrieves all conversations from a Slack workspace including:
 * - Public channels
 * - Private channels
 * - Direct messages (DMs)
 * - Multi-party direct messages (MPDMs)
 */
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { getConversations } from "./slack.ts";
import { corsPreflightResponse, jsonResponse } from "./response.ts";

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return corsPreflightResponse();
  }

  const slackToken = Deno.env.get("SLACK_USER_TOKEN");

  if (!slackToken) {
    return jsonResponse({ error: "SLACK_USER_TOKEN not configured" }, 500);
  }

  const conversations = await getConversations(slackToken);

  return jsonResponse({
    conversations,
    count: conversations.length,
  });
});