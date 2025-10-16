import { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, Users, Target, Brain, Activity, Calendar } from 'lucide-react';
import api from '@/lib/api';

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

export default function AnalyticsPage() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalCampaigns: 0,
    activeCampaigns: 0,
    totalUsers: 0,
    totalOrganizations: 0,
    totalRecommendations: 0,
    pendingRecommendations: 0
  });
  const [campaigns, setCampaigns] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [analytics, setAnalytics] = useState([]);
  const [timeRange, setTimeRange] = useState('30');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [campaignsRes, recsRes, usersRes, orgsRes] = await Promise.all([
        api.get('/api/campaigns'),
        api.get('/api/ai/recommendations'),
        api.get('/api/users'),
        api.get('/api/organizations')
      ]);

      const campaignsData = campaignsRes.data.campaigns || [];
      const recsData = recsRes.data.recommendations || [];
      const usersData = usersRes.data.users || [];
      const orgsData = orgsRes.data.organizations || [];

      setCampaigns(campaignsData);
      setRecommendations(recsData);

      setStats({
        totalCampaigns: campaignsData.length,
        activeCampaigns: campaignsData.filter(c => c.status === 'active').length,
        totalUsers: usersData.length,
        totalOrganizations: orgsData.length,
        totalRecommendations: recsData.length,
        pendingRecommendations: recsData.filter(r => r.status === 'pending').length
      });

      // Generate mock analytics data for visualization
      generateAnalyticsData(campaignsData, recsData);
    } catch (err) {
      console.error('Failed to load analytics data:', err);
    } finally {
      setLoading(false);
    }
  };

  const generateAnalyticsData = (campaignsData, recsData) => {
    // Generate time-series data for the last 30 days
    const days = parseInt(timeRange);
    const timeSeriesData = [];
    const today = new Date();

    for (let i = days - 1; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      const dateStr = date.toISOString().split('T')[0];

      timeSeriesData.push({
        date: dateStr,
        campaigns: Math.floor(Math.random() * 10) + 5,
        recommendations: Math.floor(Math.random() * 15) + 10,
        engagement: Math.floor(Math.random() * 100) + 50
      });
    }

    setAnalytics(timeSeriesData);
  };

  const getCampaignStatusData = () => {
    const statusCounts = campaigns.reduce((acc, campaign) => {
      acc[campaign.status] = (acc[campaign.status] || 0) + 1;
      return acc;
    }, {});

    return Object.entries(statusCounts).map(([name, value]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value
    }));
  };

  const getCampaignTypeData = () => {
    const typeCounts = campaigns.reduce((acc, campaign) => {
      acc[campaign.campaign_type] = (acc[campaign.campaign_type] || 0) + 1;
      return acc;
    }, {});

    return Object.entries(typeCounts).map(([name, value]) => ({
      name: name.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
      value
    }));
  };

  const getRecommendationStatusData = () => {
    const statusCounts = recommendations.reduce((acc, rec) => {
      acc[rec.status] = (acc[rec.status] || 0) + 1;
      return acc;
    }, {});

    return Object.entries(statusCounts).map(([name, value]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value
    }));
  };

  const getAgentTypeData = () => {
    const agentCounts = recommendations.reduce((acc, rec) => {
      acc[rec.agent_type] = (acc[rec.agent_type] || 0) + 1;
      return acc;
    }, {});

    const agentNames = {
      narrative: 'Narrative Architect',
      content: 'Content Synthesizer',
      distribution: 'Distribution Optimizer',
      feedback: 'Feedback Intelligence'
    };

    return Object.entries(agentCounts).map(([name, value]) => ({
      name: agentNames[name] || name,
      value
    }));
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
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="mt-2 text-sm text-gray-600">
            Platform metrics and performance insights
          </p>
        </div>
        <select
          value={timeRange}
          onChange={(e) => {
            setTimeRange(e.target.value);
            generateAnalyticsData(campaigns, recommendations);
          }}
          className="px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
          <option value="90">Last 90 days</option>
        </select>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Campaigns</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.totalCampaigns}</p>
              <p className="text-sm text-green-600 mt-1">
                {stats.activeCampaigns} active
              </p>
            </div>
            <div className="bg-blue-100 rounded-lg p-3">
              <Target className="w-8 h-8 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Users</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.totalUsers}</p>
              <p className="text-sm text-gray-500 mt-1">
                {stats.totalOrganizations} organizations
              </p>
            </div>
            <div className="bg-green-100 rounded-lg p-3">
              <Users className="w-8 h-8 text-green-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">AI Recommendations</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.totalRecommendations}</p>
              <p className="text-sm text-yellow-600 mt-1">
                {stats.pendingRecommendations} pending review
              </p>
            </div>
            <div className="bg-purple-100 rounded-lg p-3">
              <Brain className="w-8 h-8 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Activity Trend */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-gray-900">Activity Trend</h2>
          <Activity className="w-5 h-5 text-gray-400" />
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={analytics}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
            />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip 
              labelFormatter={(value) => new Date(value).toLocaleDateString()}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="campaigns" 
              stroke="#3B82F6" 
              strokeWidth={2}
              name="Campaigns"
            />
            <Line 
              type="monotone" 
              dataKey="recommendations" 
              stroke="#10B981" 
              strokeWidth={2}
              name="Recommendations"
            />
            <Line 
              type="monotone" 
              dataKey="engagement" 
              stroke="#F59E0B" 
              strokeWidth={2}
              name="Engagement"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Campaign Status Distribution */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Campaign Status</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={getCampaignStatusData()}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {getCampaignStatusData().map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Campaign Types */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Campaign Types</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={getCampaignTypeData()}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="value" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* AI Agent Usage */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">AI Agent Usage</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={getAgentTypeData()} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" tick={{ fontSize: 12 }} />
              <YAxis dataKey="name" type="category" width={150} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="value" fill="#8B5CF6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Recommendation Status */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Recommendation Status</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={getRecommendationStatusData()}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {getRecommendationStatusData().map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity Summary */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Platform Summary</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="border-l-4 border-blue-500 pl-4">
            <p className="text-sm font-medium text-gray-600">Campaign Performance</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">
              {stats.activeCampaigns > 0 
                ? ((stats.activeCampaigns / stats.totalCampaigns) * 100).toFixed(1) 
                : 0}%
            </p>
            <p className="text-sm text-gray-500 mt-1">Active campaign rate</p>
          </div>

          <div className="border-l-4 border-green-500 pl-4">
            <p className="text-sm font-medium text-gray-600">AI Approval Rate</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">
              {stats.totalRecommendations > 0
                ? ((recommendations.filter(r => r.status === 'approved').length / stats.totalRecommendations) * 100).toFixed(1)
                : 0}%
            </p>
            <p className="text-sm text-gray-500 mt-1">Recommendations approved</p>
          </div>

          <div className="border-l-4 border-purple-500 pl-4">
            <p className="text-sm font-medium text-gray-600">Avg Users per Org</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">
              {stats.totalOrganizations > 0
                ? (stats.totalUsers / stats.totalOrganizations).toFixed(1)
                : 0}
            </p>
            <p className="text-sm text-gray-500 mt-1">User distribution</p>
          </div>
        </div>
      </div>
    </div>
  );
}

