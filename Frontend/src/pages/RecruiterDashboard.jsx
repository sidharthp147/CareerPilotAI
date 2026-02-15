import styles from "./RecruiterDashboard.module.css";
import { useEffect, useState } from "react";
import api from "./api.jsx"
import { Link } from "react-router";
function RecruiterDashboard() {
        const[stats,setStats]=useState([{
          "heading":"",
          "skills":"",
          "location":"",
          "job_type":"",
          "created_at":""

}]);  
        const [isapproved,setIsapproved]=useState(""); 
        const[error,setError]=useState("");
       useEffect(()=>{
        const fetchstats=async ()=>{
    try{
      const token=localStorage.getItem("token");
      const res=await api.get("https://job-portal-sfyn.onrender.com/recruiters/RecruiterDashboard",{headers: {Authorization:`Bearer ${token}`,},});
      const{res1,res2}=res.data;
      console.log(res2);
      setIsapproved(res2);
      setStats(res1);
    }
    catch(err)
    {setError(err.response?.data?.message|| "Cant Fetch data")
  
    }
    };
    fetchstats();
  },[]);
  
return   (
    <div className={styles.container}>
      <h2>Recruiter Dashboard</h2>
 {error && <p style={{color:"red"}}>{error}</p>}
      {isapproved===false&&(<p className="notapproved" style={{color:"white"}}>Admin has not approved your registration request</p>)}
      <div className={styles.jobs}>
        {stats.map(stats => (

          <div key={stats.id} className={styles.card}>
            <h3>Job name: {stats.heading}</h3>
            <p>{stats.skills}</p>
            <p>{stats.job_type}</p>
            <p>{stats.location}</p>
            <p>{stats.created_at}</p>
          </div>
        ))}
      </div>
      <div className={styles.link}>
        {isapproved?
      <Link to="/RecruiterDashboard/CreateJob" disabled={isapproved} style={{color:"aqua",fontSize:"20px"}}>Create Jobs</Link>:<span style={{color:"violet"}}>Create Jobs</span>}
      </div>

      </div>)
}


export default RecruiterDashboard;