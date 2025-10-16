import { useAuth } from '@/contexts/AuthContext';
import { hasPermission, hasAnyPermission, hasAllPermissions } from '@/lib/permissions';

/**
 * ProtectedAction Component
 * 
 * Conditionally renders children based on user permissions.
 * Useful for hiding/showing buttons, links, or entire sections based on user role.
 * 
 * @param {string} permission - Single permission to check
 * @param {string[]} anyOf - Array of permissions (user needs at least one)
 * @param {string[]} allOf - Array of permissions (user needs all)
 * @param {React.ReactNode} children - Content to render if user has permission
 * @param {React.ReactNode} fallback - Optional content to render if user lacks permission
 */
export default function ProtectedAction({ 
  permission, 
  anyOf, 
  allOf, 
  children, 
  fallback = null 
}) {
  const { user } = useAuth();
  
  if (!user) {
    return fallback;
  }

  let hasAccess = false;

  if (permission) {
    hasAccess = hasPermission(user.role, permission);
  } else if (anyOf && anyOf.length > 0) {
    hasAccess = hasAnyPermission(user.role, anyOf);
  } else if (allOf && allOf.length > 0) {
    hasAccess = hasAllPermissions(user.role, allOf);
  } else {
    // If no permission specified, allow access
    hasAccess = true;
  }

  return hasAccess ? children : fallback;
}

