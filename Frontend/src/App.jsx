import { createBrowserRouter, Navigate, RouterProvider } from "react-router-dom";
import Layout from "./pages/Layout.jsx"
import PublicHome from "./pages/PublicHome.jsx";
import Login from "./pages/login.jsx";
import Registration from "./pages/Registration.jsx";
import JobList from "./pages/JobList.jsx";
import Home from "./pages/Home.jsx";
import UserDashboard from "./pages/UserDashboard.jsx";
import RecruiterDashboard from "./pages/RecruiterDashboard.jsx";
import Navbar from "./pages/NavBar.jsx";
import {useState } from "react";
import AdminDashboard from "./pages/AdminDashboard.jsx";
import JobDetails from "./pages/JobDetails.jsx";
import CreateJob from "./pages/CreateJob.jsx";
import RecruiterRegister from "./pages/RecruiterRegister.jsx";
import RecruiterApproval from "./pages/RecruiterApproval.jsx";
import ProtectedRoute from "./pages/ProtectedRoute.jsx";
function App() {
const [isLoggedIn,setIsLoggedIn]= useState(()=>Boolean(localStorage.getItem("token")));
const [role,setRole] = useState(()=>localStorage.getItem("role"));


const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} role={role} setRole={setRole}/>,
    children: [
      {
      index: true, element:<Home />
      },
      { path: "login", element:<Login setIsLoggedIn={setIsLoggedIn} role={role} setRole={setRole}/> },
      { path: "register", element:<Registration /> },
      { path: "jobs", element:<JobList />},
      { path: "UserDashboard", element:(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"USER"}> <UserDashboard /> </ProtectedRoute>)},
      { path: "RecruiterDashboard", element:(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"RECRUITER"}> <RecruiterDashboard /> </ProtectedRoute>)},
      { path: "AdminDashboard",element:(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"ADMIN"}> <AdminDashboard /> </ProtectedRoute>)},
      { path: "Jobs/:id",element :isLoggedIn?<JobDetails/>:<Navigate to="/login" replace />},
      { path: "RecruiterDashboard/CreateJob",element :(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"RECRUITER"}> <CreateJob /> </ProtectedRoute>)},
      { path: "RecruiterRegister",element:<RecruiterRegister/>},
      {path:"RecruiterApproval",element:(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"ADMIN"}> <RecruiterApproval /> </ProtectedRoute>)},
   
      
      ]
  }
]);
  return (
  <> 
  <RouterProvider router={router} />;
  </>
  );
}
export default App;