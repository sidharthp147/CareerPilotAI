import { Link, Navigate } from 'react-router-dom';
import styles from "./Login.module.css";
import { useState } from 'react';
import api from "./api.jsx"
import { useNavigate } from 'react-router-dom';
import bg from "../assets/360_F_292905667_yFUJNJPngYeRNlrRL4hApHWxuYyRY4kN.jpg";
function Login({setIsLoggedIn,setRole}) {
   const navigate=useNavigate();
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");
  const [error,setError]=useState("");
  const [loading,setLoading]=useState(false);
  const [unverified,setUnverified]=useState(false);
  const handleSubmit=async(e)=>{
    e.preventDefault();
  if(loading) return;
  setLoading(true);
  
    try{
      const res=await api.post("/auth/login",{email,password})
      localStorage.setItem("token",res.data.token);
      localStorage.setItem("user_id",res.data.user_id);
      localStorage.setItem("role",res.data.role);
      setIsLoggedIn(true);
      setRole(res.data.role);
      alert("Login Successful")
      if(res.data.role==="USER")
        navigate("/UserDashboard")
      else if(res.data.role==="RECRUITER")
        navigate("/RecruiterDashboard")
      else if(res.data.role==="ADMIN")
        navigate("/AdminDashboard")

    }
  catch(err){
    
    if (err.response?.data.detail === "User is not verified" ) {
      setUnverified(true);
      setError("User Not Verified.Please check your email for verification link or resend verification email button below.")
    
  } 
  else if (err.response?.status === 401) {
    setError(err.response?.data?.detail || "Email/password incorrect")
   
  }
  else {
    setError("Something went wrong. Please try again later.")
  }
  setLoading(false);
}
  }
  return(
    <>
  
      <div className={styles.bodyBackground}  style={{backgroundImage:`url(${bg})`}}>
      <div className={styles.loginContainer}>
        <form className={styles.loginForm} onSubmit={handleSubmit}>
          <h2 align="center">Login</h2>
          {error &&<p style={{color:"red"}}>{error}</p>}
          <label id="email">Email</label>
          <input id="inputemail" type="text" value={email} onChange={(e)=>setEmail(e.target.value)} required />
          <label id="pwd" htmlFor="pwd">Password</label>
          <input id="inputpwd" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} required />
          <button type="submit" className={styles.loginButton} disabled={loading} type="submit">{loading ? "Logging in..." : "Login"}</button>
          <div className={styles.fogotContainer}>
            <Link className={styles.forgotLink} to="/ForgotPassword">Forgot Password?</Link>

          </div>
          <Link className={styles.registerLink} to="/Register">New User? Register Here</Link>
          {unverified && (
          <button onClick={() =>{setEmail("");setPassword(""); navigate("/Resend_verification")}} className={styles.resendButton} disabled={loading}>
            {"Resend Verification Email"}
          </button>)}
        </form>
      </div>
      </div>
      
 </>
)    

}

export default Login;
