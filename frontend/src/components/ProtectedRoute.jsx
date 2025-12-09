import { Navigate, useLocation } from 'react-router-dom';
import { useUser } from '../hooks/useUser';

const ProtectedRoute = ({ children, allowedRoles }) => {
  const { data: user, isLoading, isError } = useUser();
  const location = useLocation();

  if (isLoading) {
    return <div className="loading-spinner">Loading...</div>; 
  }

  if (isError || !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
};

export default ProtectedRoute;