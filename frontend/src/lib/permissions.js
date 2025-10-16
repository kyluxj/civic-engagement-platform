/**
 * Role-based Access Control (RBAC) Permissions System
 * 
 * Roles:
 * - super_admin: Full system access
 * - org_admin: Organization management
 * - campaign_manager: Campaign management
 * - content_creator: Content creation
 * - analyst: Analytics and reporting
 * - reviewer: Review AI recommendations
 * - viewer: Read-only access
 */

export const ROLES = {
  SUPER_ADMIN: 'super_admin',
  ORG_ADMIN: 'org_admin',
  CAMPAIGN_MANAGER: 'campaign_manager',
  CONTENT_CREATOR: 'content_creator',
  ANALYST: 'analyst',
  REVIEWER: 'reviewer',
  VIEWER: 'viewer'
};

export const PERMISSIONS = {
  // User Management
  VIEW_USERS: 'view_users',
  CREATE_USERS: 'create_users',
  EDIT_USERS: 'edit_users',
  DELETE_USERS: 'delete_users',
  
  // Organization Management
  VIEW_ORGANIZATIONS: 'view_organizations',
  CREATE_ORGANIZATIONS: 'create_organizations',
  EDIT_ORGANIZATIONS: 'edit_organizations',
  DELETE_ORGANIZATIONS: 'delete_organizations',
  
  // Campaign Management
  VIEW_CAMPAIGNS: 'view_campaigns',
  CREATE_CAMPAIGNS: 'create_campaigns',
  EDIT_CAMPAIGNS: 'edit_campaigns',
  DELETE_CAMPAIGNS: 'delete_campaigns',
  
  // AI Recommendations
  VIEW_RECOMMENDATIONS: 'view_recommendations',
  REQUEST_RECOMMENDATIONS: 'request_recommendations',
  REVIEW_RECOMMENDATIONS: 'review_recommendations',
  
  // Content Management
  VIEW_CONTENT: 'view_content',
  CREATE_CONTENT: 'create_content',
  EDIT_CONTENT: 'edit_content',
  DELETE_CONTENT: 'delete_content',
  PUBLISH_CONTENT: 'publish_content',
  
  // Analytics
  VIEW_ANALYTICS: 'view_analytics',
  EXPORT_ANALYTICS: 'export_analytics',
  
  // System
  VIEW_AUDIT_LOGS: 'view_audit_logs',
  MANAGE_COMPLIANCE: 'manage_compliance'
};

// Role-to-Permissions mapping
const rolePermissions = {
  [ROLES.SUPER_ADMIN]: [
    // Full access to everything
    ...Object.values(PERMISSIONS)
  ],
  
  [ROLES.ORG_ADMIN]: [
    PERMISSIONS.VIEW_USERS,
    PERMISSIONS.CREATE_USERS,
    PERMISSIONS.EDIT_USERS,
    PERMISSIONS.VIEW_ORGANIZATIONS,
    PERMISSIONS.EDIT_ORGANIZATIONS,
    PERMISSIONS.VIEW_CAMPAIGNS,
    PERMISSIONS.CREATE_CAMPAIGNS,
    PERMISSIONS.EDIT_CAMPAIGNS,
    PERMISSIONS.DELETE_CAMPAIGNS,
    PERMISSIONS.VIEW_RECOMMENDATIONS,
    PERMISSIONS.REQUEST_RECOMMENDATIONS,
    PERMISSIONS.REVIEW_RECOMMENDATIONS,
    PERMISSIONS.VIEW_CONTENT,
    PERMISSIONS.CREATE_CONTENT,
    PERMISSIONS.EDIT_CONTENT,
    PERMISSIONS.DELETE_CONTENT,
    PERMISSIONS.PUBLISH_CONTENT,
    PERMISSIONS.VIEW_ANALYTICS,
    PERMISSIONS.EXPORT_ANALYTICS,
    PERMISSIONS.VIEW_AUDIT_LOGS
  ],
  
  [ROLES.CAMPAIGN_MANAGER]: [
    PERMISSIONS.VIEW_CAMPAIGNS,
    PERMISSIONS.CREATE_CAMPAIGNS,
    PERMISSIONS.EDIT_CAMPAIGNS,
    PERMISSIONS.VIEW_RECOMMENDATIONS,
    PERMISSIONS.REQUEST_RECOMMENDATIONS,
    PERMISSIONS.VIEW_CONTENT,
    PERMISSIONS.CREATE_CONTENT,
    PERMISSIONS.EDIT_CONTENT,
    PERMISSIONS.VIEW_ANALYTICS
  ],
  
  [ROLES.CONTENT_CREATOR]: [
    PERMISSIONS.VIEW_CAMPAIGNS,
    PERMISSIONS.VIEW_RECOMMENDATIONS,
    PERMISSIONS.VIEW_CONTENT,
    PERMISSIONS.CREATE_CONTENT,
    PERMISSIONS.EDIT_CONTENT
  ],
  
  [ROLES.ANALYST]: [
    PERMISSIONS.VIEW_CAMPAIGNS,
    PERMISSIONS.VIEW_RECOMMENDATIONS,
    PERMISSIONS.VIEW_CONTENT,
    PERMISSIONS.VIEW_ANALYTICS,
    PERMISSIONS.EXPORT_ANALYTICS
  ],
  
  [ROLES.REVIEWER]: [
    PERMISSIONS.VIEW_CAMPAIGNS,
    PERMISSIONS.VIEW_RECOMMENDATIONS,
    PERMISSIONS.REVIEW_RECOMMENDATIONS,
    PERMISSIONS.VIEW_CONTENT,
    PERMISSIONS.EDIT_CONTENT
  ],
  
  [ROLES.VIEWER]: [
    PERMISSIONS.VIEW_CAMPAIGNS,
    PERMISSIONS.VIEW_RECOMMENDATIONS,
    PERMISSIONS.VIEW_CONTENT,
    PERMISSIONS.VIEW_ANALYTICS
  ]
};

