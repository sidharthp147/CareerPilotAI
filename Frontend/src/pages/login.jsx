import { Link, Navigate } from 'react-router-dom';
import styles from "./Login.module.css";
import { useState } from 'react';
import api from "./api.jsx"
import { useNavigate } from 'react-router-dom';
function Login({setIsLoggedIn,setRole}) {
   const navigate=useNavigate();
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");
  const [error,setError]=useState("");
  const handleSubmit=async(e)=>{
    e.preventDefault();
  
  
    try{
      const res=await api.post("/auth/login",{email,password})
      localStorage.setItem("token",res.data.token);
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
    setError(err.response?.data?.message|| "Email/password incorrect")
  }
}
  return(
    <>
  
      <div className={styles.bodyBackground}>
      <div className={styles.loginContainer}>
        <form className={styles.loginForm} onSubmit={handleSubmit}>
          <h2 align="center">Login</h2>
          {error &&<p style={{color:"red"}}>{error}</p>}
          <label id="email">Email</label>
          <input id="inputemail" type="text" value={email} onChange={(e)=>setEmail(e.target.value)} required />
          <label id="pwd" htmlFor="pwd">Password</label>
          <input id="inputpwd" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} required />
          <button className={styles.loginButton} type="submit">Login</button>
          <Link className={styles.registerLink} to="/Register">New User? Register Here</Link>
        </form>
      </div>
      </div>
      
 </>
)    }
export default Login;
