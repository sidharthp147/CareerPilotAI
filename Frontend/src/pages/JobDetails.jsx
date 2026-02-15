import styles from "./JobDetails.module.css";
import { useState, useEffect } from "react";
import api from "./api.jsx"
import { useParams } from "react-router-dom";

function JobDetails() {
  const { id } = useParams();

  const [error, setError] = useState("");
  const [job, setJob] = useState(null);
  const [applied, setApplied] = useState(false);


  useEffect(() => {
      const token = localStorage.getItem("token");
    const fetchJob = async () => {
      try {
        const res = await api.get(`/jobs/Jobs/${id}`,{headers: {Authorization: `Bearer ${token}`,},});
        setJob(res.data);
      } catch (err) {
        setError(err.response?.data?.detail || "Can't fetch job");
      }
    };

    fetchJob();
  }, [id]);
  useEffect(() => {
      const token = localStorage.getItem("token");
    const checkApplied = async () => {
      try {
        const res = await api.get(`/jobs/jobs/${id}/applied`,{headers: {Authorization: `Bearer ${token}`,},});
        setApplied(res.data.applied);
      } catch (err) {
        console.error("Apply check failed");
        console.log(err)
      }
    };

    checkApplied();
  }, [id]);

  const applyJob = async () => {
      const token = localStorage.getItem("token");
    try {
      await api.post(`/jobs/jobs/${id}/apply`,{},{headers: {Authorization: `Bearer ${token}`,},});
      setApplied(true);
    } catch (err) {
      alert(err.response?.data?.detail || "Error applying");
      console.log(err)
    }
  };

  if (!job) {
    return <h2>Job not found</h2>;
  }

  return (
    <div className={styles.container}>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>{job.heading}</h2>
      <p>{job.location}</p>
      <p>{job.description}</p>

      <button
        onClick={applyJob}
        disabled={applied}
        className={applied ? styles.appliedBtn : styles.applyBtn}
      >
        {applied ? "Applied" : "Apply Now"}
      </button>
    </div>
  );
}

export default JobDetails;