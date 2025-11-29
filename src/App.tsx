import { useState } from 'react';
import { Hash, Lock, RefreshCw, User, Users } from 'lucide-react';

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

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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

                  return (
                    <div
                      key={conv.id}
                      className="flex items-center justify-between p-4 bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors border border-slate-200"
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

                      {conv.is_member && (
                        <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
                          Joined
                        </span>
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
