import { Link, useNavigate } from 'react-router-dom';
import styles from "./Registration.module.css";
import api from "./api.jsx"
import { useState } from 'react';
function Registration() {
  const navigate=useNavigate();
  const[username,setUsername]=useState("");
  const[email,setEmail]=useState("");
  const[skills,setSkills]=useState("");
  const[experience,setExperience]=useState("");
  const[resume_url,setResume_url]=useState("");
  const[password,setPassword]=useState("");
  const[confirmpassword,setConfirmpassword]=useState("");
  const[error,setError]=useState("");
  const handleSubmit=async(e)=>{
    e.preventDefault();
    try{
      const res=await api.post("/auth/registration",{email,password,confirmpassword,username,skills,experience,resume_url,});
      console.log(res.response);
      alert("Registration Successful");
      navigate("/login");

    }
    catch(err)
    {
        setError(err.response?.data?.message|| err.response.data.detail)
        console.log(err.response)
    }
  }
  
  return (
    <>
     <form onSubmit={handleSubmit}>
        <div className={styles.reg}>
          <div className={styles.regContainer}>
            <div className={styles.headingreg}  >
             <h2>Register</h2>
             {error &&<p style={{color:"red"}}>{error}</p>}
            </div>
          <div className={styles.formGroup1}>
          <label className={styles.unamereg} >Username:</label>
          <input  type="text" className={styles.username} name="username" value={username} onChange={(e)=>setUsername(e.target.value)} required/>
          </div>
          <div className={styles.formGroup2}>
          <label className={styles.emailreg}>Email:</label>
          <input type="email" className={styles.email} name="email"  value={email} onChange={(e)=>setEmail(e.target.value)} required/>
          </div>    
          <div className={styles.formGroup3}>
          <label className={styles.skills} >Skills:</label>
          <input  type="text" className={styles.skills} name="skills" value={skills} onChange={(e)=>setSkills(e.target.value)}/>
          </div>
          <div className={styles.formGroup4}>
          <label className={styles.experience} >Experience:</label>
          <input  type="number" className={styles.experience} name="experience" value={experience} onChange={(e)=>setExperience(e.target.value)} />
          </div>
          <div className={styles.formGroup5}>
          <label className={styles.resumeurl} >Resume URL:</label>
          <input type="text" className={styles.resumeurl} name="resumeurl" value={resume_url} onChange={(e)=>setResume_url(e.target.value)} />
          </div>
          <div className={styles.formGroup6}>
          <label className={styles.pwdreg} >Password:</label>
          <input type="password" className={styles.password} name="password" value={password} onChange={(e)=>setPassword(e.target.value)} required/>
          </div>
          <div className={styles.formGroup7}>
          <label className={styles.confirmpass} >Confirm Password:</label>
          <input  type="password" className={styles.confirmpassword} name="confirmpassword" value={confirmpassword} onChange={(e)=>setConfirmpassword(e.target.value)} required/>
          </div>
          <div className={styles.btnCenter}>
          <button className={styles.registerButton} type="submit" >Register</button>
          </div>  
          <div >
            <Link to="/RecruiterRegister" className={styles.regRecruiter}>Register As Recruiter</Link>
          </div>
          <div className={styles.link}>
        <Link to="/login" className={styles.loginLink}>Already have an account? Login here</Link>
      </div>
    </div>
    </div>
  </form>
  </>
  );
}
export default Registration;