import api from "./api.jsx"
import styles from "./AdminDashboard.module.css";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";

 function  AdminDashboard() {
  const[stats,setStats]=useState({total_users:0,
    total_jobs:0,total_recruiters:0} )
     const [error,setError]=useState("");
     useEffect(()=>{
      const fetchstats=async ()=>{
  try{
    const res=await api.get("admin/AdminDashboard");
    setStats(res.data);
  }
  catch(err)
  {setError(err.response?.data?.message|| "Cant Fetch data")

  }
  };
  fetchstats();
},[]);

  return (
    <div className={styles.container}>
      <h2>Admin Dashboard</h2>
      {error && <p style={{color:"red"}}> {error}</p>}
      <p>Total Users: {stats.total_users}</p>
      <p>Total Recruiters: {stats.total_recruiters}</p>
      <p>Total Jobs: {stats.total_jobs}</p>
      <Link to="/RecruiterApproval" style={{color:"aqua",fontSize:"20px"}}>Applications</Link>
    </div>
  );
}

export default AdminDashboard;