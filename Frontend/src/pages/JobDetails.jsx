import styles from "./JobDetails.module.css";
import { useState, useEffect } from "react";
import api from "./api.jsx"
import { useParams } from "react-router-dom";

function JobDetails() {
  const { id } = useParams();

  const [error, setError] = useState("");
  const [job, setJob] = useState(null);
  const [applied, setApplied] = useState(false);
  const [applying, setApplying] = useState(false);
  const [notice, setNotice] = useState("");
  const [noticeType, setNoticeType] = useState("success");
  const role= localStorage.getItem("role");


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
        console.error(err)
      }
    };

    checkApplied();
  }, [id]);

  const applyJob = async () => {
      const token = localStorage.getItem("token");
    try {
      if (applying || applied) return;
      setApplying(true);
      setNotice("");
      await api.post(`/jobs/jobs/${id}/apply`,{},{headers: {Authorization: `Bearer ${token}`,},});
      setApplied(true);
    } catch (err) {
      setNoticeType("error");
      setNotice(err.response?.data?.detail || "Error applying");
      console.error(noticeType)
    } finally {
      setApplying(false);
    }
  };

  if (!job) {
    return <h2>Job not found</h2>;
  }

  return (
    <div className={styles.container}>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button onClick={() => window.history.back()} className={styles.closeBtn}>        X
      </button>
      <h2>{job["heading"].charAt(0).toUpperCase() + job["heading"].slice(1)}</h2>
      <p>Skills:{job["skills"]}</p>
      <p>Location:{job["location"]}</p>
      <p>Description:{job["description"]}</p>
      <p>Salary:{job["salary_range"]}</p>
      <p>Job Type:{job["job_type"]}</p>
      <p>Experience:{job["experience"]}</p>

      {notice && (
        <p
          style={{
            marginTop: 12,
            padding: "10px 12px",
            borderRadius: 10,
            border: "1px solid #f5c2c7",
            background: "#f8d7da",
            color: "#842029",
          }}
        >
          {notice}
        </p>
      )}
      {role==="USER" && (
      <button
        onClick={applyJob}
        disabled={applied || applying}
        className={applied ? styles.appliedBtn : styles.applyBtn}
      >
        {applied ? "Applied" : applying ? "Applying..." : "Apply Now"}
      </button>)}
    </div>
  );
}

export default JobDetails;