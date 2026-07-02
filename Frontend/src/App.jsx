import { createBrowserRouter, Navigate, RouterProvider } from "react-router-dom";
import Layout from "./pages/Layout.jsx"
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
import VerifyEmail from "./pages/Verifyemail.jsx";
import ResendVerification from "./pages/Resend_verification.jsx";
import ViewApplications from "./pages/ViewApplications.jsx";
import UserProfile from "./pages/UserProfile.jsx";
import JobsLayout from "./pages/JobsLayout.jsx";
import Saved_Jobs from "./pages/Saved_Jobs.jsx";
import User_Applications from "./pages/User_Applications.jsx";
import ForgotPassword from "./pages/PasswordLayout.jsx";
import ResetPassword from "./pages/PasswordReset.jsx";
import UserDashboardLayout from "./pages/UserDashboardLayout.jsx";
import Notifications from "./pages/Notifications.jsx";
import PasswordLayout from "./pages/PasswordLayout.jsx";
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
      { path: "jobs", element:<JobsLayout />, children:[
        {path:":id", element :isLoggedIn?<JobDetails/>:<Navigate to="/login" replace />},
      ]},
      { path: "UserDashboard", element:(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"USER"}> <UserDashboardLayout /> </ProtectedRoute>) ,children:[
        {path:":id", element :isLoggedIn?<JobDetails/>:<Navigate to="/login" replace />}, 
      ],},
      { path: "RecruiterDashboard", element:(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"RECRUITER"}> <RecruiterDashboard /> </ProtectedRoute>)},
      { path: "AdminDashboard",element:(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"ADMIN"}> <AdminDashboard /> </ProtectedRoute>)},
      { path: "RecruiterDashboard/CreateJob",element :(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"RECRUITER"}> <CreateJob /> </ProtectedRoute>)},
      { path: "RecruiterRegister",element:<RecruiterRegister/>},
      {path:"AdminDashboard/RecruiterApproval",element:(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"ADMIN"}> <RecruiterApproval /> </ProtectedRoute>)},
      {path:"verify-email",element:<VerifyEmail/>},
      {path:"Resend_verification",element:<ResendVerification/>},
      {path:"jobs/Applications/:id",element :(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"RECRUITER"}> <ViewApplications /> </ProtectedRoute>)},
      {path:"/Userprofile",element :(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"USER"}> <UserProfile /> </ProtectedRoute>)},
      {path:"/SavedJobs",element :(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"USER"}> <Saved_Jobs /> </ProtectedRoute>),
      },
      {path:"/SavedJobs/:id",element :(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"USER"}> <JobDetails /> </ProtectedRoute>)},
      {path:"/User_Applications",element :(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"USER"}> <User_Applications /> </ProtectedRoute>)},
      {path:"/ForgotPassword",element : <ForgotPassword />},
      {path:"/ForgotPassword/ResetPassword",element : <ResetPassword />},
      {path:"/Notifications",element :(<ProtectedRoute isLoggedIn={isLoggedIn} role={role} allowedRoles={"USER"}> <Notifications /> </ProtectedRoute>)},
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