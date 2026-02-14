import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children, isLoggedIn, allowedRoles, role }) => {
  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
    return <Navigate to="/" replace />;
  }

  return children;
};

export default ProtectedRoute;