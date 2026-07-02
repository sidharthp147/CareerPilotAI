import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api.jsx";
import styles from "./UserDashboard.module.css";

function UserDashboard() {
  const [jobs, setJobs] = useState([]);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const fetchRecommendedJobs = async () => {
      try {
        const token = localStorage.getItem("token");

        const response = await api.get("/users/UserRecommendedJobs", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setJobs(response.data.jobs);
        setTotal(response.data.total);

        if (response.data.message) {
          setMessage(response.data.message);
        }
      } catch (err) {
        console.error(err);
        setError("Failed to load recommendations");
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendedJobs();
  }, []);

  return (
    <div className={styles.container}>
      <div className={styles.wrapper}>
        <h2 className={styles.title}>
          Recommended <span className={styles.highlight}>Jobs For You</span>
        </h2>

        {total > 0 && (
          <p className={styles.subtitle}>
            {total} jobs matched with your resume
          </p>
        )}

        {message && (
          <p className={styles.subtitle}>
            {message}
          </p>
        )}

        {loading && (
          <p className={styles.loading}>
            Loading recommendations...
          </p>
        )}

        {error && (
          <p className={styles.error}>
            {error}
          </p>
        )}

        {!loading && jobs.length === 0 && (
          <p className={styles.empty}>
            No matching jobs found
          </p>
        )}

        <div className={styles.jobs}>
          {jobs.map((job) => (
            <div key={job.id} className={styles.card}>

              <div className={styles.cardBody}>

                <div className={styles.cardTop}>
                  <h3>{job.heading.charAt(0).toUpperCase() + job.heading.slice(1)}</h3>
                </div>

                <p className={styles.meta}>
                  📍 <b>{job.location}</b>
                </p>

                <div className={styles.badge}>
                  {job.job_type}
                </div>

                <p className={styles.jobId}>
                  Job ID: {job.id}
                </p>

                <div className={styles.skillSection}>
                  <p className={styles.skillsTitle}>
                    <b>Required Skills</b>
                  </p>

                  {job.skills
                    .split(",")
                    .slice(0, 5)
                    .map((skill) => (
                      <span
                        key={skill}
                        className={styles.skillChip1}
                      >
                        {skill.trim()}
                      </span>
                    ))}

                  {job.skills.split(",").length > 5 && (
                    <span className={styles.moreSkills}>
                      +{job.skills.split(",").length - 5} More
                    </span>
                  )}
                </div>
              </div>

              <div className={styles.cardFooter}>

                {job.final_score && (
                  <div className={styles.scoreSection}>
                    <div className={styles.scoreHeader}>
                      <span>Match Score</span>
                      <span>
                        {(job.final_score * 100).toFixed(0)}%
                      </span>
                    </div>

                    <div className={styles.progressBar}>
                      <div
                        className={styles.progressFill}
                        style={{
                          width: `${job.final_score * 100}%`,
                        }}
                      />
                    </div>
                  </div>
                )}

                <p className={styles.salary}>
                  <b>Salary:</b> {job.salary_range}
                </p>

                <button
                  className={styles.btn}
                  onClick={() =>
                    navigate(/UserDashboard/`${job.id}`)
                  }
                >
                  View More Details
                </button>

              </div>

            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default UserDashboard;