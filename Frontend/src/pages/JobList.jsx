import { useEffect, useState } from "react";
import styles from "./JobList.module.css";
import { Link } from "react-router-dom";
import api from "./api.jsx"

function JobList() {
  const [error,setError]=useState("");
  const [jobs,setJobs]=useState([]);
  const [search,setSearch]=useState("");
const [jobType, setJobType] = useState("");
const [location, setLocation] = useState("");
  useEffect(()=>{
    const fetchJobs=async()=>{
  try{
    const res=await api.get("http://127.0.0.1:8000/jobs/jobs");
    setJobs(res.data)
  }
  catch(err){
    setError(err.response?.data?.message|| "Cant Fecth data")
  }
};
fetchJobs();
},[]);
const handleSubmit=async () => 
{
try{
    const res=await api.post(`http://127.0.0.1:8000/jobs/Jobs/search?search=${search}`);
    console.log(res.data);
    setJobs(res.data);
  }
  catch(err){
    setError(err.response?.data?.message|| "Cant Fecth data")
  }
}
const applyFilters = async () => {
  const res = await api.get(`/jobs/fJobs?search=${search}&job_type=${jobType}&location=${location}`  );
  setJobs(res.data);
};
  return (
    <div className={styles.container}>
      <h2>Available Jobs</h2>
      {error && <p style={{color:"red"}}>{error}</p>}
      <div className={styles.search}>
          <input type="search" id="search" name="search" placeholder="Search...Jobs Here......" onChange={(e)=>setSearch(e.target.value)}/>
          <button className={styles.sbutton} type="submit" onClick={handleSubmit}>Search</button>
    <select  style={{marginLeft:"5px"}}value={jobType} onChange={(e) => setJobType(e.target.value)}>
    <option value="">All Job Types</option>
    <option value="Permanent">Permanent</option>
    <option value="Remote">Remote</option>
    <option value="Part Time">Part Time</option>
  </select>

  <select style={{marginLeft:"5px"}}value={location} onChange={(e) => setLocation(e.target.value)}>
    <option value="">All Locations</option>
    <option value="Bangalore">Bangalore</option>
    <option value="Chennai">Chennai</option>
  </select>

  <button style={{marginLeft:"5px",marginTop:"3px",marginBottom:"3px",width:"65px"}} onClick={applyFilters}>Apply</button>
</div>
      <div className={styles.jobs}>
        {jobs.map(job => (

          <div key={job.id} className={styles.card}>
            <h3>Job name:={job.heading}</h3>
            <p>{job.job_type}</p>
            <p>{job.location}</p>
            <Link to={`/Jobs/${job.id}`} className={styles.btn}>
              View Details
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default JobList;