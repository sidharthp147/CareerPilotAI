import { NavLink, useNavigate } from "react-router-dom";
import style from "./NavBarPublic.module.css";
import api from "./api";


function Navbar({ isLoggedIn,setIsLoggedIn, role,setRole}) {
  const navigate = useNavigate();
  
  const handleLogout = async () => {
    const res=await api.get("https://job-portal-sfyn.onrender.com/auth/logout");
    alert("Logged out successfully")
    console.log(res.data);
    localStorage.removeItem("token")
    localStorage.removeItem("USER")
    setIsLoggedIn(false)
    setRole(null);
    navigate("/login");
  };


  return (
    <nav className={style.navbar}>
      <ul className={style.menu}>
        <li><NavLink to="/" className={({isActive}) => isActive ? style.active: ""}>Home</NavLink></li>
        {}
        {!isLoggedIn && (
          <>
            <li><NavLink to="/jobs" className={({isActive}) => isActive ? style.active: ""}>Jobs</NavLink></li>
            <li><NavLink to="/login" className={({isActive}) => isActive ? style.active: ""}>Login</NavLink></li>
            <li><NavLink to="/register" className={({isActive}) => isActive ? style.active: ""}>Register</NavLink></li>
          </>
        )}

        {isLoggedIn && role === "USER" && (
          <>  
            <li><NavLink to="/jobs" className={({isActive}) => isActive ? style.active: ""}>Jobs</NavLink></li>
            <li><NavLink to="/UserDashboard" className={({isActive}) => isActive ? style.active: ""}>Dashboard</NavLink></li>
            <li><button onClick={handleLogout}>Logout</button></li>
          </>
        )}

        {isLoggedIn && role === "RECRUITER" && (
          <>
            
            <li><NavLink to="/RecruiterDashboard" className={({isActive}) => isActive ? style.active: ""}>Dashboard</NavLink></li>
            <li><button onClick={handleLogout}>Logout</button></li>
          </>
        )}
        {isLoggedIn && role === "ADMIN" && (
          <>
            <li><NavLink to="/AdminDashboard" className={({isActive}) => isActive ? style.active: ""}>Dashboard</NavLink></li>
            <li><button onClick={handleLogout}>Logout</button></li>
          </>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;