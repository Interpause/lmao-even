import { useState } from 'react';
import { Hash, Lock, RefreshCw, User, Users, ChevronDown, ChevronUp } from 'lucide-react';

interface MessageReference {
  message_id: string;
  ref_type: 'parent' | 'reply';
}

interface NormalizedMessage {
  message_id: string;
  conversation_id: string;
  text: string;
  user: string;
  timestamp: string;
  ref_message_ids: MessageReference[];
}

interface Conversation {
  id: string;
  name?: string;
  is_channel?: boolean;
  is_group?: boolean;
  is_im?: boolean;
  is_mpim?: boolean;
  is_private?: boolean;
  is_member?: boolean;
  num_members?: number;
  user?: string;
}

interface ConversationsResponse {
  conversations: Conversation[];
  count: number;
}

interface MessagesResponse {
  messages: NormalizedMessage[];
  count: number;
}

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedConversations, setExpandedConversations] = useState<Set<string>>(new Set());
  const [conversationMessages, setConversationMessages] = useState<Record<string, NormalizedMessage[]>>({});
  const [loadingMessages, setLoadingMessages] = useState<Set<string>>(new Set());

  const fetchChannels = async () => {
    setLoading(true);
    setError(null);

    try {
      const apiUrl = `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/slack-channels`;

      const res = await fetch(apiUrl, {
        headers: {
          'Authorization': `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}`,
        },
      });

      if (!res.ok) {
        throw new Error('Failed to fetch channels');
      }

      const data: ConversationsResponse = await res.json();
      setConversations(data.conversations);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
      console.error('Error fetching channels:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchMessages = async (conversationId: string) => {
    if (conversationMessages[conversationId]) return;

    setLoadingMessages((prev) => new Set(prev).add(conversationId));

    try {
      const apiUrl = `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/slack-channels?channel_id=${conversationId}`;

      const res = await fetch(apiUrl, {
        headers: {
          'Authorization': `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}`,
        },
      });

      if (!res.ok) {
        throw new Error('Failed to fetch messages');
      }

      const data: MessagesResponse = await res.json();
      setConversationMessages((prev) => ({
        ...prev,
        [conversationId]: data.messages,
      }));
    } catch (err) {
      console.error('Error fetching messages:', err);
    } finally {
      setLoadingMessages((prev) => {
        const next = new Set(prev);
        next.delete(conversationId);
        return next;
      });
    }
  };

  const toggleConversation = (conversationId: string) => {
    const isExpanded = expandedConversations.has(conversationId);

    if (!isExpanded) {
      fetchMessages(conversationId);
      setExpandedConversations((prev) => new Set(prev).add(conversationId));
    } else {
      setExpandedConversations((prev) => {
        const next = new Set(prev);
        next.delete(conversationId);
        return next;
      });
    }
  };

  const getParentId = (message: NormalizedMessage): string | null => {
    const parentRef = message.ref_message_ids.find((ref) => ref.ref_type === 'parent');
    return parentRef?.message_id || null;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="max-w-6xl mx-auto p-8">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="bg-gradient-to-r from-slate-800 to-slate-700 px-8 py-6">
            <h1 className="text-3xl font-bold text-white">
              Slack Conversations
            </h1>
            <p className="text-slate-300 mt-1">
              View all conversations from your Slack workspace
            </p>
          </div>

          <div className="p-8">
            <div className="flex items-center justify-between mb-6">
              <div className="text-sm text-slate-600">
                {conversations.length > 0 && (
                  <span className="font-medium">
                    {conversations.length} conversation{conversations.length !== 1 ? 's' : ''} found
                  </span>
                )}
              </div>

              <button
                onClick={fetchChannels}
                disabled={loading}
                className="flex items-center gap-2 px-4 py-2 bg-slate-800 text-white rounded-lg hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                {loading ? 'Loading...' : 'Refresh Conversations'}
              </button>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <p className="text-red-800 text-sm">
                  <strong>Error:</strong> {error}
                </p>
              </div>
            )}

            {conversations.length === 0 && !loading && !error && (
              <div className="text-center py-12">
                <Hash className="w-16 h-16 text-slate-300 mx-auto mb-4" />
                <p className="text-slate-600 text-lg mb-2">No conversations loaded</p>
                <p className="text-slate-500 text-sm">
                  Click "Refresh Conversations" to load all Slack conversations
                </p>
              </div>
            )}

            {conversations.length > 0 && (
              <div className="grid gap-3">
                {conversations.map((conv) => {
                  const getIcon = () => {
                    if (conv.is_im) return <User className="w-5 h-5 text-slate-500 flex-shrink-0" />;
                    if (conv.is_mpim) return <Users className="w-5 h-5 text-slate-500 flex-shrink-0" />;
                    if (conv.is_private) return <Lock className="w-5 h-5 text-slate-500 flex-shrink-0" />;
                    return <Hash className="w-5 h-5 text-slate-500 flex-shrink-0" />;
                  };

                  const getType = () => {
                    if (conv.is_im) return 'Direct Message';
                    if (conv.is_mpim) return 'Group DM';
                    if (conv.is_private) return 'Private Channel';
                    return 'Public Channel';
                  };

                  const getName = () => {
                    if (conv.name) return conv.name;
                    if (conv.is_im) return 'Direct Message';
                    if (conv.is_mpim) return 'Group Message';
                    return conv.id;
                  };

                  const isExpanded = expandedConversations.has(conv.id);
                  const messages = conversationMessages[conv.id] || [];
                  const isLoadingMessages = loadingMessages.has(conv.id);

                  return (
                    <div key={conv.id} className="border border-slate-200 rounded-lg overflow-hidden">
                      <div
                        onClick={() => toggleConversation(conv.id)}
                        className="flex items-center justify-between p-4 bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer"
                      >
                        <div className="flex items-center gap-3">
                          {getIcon()}

                          <div>
                            <h3 className="font-semibold text-slate-800">
                              {getName()}
                            </h3>
                            <div className="flex items-center gap-3 mt-1">
                              <span className="text-xs text-slate-500">
                                {getType()}
                              </span>
                              {conv.num_members !== undefined && (
                                <span className="text-xs text-slate-500">
                                  {conv.num_members} member{conv.num_members !== 1 ? 's' : ''}
                                </span>
                              )}
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center gap-2">
                          {conv.is_member && (
                            <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
                              Joined
                            </span>
                          )}
                          {isExpanded ? (
                            <ChevronUp className="w-5 h-5 text-slate-500" />
                          ) : (
                            <ChevronDown className="w-5 h-5 text-slate-500" />
                          )}
                        </div>
                      </div>

                      {isExpanded && (
                        <div className="bg-white border-t border-slate-200">
                          {isLoadingMessages ? (
                            <div className="p-4 text-center text-slate-500">
                              Loading messages...
                            </div>
                          ) : messages.length === 0 ? (
                            <div className="p-4 text-center text-slate-500">
                              No messages found
                            </div>
                          ) : (
                            <div className="max-h-96 overflow-y-auto">
                              {messages.map((msg) => {
                                const parentId = getParentId(msg);
                                const isReply = parentId !== null;

                                return (
                                  <div
                                    key={msg.message_id}
                                    className={`p-4 border-b border-slate-100 hover:bg-slate-50 ${
                                      isReply ? 'pl-8 bg-slate-50/50' : ''
                                    }`}
                                  >
                                    <div className="flex items-start gap-2 mb-1">
                                      <span className="text-xs font-medium text-slate-700">
                                        {msg.user || 'Unknown'}
                                      </span>
                                      <span className="text-xs text-slate-400">
                                        {new Date(parseFloat(msg.timestamp) * 1000).toLocaleString()}
                                      </span>
                                      {isReply && (
                                        <span className="text-xs text-blue-600">↳ Reply</span>
                                      )}
                                    </div>
                                    <p className="text-sm text-slate-800 whitespace-pre-wrap">
                                      {msg.text}
                                    </p>
                                  </div>
                                );
                              })}
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
