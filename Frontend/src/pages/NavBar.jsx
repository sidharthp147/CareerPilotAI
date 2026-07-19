import { NavLink, useNavigate } from "react-router-dom";
import style from "./NavBarPublic.module.css";
import api from "./api";
import { useState } from "react";
import Notification_Bell from "../pages/Notification_Bell.jsx";
import logo from "../assets/logo.png"; // Adjust the path to your logo image

function Navbar({ isLoggedIn, setIsLoggedIn, role, setRole }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);


  const handleLogout = async () => {
    const confirmLogout = window.confirm("Are you sure you want to logout?");
    if (!confirmLogout) return;
    if (loading) return;

    try {
      setLoading(true);
       await api.post("/auth/logout");
    

      localStorage.removeItem("token");
      localStorage.removeItem("USER");

      setIsLoggedIn(false);
      setRole(null);

      navigate("/login");
    } catch (err) {
      console.error(err);
      alert("Logout failed", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <nav className={style.navbar}>
      {/* 🔥 Logo */}
      <div className={style.logo} onClick={() => navigate("/")}>
        <img src={logo} alt="logo" height={100} width={200} style={{marginRight:"5px",color:"black"}} / >
        
      </div>

      {/* 🔥 Desktop Menu */}
      <ul className={style.menu}>
        <li>
          <NavLink to="/" className={({ isActive }) => isActive ? style.active : ""}>
            Home
          </NavLink>
        </li>
        <li>
              <NavLink to="/jobs" className={({ isActive }) => isActive ? style.active : ""}>
                Jobs
              </NavLink>
              </li>
        {!isLoggedIn && (
          <>
           

            <li>
              <NavLink
                to="/login"
                className={({ isActive }) =>`
                  ${style.loginBtn} ${isActive ? style.active : ""}`
                }
              >
                Login
              </NavLink>
            </li>

            <li>
              <NavLink
                to="/register"
                className={({ isActive }) =>`
                  ${style.registerBtn} ${isActive ? style.active : ""}`
                }
              >
                Register
              </NavLink>
            </li>
          </>
        )}

        {isLoggedIn &&  (
          <>
           

            {role === "USER" && (
              
                <>
                
                <NavLink to="/SavedJobs" className={({ isActive }) => isActive ? style.active : ""}>
                  Saved Jobs
                </NavLink>
                <NavLink to="/User_Applications" className={({ isActive }) => isActive ? style.active : ""}>
                  My Applications
                </NavLink>
                <NavLink to="/UserDashboard" className={({ isActive }) => isActive ? style.active : ""}>
                  Dashboard
                </NavLink>
                
                <NavLink to="/UserProfile" className={({ isActive }) => isActive ? style.active : ""}>
                  Profile
                </NavLink>
                <li>
                    <Notification_Bell />
                  </li>
              </>
              
            )}

            {role === "RECRUITER" && (
              <li>
                <NavLink to="/RecruiterDashboard" className={({ isActive }) => isActive ? style.active : ""}>
                  Dashboard
                </NavLink>
              </li>
            )}
            
            {role === "ADMIN" && (
              <li>
                <NavLink to="/AdminDashboard" className={({ isActive }) => isActive ? style.active : ""}>
                  Dashboard
                </NavLink>
              </li>
            )}
            

            <li>
              <button onClick={handleLogout} disabled={loading}>
                {loading ? "Logging out..." : "Logout"}
              </button>
            </li>
          </>
        )}
      </ul>

      {/* 🔥 Mobile Hamburger */}
      <div
        className={style.hamburger}
        onClick={() => setMenuOpen(!menuOpen)}
      >
        ☰
      </div>

      {/* 🔥 Mobile Menu */}
      {menuOpen && (
        <div className={style.mobileMenu}>
          <NavLink to="/" onClick={() => setMenuOpen(false)}>Home</NavLink>

          {!isLoggedIn && (
            <>
              <NavLink to="/jobs" onClick={() => setMenuOpen(false)}>Jobs</NavLink>
              <NavLink to="/login" onClick={() => setMenuOpen(false)}>Login</NavLink>
              <NavLink to="/register" onClick={() => setMenuOpen(false)}>Register</NavLink>
            </>
          )}

          {isLoggedIn && (
            <>
              <NavLink to="/jobs" onClick={() => setMenuOpen(false)}>Jobs</NavLink>

              {role === "USER" && (
                <>
                  <NavLink to="/UserDashboard" onClick={() => setMenuOpen(false)}>Dashboard</NavLink>
                  <NavLink to="/UserProfile" onClick={() => setMenuOpen(false)}>Profile</NavLink>
                  <NavLink to="/SavedJobs" onClick={() => setMenuOpen(false)}>Saved Jobs</NavLink>
                  <NavLink to="/User_Applications" onClick={() => setMenuOpen(false)}>My Applications</NavLink>
                  <NavLink to="/" onClick={() => setMenuOpen(false)}>Notifications</NavLink>

                </>
              )}

              {role === "RECRUITER" && (
                <NavLink to="/RecruiterDashboard" onClick={() => setMenuOpen(false)}>Dashboard</NavLink>
              )}

              {role === "ADMIN" && (
                <NavLink to="/AdminDashboard" onClick={() => setMenuOpen(false)}>Dashboard</NavLink>
              )}

              <button onClick={handleLogout} disabled={loading}>
                {loading ? "Logging out..." : "Logout"}
              </button>
            </>
          )}
        </div>
      )}
    </nav>
  );
}

export default Navbar;