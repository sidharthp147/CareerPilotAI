import styles from "./ViewApplications.module.css";
import { useState, useEffect, useCallback } from "react";
import api from "./api.jsx";
import { useParams } from "react-router-dom";

function ApplicationDetails() {

  const { id } = useParams();
  const [error, setError] = useState("");
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [rankedCandidates, setRankedCandidates] = useState([]);
  const [showRanked, setShowRanked] = useState(false);
  const [rankCandidates,setRankCandidates]=useState(false)

  const fetchJobAppn = useCallback(async () => {

    try {

      setLoading(true);

      const response = await api.get(`/jobs/Applications/${id}`);

      setJob(response.data);

    } catch (err) {

      setError(
        err.response?.data?.detail || "Can't fetch job"
      );

    } finally {

      setLoading(false);
    }

  }, [id]);



  useEffect(() => {

    fetchJobAppn();

  }, [fetchJobAppn]);



  useEffect(() => {

    const user_id = localStorage.getItem("user_id");

    const ws = new WebSocket(`wss://career-pilot-ai-147.vercel.app/ws/recruiter/${user_id}`);

    ws.onopen = () => {
    };

    ws.onmessage = (event) => {

      JSON.parse(event.data);


      // refresh applications live
      fetchJobAppn();
    };

    ws.onclose = () => {
    };

    ws.onerror = (error) => {
      console.error(error)
    };

    return () => {
      ws.close();
    };

  }, [fetchJobAppn]);



  const handleApprove = async (userId, jobId) => {

    try {

        await api.post(`recruiters/user/${jobId}/${userId}/approve`);
      fetchJobAppn();
      setRankedCandidates(prev=>prev.filter((r) => r.job_seeker_id !== userId));

    } catch (error) {

      console.error("Approve failed", error);
    }
  };



  const handleReject = async (userId, jobId) => {
    try {

      await api.post(`/recruiters/user/${jobId}/${userId}/reject`);

      fetchJobAppn();
      setRankedCandidates(prev=>prev.filter((r) => r.job_seeker_id !== userId));

    } catch (error) {

      console.error("Reject failed", error);
    }
  };



  if (loading) return <h2>Loading...</h2>;
  const handleRankCandidates =async () => { 
    if (rankCandidates==true)
      return;
    setRankCandidates(true)

  try {
  const response = await api.post(`/recruiters/rankcandidates/${id}`)
  if (response.data == null)
  {
    alert("No candidates to rank");
    return
  }
  setRankedCandidates(
    response.data
  );
  setShowRanked(true);
  }
  catch (err) {
    console.error(err);
    
  }}


  return (
  <div className={styles.container}>
    <div className={styles.header}>
      <h1>Applications</h1>

      <p>
        Review and manage candidate applications
      </p>

      <div className={styles.stats}>
        Total Applications: {job?.total || 0}
      </div>
      <button
  className={styles.rankBtn}
  onClick={handleRankCandidates}
  disabled={rankCandidates}
>
  Rank Candidates
</button>
    </div>

    {error && (
      <div className={styles.error}>
        {error}
      </div>
    )}
    {showRanked && (
  <div className={styles.rankedSection}>
    <h2>AI Ranked Candidates</h2>

    <div className={styles.grid}>
      {rankedCandidates.map((item, index) => (
        <div
          key={item.candidate.job_seeker_id}
          className={styles.card}
        >
          <div className={styles.cardTop}>
            <h3>
              #{index + 1} {item.resume.full_name?.replace(/"/g, "")}
            </h3>

            <span className={styles.matchScore}>
              {(item.similarity * 100).toFixed(1)}% Match(ATS)
            </span>
          </div>

          <div className={styles.details}>
            <p>
              <strong>Role:</strong>{" "}
              {item.resume.role}
            </p>

            <p>
              <strong>Experience:</strong>{" "}
              {item.resume.experience} years
            </p>

            <p>
              <strong>Skills:</strong>{" "}
              {item.resume.skills?.replace(/"/g, "")}
            </p>

            <p>
              <strong>Email:</strong>{" "}
              {item.resume.email?.replace(/"/g, "")}
            </p>
          </div>

          <div className={styles.aiExplanation}>
            <strong>AI Explanation</strong>

            <p>{item.explanation}</p>
          </div>
          
        </div>
      ))}
    </div>
  </div>
)}
    <div className={styles.grid}>
      {job?.applications?.map((item) => (
        <div
          key={item.id}
          className={styles.card}
        >
          <div className={styles.cardTop}>
            <h3>{item.seeker?.name}</h3>

            <span
              className={`${styles.status} ${
                item.application?.status ==="APPROVED"? styles.approved: item.application?.status === "REJECTED" ? styles.rejected : styles.pending
              }`}
            >
              {item.application?.status}
            </span>
          </div>

          <div className={styles.details}>
            <p>
              <strong>Experience:</strong>{" "}
              {item.seeker?.experience} years
            </p>

            <p>
              <strong>Skills:</strong>{" "}
              {item.seeker?.skills}
            </p>
          </div>

          <a
            href={item.seeker?.resume_url}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.resumeBtn}
          >
            View Resume
          </a>

          {item.application?.status ===
            "APPLIED" && (
            <div className={styles.actions}>
              <button
                className={styles.approve}
                onClick={() =>
                  handleApprove(
                    item.application
                      .job_seeker_id,
                    id
                  )
                }
              >
                Approve
              </button>

              <button
                className={styles.reject}
                onClick={() =>
                  handleReject(
                    item.application
                      .job_seeker_id,
                    id
                  )
                }
              >
                Reject
              </button>
            </div>
          )}
        </div>
      ))}
    </div>
  </div>
);
}

export default ApplicationDetails;