/**
 * Check if a user has a specific permission
 * @param {string} userRole - The user's role
 * @param {string} permission - The permission to check
 * @returns {boolean} - Whether the user has the permission
 */
export const hasPermission = (userRole, permission) => {
  if (!userRole || !permission) return false;
  
  const permissions = rolePermissions[userRole] || [];
  return permissions.includes(permission);
};

/**
 * Check if a user has any of the specified permissions
 * @param {string} userRole - The user's role
 * @param {string[]} permissions - Array of permissions to check
 * @returns {boolean} - Whether the user has any of the permissions
 */
export const hasAnyPermission = (userRole, permissions) => {
  if (!userRole || !permissions || permissions.length === 0) return false;
  
  return permissions.some(permission => hasPermission(userRole, permission));
};

/**
 * Check if a user has all of the specified permissions
 * @param {string} userRole - The user's role
 * @param {string[]} permissions - Array of permissions to check
 * @returns {boolean} - Whether the user has all of the permissions
 */
export const hasAllPermissions = (userRole, permissions) => {
  if (!userRole || !permissions || permissions.length === 0) return false;
  
  return permissions.every(permission => hasPermission(userRole, permission));
};

/**
 * Get all permissions for a role
 * @param {string} userRole - The user's role
 * @returns {string[]} - Array of permissions
 */
export const getRolePermissions = (userRole) => {
  return rolePermissions[userRole] || [];
};

/**
 * Check if a role is an admin role
 * @param {string} userRole - The user's role
 * @returns {boolean} - Whether the role is an admin role
 */
export const isAdmin = (userRole) => {
  return userRole === ROLES.SUPER_ADMIN || userRole === ROLES.ORG_ADMIN;
};

/**
 * Get human-readable role name
 * @param {string} role - The role identifier
 * @returns {string} - Human-readable role name
 */
export const getRoleName = (role) => {
  const roleNames = {
    [ROLES.SUPER_ADMIN]: 'Super Administrator',
    [ROLES.ORG_ADMIN]: 'Organization Administrator',
    [ROLES.CAMPAIGN_MANAGER]: 'Campaign Manager',
    [ROLES.CONTENT_CREATOR]: 'Content Creator',
    [ROLES.ANALYST]: 'Analyst',
    [ROLES.REVIEWER]: 'Reviewer',
    [ROLES.VIEWER]: 'Viewer'
  };
  
  return roleNames[role] || role;
};

/**
 * Get role description
 * @param {string} role - The role identifier
 * @returns {string} - Role description
 */
export const getRoleDescription = (role) => {
  const descriptions = {
    [ROLES.SUPER_ADMIN]: 'Full system access and control',
    [ROLES.ORG_ADMIN]: 'Manage organization users, campaigns, and content',
    [ROLES.CAMPAIGN_MANAGER]: 'Create and manage campaigns',
    [ROLES.CONTENT_CREATOR]: 'Create and edit content',
    [ROLES.ANALYST]: 'View analytics and generate reports',
    [ROLES.REVIEWER]: 'Review AI recommendations and content',
    [ROLES.VIEWER]: 'Read-only access to campaigns and content'
  };
  
  return descriptions[role] || 'No description available';
};

export default {
  ROLES,
  PERMISSIONS,
  hasPermission,
  hasAnyPermission,
  hasAllPermissions,
  getRolePermissions,
  isAdmin,
  getRoleName,
  getRoleDescription
};

