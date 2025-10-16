import { useState, useEffect } from 'react';
import { Brain, Sparkles, TrendingUp, MessageSquare, CheckCircle, XCircle, Clock, Eye, ThumbsUp, ThumbsDown } from 'lucide-react';
import api from '@/lib/api';

const AGENT_TYPES = {
  narrative: {
    name: 'Narrative Architect',
    icon: Brain,
    color: 'blue',
    description: 'Analyzes public discourse and suggests narrative frameworks'
  },
  content: {
    name: 'Content Synthesizer',
    icon: Sparkles,
    color: 'purple',
    description: 'Generates educational explainer content'
  },
  distribution: {
    name: 'Distribution Optimizer',
    icon: TrendingUp,
    color: 'green',
    description: 'Recommends optimal posting times and channels'
  },
  feedback: {
    name: 'Feedback Intelligence',
    icon: MessageSquare,
    color: 'orange',
    description: 'Analyzes engagement data and flags misinformation'
  }
};

export default function AIAgentsPage() {
  const [recommendations, setRecommendations] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showRequestModal, setShowRequestModal] = useState(false);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [selectedRecommendation, setSelectedRecommendation] = useState(null);
  const [filterAgent, setFilterAgent] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [requestForm, setRequestForm] = useState({
    campaign_id: '',
    agent_type: 'narrative',
    prompt: ''
  });
  const [reviewForm, setReviewForm] = useState({
    status: 'approved',
    review_notes: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [requesting, setRequesting] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [recsRes, campaignsRes] = await Promise.all([
        api.get('/api/ai/recommendations'),
        api.get('/api/campaigns')
      ]);
      setRecommendations(recsRes.data.recommendations || []);
      setCampaigns(campaignsRes.data.campaigns || []);
    } catch (err) {
      setError('Failed to load data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRequestRecommendation = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setRequesting(true);

    try {
      await api.post('/api/ai/recommendations', requestForm);
      setSuccess('AI recommendation requested successfully');
      fetchData();
      handleCloseRequestModal();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to request recommendation');
    } finally {
      setRequesting(false);
    }
  };

  const handleReviewRecommendation = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await api.put(`/api/ai/recommendations/${selectedRecommendation.id}/review`, reviewForm);
      setSuccess('Recommendation reviewed successfully');
      fetchData();
      handleCloseReviewModal();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to review recommendation');
    }
  };

  const handleCloseRequestModal = () => {
    setShowRequestModal(false);
    setRequestForm({
      campaign_id: '',
      agent_type: 'narrative',
      prompt: ''
    });
  };

  const handleCloseReviewModal = () => {
    setShowReviewModal(false);
    setSelectedRecommendation(null);
    setReviewForm({
      status: 'approved',
      review_notes: ''
    });
  };

  const handleViewRecommendation = (rec) => {
    setSelectedRecommendation(rec);
    setReviewForm({
      status: rec.status === 'pending' ? 'approved' : rec.status,
      review_notes: rec.review_notes || ''
    });
    setShowReviewModal(true);
  };

  const filteredRecommendations = recommendations.filter(rec => {
    const matchesAgent = filterAgent === 'all' || rec.agent_type === filterAgent;
    const matchesStatus = filterStatus === 'all' || rec.status === filterStatus;
    return matchesAgent && matchesStatus;
  });

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { color: 'bg-yellow-100 text-yellow-800', icon: Clock, label: 'Pending Review' },
      approved: { color: 'bg-green-100 text-green-800', icon: CheckCircle, label: 'Approved' },
      rejected: { color: 'bg-red-100 text-red-800', icon: XCircle, label: 'Rejected' },
      implemented: { color: 'bg-blue-100 text-blue-800', icon: CheckCircle, label: 'Implemented' }
    };

    const config = statusConfig[status] || statusConfig.pending;
    const Icon = config.icon;

    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
        <Icon className="w-3 h-3 mr-1" />
        {config.label}
      </span>
    );
  };

  const getCampaignName = (campaignId) => {
    const campaign = campaigns.find(c => c.id === campaignId);
    return campaign ? campaign.name : 'Unknown Campaign';
  };

  const getAgentConfig = (type) => {
    return AGENT_TYPES[type] || AGENT_TYPES.narrative;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Agents</h1>
          <p className="mt-2 text-sm text-gray-600">
            Request AI recommendations and review generated content
          </p>
        </div>
        <button
          onClick={() => setShowRequestModal(true)}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
        >
          <Brain className="w-5 h-5 mr-2" />
          Request Recommendation
        </button>
      </div>

      {/* Alerts */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {success && (
        <div className="bg-green-50 border-l-4 border-green-400 p-4">
          <p className="text-sm text-green-700">{success}</p>
        </div>
      )}

      {/* AI Agents Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {Object.entries(AGENT_TYPES).map(([key, agent]) => {
          const Icon = agent.icon;
          const count = recommendations.filter(r => r.agent_type === key).length;
          return (
            <div key={key} className="bg-white rounded-lg shadow p-4 hover:shadow-lg transition-shadow">
              <div className={`bg-${agent.color}-100 rounded-lg p-3 w-fit mb-3`}>
                <Icon className={`w-6 h-6 text-${agent.color}-600`} />
              </div>
              <h3 className="font-semibold text-lg mb-1">{agent.name}</h3>
              <p className="text-sm text-gray-600 mb-2">{agent.description}</p>
              <p className="text-xs text-gray-500">{count} recommendations</p>
            </div>
          );
        })}
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <select
            value={filterAgent}
            onChange={(e) => setFilterAgent(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Agents</option>
            <option value="narrative">Narrative Architect</option>
            <option value="content">Content Synthesizer</option>
            <option value="distribution">Distribution Optimizer</option>
            <option value="feedback">Feedback Intelligence</option>
          </select>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Statuses</option>
            <option value="pending">Pending Review</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
            <option value="implemented">Implemented</option>
          </select>
        </div>
      </div>

      {/* Recommendations List */}
      <div className="space-y-4">
        {filteredRecommendations.map((rec) => {
          const agentConfig = getAgentConfig(rec.agent_type);
          const Icon = agentConfig.icon;
          
          return (
            <div
              key={rec.id}
              className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow duration-200 overflow-hidden"
            >
              <div className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className={`bg-${agentConfig.color}-100 rounded-lg p-2`}>
                        <Icon className={`w-5 h-5 text-${agentConfig.color}-600`} />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{agentConfig.name}</h3>
                        <p className="text-sm text-gray-500">{getCampaignName(rec.campaign_id)}</p>
                      </div>
                    </div>

                    <div className="ml-11 space-y-2">
                      {rec.recommendation_data && (
                        <div className="bg-gray-50 rounded-lg p-4">
                          <p className="text-sm text-gray-700 whitespace-pre-wrap">
                            {typeof rec.recommendation_data === 'string' 
                              ? rec.recommendation_data 
                              : JSON.stringify(rec.recommendation_data, null, 2)}
                          </p>
                        </div>
                      )}

                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span>Requested: {new Date(rec.created_at).toLocaleDateString()}</span>
                        {rec.reviewed_at && (
                          <span>Reviewed: {new Date(rec.reviewed_at).toLocaleDateString()}</span>
                        )}
                        {getStatusBadge(rec.status)}
                      </div>

                      {rec.review_notes && (
                        <div className="bg-blue-50 border-l-4 border-blue-400 p-3">
                          <p className="text-sm text-blue-700">
                            <span className="font-medium">Review Notes:</span> {rec.review_notes}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>

                  <button
                    onClick={() => handleViewRecommendation(rec)}
                    className="ml-4 inline-flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                  >
                    <Eye className="w-4 h-4 mr-2" />
                    {rec.status === 'pending' ? 'Review' : 'View'}
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {filteredRecommendations.length === 0 && (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <Brain className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No recommendations found</h3>
          <p className="mt-1 text-sm text-gray-500">
            {filterAgent !== 'all' || filterStatus !== 'all' 
              ? 'Try adjusting your filters' 
              : 'Request an AI recommendation to get started'}
          </p>
        </div>
      )}

      {/* Request Modal */}
      {showRequestModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center p-4">
          <div className="relative bg-white rounded-lg shadow-xl max-w-2xl w-full">
            <div className="border-b px-6 py-4">
              <h3 className="text-lg font-semibold text-gray-900">Request AI Recommendation</h3>
            </div>

            <form onSubmit={handleRequestRecommendation} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Campaign *
                </label>
                <select
                  required
                  value={requestForm.campaign_id}
                  onChange={(e) => setRequestForm({ ...requestForm, campaign_id: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Select Campaign</option>
                  {campaigns.map(campaign => (
                    <option key={campaign.id} value={campaign.id}>{campaign.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  AI Agent *
                </label>
                <select
                  required
                  value={requestForm.agent_type}
                  onChange={(e) => setRequestForm({ ...requestForm, agent_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                >
                  {Object.entries(AGENT_TYPES).map(([key, agent]) => (
                    <option key={key} value={key}>{agent.name}</option>
                  ))}
                </select>
                <p className="mt-1 text-sm text-gray-500">
                  {AGENT_TYPES[requestForm.agent_type].description}
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Prompt / Context *
                </label>
                <textarea
                  required
                  value={requestForm.prompt}
                  onChange={(e) => setRequestForm({ ...requestForm, prompt: e.target.value })}
                  rows={5}
                  placeholder="Provide context and specific requirements for the AI recommendation..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div className="flex space-x-3 pt-4 border-t">
                <button
                  type="button"
                  onClick={handleCloseRequestModal}
                  disabled={requesting}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={requesting}
                  className="flex-1 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
                >
                  {requesting ? 'Requesting...' : 'Request Recommendation'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Review Modal */}
      {showReviewModal && selectedRecommendation && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center p-4">
          <div className="relative bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b px-6 py-4 z-10">
              <h3 className="text-lg font-semibold text-gray-900">
                {selectedRecommendation.status === 'pending' ? 'Review Recommendation' : 'View Recommendation'}
              </h3>
            </div>

            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Agent</label>
                <p className="text-gray-900">{getAgentConfig(selectedRecommendation.agent_type).name}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Campaign</label>
                <p className="text-gray-900">{getCampaignName(selectedRecommendation.campaign_id)}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Recommendation</label>
                <div className="bg-gray-50 rounded-lg p-4">
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans">
                    {typeof selectedRecommendation.recommendation_data === 'string'
                      ? selectedRecommendation.recommendation_data
                      : JSON.stringify(selectedRecommendation.recommendation_data, null, 2)}
                  </pre>
                </div>
              </div>

              {selectedRecommendation.status === 'pending' && (
                <form onSubmit={handleReviewRecommendation} className="space-y-4 pt-4 border-t">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Decision *
                    </label>
                    <div className="flex space-x-4">
                      <button
                        type="button"
                        onClick={() => setReviewForm({ ...reviewForm, status: 'approved' })}
                        className={`flex-1 inline-flex items-center justify-center px-4 py-2 border rounded-md text-sm font-medium transition-colors ${
                          reviewForm.status === 'approved'
                            ? 'border-green-500 bg-green-50 text-green-700'
                            : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
                        }`}
                      >
                        <ThumbsUp className="w-4 h-4 mr-2" />
                        Approve
                      </button>
                      <button
                        type="button"
                        onClick={() => setReviewForm({ ...reviewForm, status: 'rejected' })}
                        className={`flex-1 inline-flex items-center justify-center px-4 py-2 border rounded-md text-sm font-medium transition-colors ${
                          reviewForm.status === 'rejected'
                            ? 'border-red-500 bg-red-50 text-red-700'
                            : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
                        }`}
                      >
                        <ThumbsDown className="w-4 h-4 mr-2" />
                        Reject
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Review Notes
                    </label>
                    <textarea
                      value={reviewForm.review_notes}
                      onChange={(e) => setReviewForm({ ...reviewForm, review_notes: e.target.value })}
                      rows={4}
                      placeholder="Add notes about your decision..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>

                  <div className="flex space-x-3 pt-4 border-t">
                    <button
                      type="button"
                      onClick={handleCloseReviewModal}
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      className="flex-1 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                    >
                      Submit Review
                    </button>
                  </div>
                </form>
              )}

              {selectedRecommendation.status !== 'pending' && (
                <div className="flex justify-end pt-4 border-t">
                  <button
                    onClick={handleCloseReviewModal}
                    className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                  >
                    Close
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

