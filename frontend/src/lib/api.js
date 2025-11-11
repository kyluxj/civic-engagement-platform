/**
 * API service for backend communication
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://civic-platform-api.onrender.com';

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
    this.token = localStorage.getItem('access_token');
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
  }

  getToken() {
    return this.token || localStorage.getItem('access_token');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
      ...options,
      headers,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Request failed');
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Auth endpoints
  async login(email, password) {
    const data = await this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    if (data.access_token) {
      this.setToken(data.access_token);
    }
    return data;
  }

  async register(userData) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async logout() {
    await this.request('/api/auth/logout', { method: 'POST' });
    this.setToken(null);
  }

  async getCurrentUser() {
    return this.request('/api/auth/me');
  }

  // User endpoints
  async getUsers(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/api/users?${query}`);
  }

  async getUser(userId) {
    return this.request(`/api/users/${userId}`);
  }

  async createUser(userData) {
    return this.request('/api/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async updateUser(userId, userData) {
    return this.request(`/api/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  async deleteUser(userId) {
    return this.request(`/api/users/${userId}`, {
      method: 'DELETE',
    });
  }

  // Organization endpoints
  async getOrganizations(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/api/organizations?${query}`);
  }

  async getOrganization(orgId) {
    return this.request(`/api/organizations/${orgId}`);
  }

  async createOrganization(orgData) {
    return this.request('/api/organizations', {
      method: 'POST',
      body: JSON.stringify(orgData),
    });
  }

  async updateOrganization(orgId, orgData) {
    return this.request(`/api/organizations/${orgId}`, {
      method: 'PUT',
      body: JSON.stringify(orgData),
    });
  }

  async deleteOrganization(orgId) {
    return this.request(`/api/organizations/${orgId}`, {
      method: 'DELETE',
    });
  }

  // Campaign endpoints
  async getCampaigns(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/api/campaigns?${query}`);
  }

  async getCampaign(campaignId) {
    return this.request(`/api/campaigns/${campaignId}`);
  }

  async createCampaign(campaignData) {
    return this.request('/api/campaigns', {
      method: 'POST',
      body: JSON.stringify(campaignData),
    });
  }

  async updateCampaign(campaignId, campaignData) {
    return this.request(`/api/campaigns/${campaignId}`, {
      method: 'PUT',
      body: JSON.stringify(campaignData),
    });
  }

  async deleteCampaign(campaignId) {
    return this.request(`/api/campaigns/${campaignId}`, {
      method: 'DELETE',
    });
  }

  async getCampaignAnalytics(campaignId) {
    return this.request(`/api/campaigns/${campaignId}/analytics`);
  }

  // AI Agent endpoints
  async requestNarrativeArchitect(campaignId) {
    return this.request('/api/ai/narrative-architect', {
      method: 'POST',
      body: JSON.stringify({ campaign_id: campaignId }),
    });
  }

  async requestContentSynthesizer(data) {
    return this.request('/api/ai/content-synthesizer', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async requestDistributionOptimizer(data) {
    return this.request('/api/ai/distribution-optimizer', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async requestFeedbackIntelligence(data) {
    return this.request('/api/ai/feedback-intelligence', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getRecommendation(recommendationId) {
    return this.request(`/api/ai/recommendations/${recommendationId}`);
  }

  async approveRecommendation(recommendationId, reviewNotes = '') {
    return this.request(`/api/ai/recommendations/${recommendationId}/approve`, {
      method: 'PUT',
      body: JSON.stringify({ review_notes: reviewNotes }),
    });
  }

  async rejectRecommendation(recommendationId, reviewNotes) {
    return this.request(`/api/ai/recommendations/${recommendationId}/reject`, {
      method: 'PUT',
      body: JSON.stringify({ review_notes: reviewNotes }),
    });
  }
}

export const api = new ApiService();
export default api;

