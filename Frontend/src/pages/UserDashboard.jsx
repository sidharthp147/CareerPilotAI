import styles from "./UserDashboard.module.css";
import { useEffect, useState } from "react";
import api from "./api.jsx"
function UserDashboard() {
        const[stats,setStats]=useState([{
         "heading":"",
         "location":"",
         "job_type":"",
          "status":"",
          "applied_at":"",

}]);
        const[error,setError]=useState("");
       useEffect(()=>{
        const fetchstats=async ()=>{
    try{
      const token=localStorage.getItem("token");
      console.log(token)
      const res=await api.get("/users/UserDashboard",{headers: {Authorization:`Bearer ${token}`,},});
      console.log(res.data)
      setStats(res.data);
    }
    catch(err)
    {setError(err.response?.data?.message|| "Cant Fetch dataa")
  
    }
    };
    fetchstats();
  },[]);
  
return   (
    <div className={styles.container}>
      <h2>User Dashboard</h2>
 {error && <p style={{color:"red"}}>{error}</p>}

      <div className={styles.jobs}>
        {stats.map(stats => (

          <div key={stats.id} className={styles.card}>
            <h3>job Heading: {stats.heading}</h3>
            <p>{stats.location}</p>
            <p>{stats.job_type}</p> 
            <p>{stats.status}</p>
            <p>{stats.applied_at}</p>
          </div>
        ))}
      </div>
      </div>)
}


export default UserDashboard;