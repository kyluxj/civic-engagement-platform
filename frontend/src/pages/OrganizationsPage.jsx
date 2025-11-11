import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Search, Building2, CheckCircle, XCircle, Clock } from 'lucide-react';
import api from '@/lib/api';

export default function OrganizationsPage() {
  const [organizations, setOrganizations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingOrg, setEditingOrg] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    type: 'ngo',
    registration_number: '',
    contact_email: '',
    contact_phone: '',
    address: '',
    compliance_status: 'pending'
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchOrganizations();
  }, []);

  const fetchOrganizations = async () => {
    try {
      setLoading(true);
      const response = await api.getOrganizations();
      setOrganizations(response.organizations || []);
    } catch (err) {
      setError('Failed to load organizations');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      if (editingOrg) {
        await api.updateOrganization(editingOrg.id, formData);
        setSuccess('Organization updated successfully');
      } else {
        await api.createOrganization(formData);
        setSuccess('Organization created successfully');
      }
      
      fetchOrganizations();
      handleCloseModal();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save organization');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this organization?')) {
      return;
    }

    try {
      await api.deleteOrganization(id);
      setSuccess('Organization deleted successfully');
      fetchOrganizations();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete organization');
    }
  };

  const handleEdit = (org) => {
    setEditingOrg(org);
    setFormData({
      name: org.name,
      type: org.type,
      registration_number: org.registration_number || '',
      contact_email: org.contact_email || '',
      contact_phone: org.contact_phone || '',
      address: org.address || '',
      compliance_status: org.compliance_status
    });
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingOrg(null);
    setFormData({
      name: '',
      type: 'ngo',
      registration_number: '',
      contact_email: '',
      contact_phone: '',
      address: '',
      compliance_status: 'pending'
    });
  };

  const filteredOrganizations = organizations.filter(org =>
    org.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    org.type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusBadge = (status) => {
    const statusConfig = {
      approved: { color: 'bg-green-100 text-green-800', icon: CheckCircle, label: 'Approved' },
      pending: { color: 'bg-yellow-100 text-yellow-800', icon: Clock, label: 'Pending' },
      suspended: { color: 'bg-red-100 text-red-800', icon: XCircle, label: 'Suspended' }
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

  const getTypeLabel = (type) => {
    const types = {
      ngo: 'NGO',
      political: 'Political',
      government: 'Government',
      public_figure: 'Public Figure'
    };
    return types[type] || type;
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
          <h1 className="text-3xl font-bold text-gray-900">Organizations</h1>
          <p className="mt-2 text-sm text-gray-600">
            Manage organizations and their compliance status
          </p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
        >
          <Plus className="w-5 h-5 mr-2" />
          Add Organization
        </button>
      </div>

      {/* Alerts */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4">
          <div className="flex">
            <XCircle className="h-5 w-5 text-red-400" />
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {success && (
        <div className="bg-green-50 border-l-4 border-green-400 p-4">
          <div className="flex">
            <CheckCircle className="h-5 w-5 text-green-400" />
            <div className="ml-3">
              <p className="text-sm text-green-700">{success}</p>
            </div>
          </div>
        </div>
      )}

      {/* Search */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search organizations..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      {/* Organizations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredOrganizations.map((org) => (
          <div
            key={org.id}
            className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow duration-200 overflow-hidden"
          >
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <div className="bg-blue-100 rounded-lg p-3">
                    <Building2 className="w-6 h-6 text-blue-600" />
                  </div>
                  <div className="ml-3">
                    <h3 className="text-lg font-semibold text-gray-900">{org.name}</h3>
                    <p className="text-sm text-gray-500">{getTypeLabel(org.type)}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-2 mb-4">
                {org.contact_email && (
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Email:</span> {org.contact_email}
                  </p>
                )}
                {org.contact_phone && (
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Phone:</span> {org.contact_phone}
                  </p>
                )}
                {org.registration_number && (
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Reg #:</span> {org.registration_number}
                  </p>
                )}
              </div>

              <div className="flex items-center justify-between mb-4">
                {getStatusBadge(org.compliance_status)}
                <div className="text-sm text-gray-500">
                  {org.user_count || 0} users • {org.campaign_count || 0} campaigns
                </div>
              </div>

              <div className="flex space-x-2 pt-4 border-t">
                <button
                  onClick={() => handleEdit(org)}
                  className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                >
                  <Edit className="w-4 h-4 mr-2" />
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(org.id)}
                  className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-red-300 rounded-md text-sm font-medium text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
                >
                  <Trash2 className="w-4 h-4 mr-2" />
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredOrganizations.length === 0 && (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <Building2 className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No organizations found</h3>
          <p className="mt-1 text-sm text-gray-500">
            {searchTerm ? 'Try adjusting your search' : 'Get started by creating a new organization'}
          </p>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center p-4">
          <div className="relative bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b px-6 py-4 z-10">
              <h3 className="text-lg font-semibold text-gray-900">
                {editingOrg ? 'Edit Organization' : 'Add New Organization'}
              </h3>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Organization Name *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Organization Type *
                </label>
                <select
                  required
                  value={formData.type}
                  onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="ngo">NGO</option>
                  <option value="political">Political</option>
                  <option value="government">Government</option>
                  <option value="public_figure">Public Figure</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Registration Number
                </label>
                <input
                  type="text"
                  value={formData.registration_number}
                  onChange={(e) => setFormData({ ...formData, registration_number: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Contact Email
                </label>
                <input
                  type="email"
                  value={formData.contact_email}
                  onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Contact Phone
                </label>
                <input
                  type="tel"
                  value={formData.contact_phone}
                  onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Address
                </label>
                <textarea
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Compliance Status *
                </label>
                <select
                  required
                  value={formData.compliance_status}
                  onChange={(e) => setFormData({ ...formData, compliance_status: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="suspended">Suspended</option>
                </select>
              </div>

              <div className="flex space-x-3 pt-4 border-t">
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                >
                  {editingOrg ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

