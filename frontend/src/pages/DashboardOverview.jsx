import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, Building2, Megaphone, Sparkles, TrendingUp, AlertTriangle } from 'lucide-react';

export default function DashboardOverview() {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    users: 0,
    organizations: 0,
    campaigns: 0,
    recommendations: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      // Load statistics from API
      const [usersData, orgsData, campaignsData] = await Promise.all([
        api.getUsers({ per_page: 1 }).catch(() => ({ total: 0 })),
        api.getOrganizations({ per_page: 1 }).catch(() => ({ total: 0 })),
        api.getCampaigns({ per_page: 1 }).catch(() => ({ total: 0 })),
      ]);

      setStats({
        users: usersData.total || 0,
        organizations: orgsData.total || 0,
        campaigns: campaignsData.total || 0,
        recommendations: 0, // Would need separate endpoint
      });
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    {
      title: 'Total Users',
      value: stats.users,
      icon: Users,
      color: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-50',
      textColor: 'text-blue-600',
    },
    {
      title: 'Organizations',
      value: stats.organizations,
      icon: Building2,
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-50',
      textColor: 'text-purple-600',
    },
    {
      title: 'Active Campaigns',
      value: stats.campaigns,
      icon: Megaphone,
      color: 'from-green-500 to-green-600',
      bgColor: 'bg-green-50',
      textColor: 'text-green-600',
    },
    {
      title: 'AI Recommendations',
      value: stats.recommendations,
      icon: Sparkles,
      color: 'from-orange-500 to-orange-600',
      bgColor: 'bg-orange-50',
      textColor: 'text-orange-600',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">
          Welcome back, {user?.full_name}!
        </h1>
        <p className="text-blue-100">
          Here's an overview of your Civic Engagement Intelligence Platform
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <Card key={stat.title} className="overflow-hidden">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">
                    {loading ? '...' : stat.value}
                  </p>
                </div>
                <div className={`p-3 rounded-xl ${stat.bgColor}`}>
                  <stat.icon className={`h-8 w-8 ${stat.textColor}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="h-5 w-5 mr-2 text-green-600" />
              Recent Activity
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <ActivityItem
                title="New campaign created"
                description="Youth Voter Registration Drive"
                time="2 hours ago"
              />
              <ActivityItem
                title="AI recommendation approved"
                description="Narrative framework for civic education"
                time="5 hours ago"
              />
              <ActivityItem
                title="New user registered"
                description="John Doe joined as Campaign Manager"
                time="1 day ago"
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <AlertTriangle className="h-5 w-5 mr-2 text-orange-600" />
              Pending Reviews
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <ReviewItem
                title="AI Content Recommendation"
                description="Awaiting approval for social media post"
                priority="high"
              />
              <ReviewItem
                title="Campaign Update"
                description="Budget allocation needs review"
                priority="medium"
              />
              <ReviewItem
                title="User Verification"
                description="3 new users pending verification"
                priority="low"
              />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Platform Info */}
      <Card className="bg-gradient-to-br from-blue-50 to-purple-50 border-blue-200">
        <CardHeader>
          <CardTitle className="text-blue-900">About This Platform</CardTitle>
        </CardHeader>
        <CardContent className="text-blue-800">
          <p className="mb-4">
            The Civic Engagement Intelligence Platform provides AI-powered tools for ethical civic
            engagement, with a focus on transparency, compliance, and human oversight.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">1</span>
              </div>
              <div>
                <h4 className="font-semibold text-blue-900">Advisory Only</h4>
                <p className="text-sm">All AI recommendations require human approval</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">2</span>
              </div>
              <div>
                <h4 className="font-semibold text-blue-900">Fully Compliant</h4>
                <p className="text-sm">Adheres to Kenya DPA 2019, GDPR, and EU AI Act</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">3</span>
              </div>
              <div>
                <h4 className="font-semibold text-blue-900">Transparent</h4>
                <p className="text-sm">Complete audit logging and transparency reports</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-8 h-8 bg-orange-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">4</span>
              </div>
              <div>
                <h4 className="font-semibold text-blue-900">Ethical AI</h4>
                <p className="text-sm">Educational focus, no manipulation or deception</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function ActivityItem({ title, description, time }) {
  return (
    <div className="flex items-start space-x-3 pb-4 border-b last:border-0">
      <div className="flex-shrink-0 w-2 h-2 bg-blue-600 rounded-full mt-2" />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900">{title}</p>
        <p className="text-sm text-gray-500">{description}</p>
        <p className="text-xs text-gray-400 mt-1">{time}</p>
      </div>
    </div>
  );
}

function ReviewItem({ title, description, priority }) {
  const priorityColors = {
    high: 'bg-red-100 text-red-800',
    medium: 'bg-orange-100 text-orange-800',
    low: 'bg-blue-100 text-blue-800',
  };

  return (
    <div className="flex items-start justify-between pb-4 border-b last:border-0">
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900">{title}</p>
        <p className="text-sm text-gray-500">{description}</p>
      </div>
      <span className={`ml-2 px-2 py-1 text-xs font-medium rounded-full ${priorityColors[priority]}`}>
        {priority}
      </span>
    </div>
  );
}

