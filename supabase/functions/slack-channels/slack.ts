import { WebClient } from "npm:@slack/web-api@7.13.0";

/**
 * Fetches all conversations from Slack workspace
 * Includes public channels, private channels, direct messages, and multi-party direct messages
 */
export async function getConversations(token: string) {
  const client = new WebClient(token);

  const result = await client.conversations.list({
    types: "public_channel,private_channel,mpim,im",
    exclude_archived: true,
    limit: 1000,
  });

  return result.channels || [];
}