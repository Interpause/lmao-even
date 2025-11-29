interface MessageReference {
  message_id: string;
  ref_type: "parent" | "reply";
}

interface NormalizedMessage {
  message_id: string;
  conversation_id: string;
  text: string;
  user: string;
  timestamp: string;
  ref_message_ids: MessageReference[];
}

interface SlackMessage {
  ts: string;
  thread_ts?: string;
  text?: string;
  user?: string;
  [key: string]: unknown;
}

/**
 * Normalizes Slack messages into a flexible structure with ref_message_ids
 *
 * For Slack:
 * - If message has thread_ts and ts !== thread_ts, it's a reply (has parent reference)
 * - If message has thread_ts and ts === thread_ts, it's a parent message (no references yet)
 * - If message has no thread_ts, it's an unthreaded message (no references)
 */
export function normalizeMessages(
  messages: SlackMessage[],
  conversationId: string
): NormalizedMessage[] {
  return messages.map((msg) => {
    const refMessageIds: MessageReference[] = [];

    if (msg.thread_ts && msg.ts !== msg.thread_ts) {
      refMessageIds.push({
        message_id: msg.thread_ts,
        ref_type: "parent",
      });
    }

    return {
      message_id: msg.ts,
      conversation_id: conversationId,
      text: msg.text || "",
      user: msg.user || "",
      timestamp: msg.ts,
      ref_message_ids: refMessageIds,
    };
  });
}

/**
 * Derived property getter: Gets parent message ID from ref_message_ids
 */
export function getParentId(message: NormalizedMessage): string | null {
  const parentRef = message.ref_message_ids.find((ref) => ref.ref_type === "parent");
  return parentRef?.message_id || null;
}

/**
 * Derived property getter: Gets all reply IDs for a given message
 * Note: This requires the full message list to compute
 */
export function getReplyIds(
  message: NormalizedMessage,
  allMessages: NormalizedMessage[]
): string[] {
  return allMessages
    .filter((msg) => getParentId(msg) === message.message_id)
    .map((msg) => msg.message_id);
}