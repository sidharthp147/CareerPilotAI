import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api";
import styles from "./saved_Jobs.module.css";

function Saved_Jobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    const loadSavedJobs = async () => {
      try {
        const token = localStorage.getItem("token");

        const response = await api.get(
          "/jobs/savedjobsfull",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        setJobs(response.data);
        
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    loadSavedJobs();
  }, []);

  const handleUnsave = async (jobId) => {
    try {
      const token = localStorage.getItem("token");

      await api.post("/jobs/unsave",{"job_id":jobId},{
        headers:{
          "Authorization":`Bearer ${token}`}
      });

      setJobs((prevJobs) =>
        prevJobs.filter(
          (job) => job.job_id !== jobId
        )
      );
    } catch (error) {
      console.error(
        "Failed to unsave job:",
        error
      );
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.wrapper}>
        <h2 className={styles.title}>
          Saved Jobs
        </h2>

        <h3 style={{ textAlign: "center" }}>
          Jobs you have saved for later
        </h3>

        {loading && (
          <p className={styles.loading}>
            Loading saved jobs...
          </p>
        )}

        {!loading &&
          jobs.length === 0 && (
            <p className={styles.empty}>
              No saved jobs found 🚀
            </p>
          )}

        <div className={styles.jobs}>
          {jobs.map((job) => (
            <div
              key={job.job_id}
              className={styles.card}
            >
              <div
                className={
                  styles.cardTop
                }
              >
                <h3>
                  {job.heading.charAt(0).toUpperCase() + job.heading.slice(1)}
                </h3>
              </div>

              <p
                className={
                  styles.meta
                }
              >
                📍 {job.location}
              </p>

              <div
                className={
                  styles.badge
                }
                style={{
                  width: "75px",
                }}
              >
                {job.job_type}
              </div>

              <p
                className={
                  styles.jobId
                }
              >
                Job ID: {job.job_id}
              </p>

              <p>
                Skills:{" "}
                {job.skills}
              </p>

              <p>
                Salary:{" "}
                {job.salary_range}
              </p>

              {job.experience && (
                <p>
                  Experience:{" "}
                  {job.experience}
                </p>
              )}

              <div
                className={
                  styles.btnContainer
                }
              >
                <button
                  className={
                    styles.btn
                  }
                  onClick={() =>
                    navigate(
                      `/SavedJobs/${job.job_id}`
                    )
                  }
                >
                  View More Details
                </button>

                <button
                  className={
                    styles.btn
                  }
                  onClick={() =>
                    handleUnsave(
                      job.job_id
                    )
                  }
                >
                  Unsave Job
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Saved_Jobs;