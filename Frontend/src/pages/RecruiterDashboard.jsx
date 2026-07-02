import styles from "./RecruiterDashboard.module.css";
import { useEffect, useState } from "react";
import api from "./api.jsx";
import { Link } from "react-router-dom";

function RecruiterDashboard() {
  const [stats, setStats] = useState([]);
  const [isapproved, setIsapproved] = useState(null);
  const [total, setTotal] = useState(0);
  //eslint-disable-next-line
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [applicationCounts, setApplicationCounts] = useState({});
  const [noticeType, setNoticeType] =
    useState("success");
    const [notValidated,setNotValidated]=useState("Your Account Is Yet To Verify")

  useEffect(() => {
    const fetchstats = async () => {
      try {
        const token =
          localStorage.getItem("token");

        const res = await api.get(
          "/recruiters/RecruiterDashboard",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const { res1, res2 ,res3 ,  res4} = res.data;
        setApplicationCounts(res3 || {});
        setTotal(res4 || 0);
        setStats(res1 || []);
        setIsapproved(res2);
      } catch (err) {
        if (
          err.response?.status === 403
        ) {
          setNotice(
            err.response?.data
              ?.message ||
              `Try again after ${
                err.response?.data
                  ?.remaining_seconds ||
                60
              } seconds`
          );
          setNotValidated(err.response.data)
        }

        }
    };

    fetchstats();
  }, []);

  const handleDelete = async (
    job_id
  ) => {
    try {
      const isConfirmed =
        window.confirm(
          "Delete this job?"
        );

      if (!isConfirmed) return;

      const token =
        localStorage.getItem("token");

      await api.delete(
        `/jobs/DeleteJob/${job_id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setNoticeType("success");
      setNotice(
        "Job deleted successfully"
      );
      setTimeout(() => {
        setNotice("");
      }, 10000);

      setStats((prev) =>
        prev.filter(
          (job) => job.id !== job_id
        )
      );
    } catch (err) {
      setNoticeType("error");

      setNotice(
        err.response?.data
          ?.message ||
          "Unable to delete job"
      );
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.wrapper}>
        <div className={styles.hero}>
          <h1>
            Recruiter Dashboard
          </h1>

          <p>
            Manage jobs, track
            applications and grow
            your hiring pipeline.
          </p>
          
          {isapproved && (
            <Link
              to="/RecruiterDashboard/CreateJob"
              className={
                styles.createBtn
              }
            >
              + Create Job
            </Link>
          )}
        </div>

        {isapproved  === false && (
          <div
            className={
              styles.warning
            }
          >
            {notValidated}
          </div>
        )}

        {notice && (
          <div
            className={
              noticeType ===
              "success"
                ? styles.success
                : styles.errorBox
            }
          >
            {notice}
          </div>
        )}

        {error && (
          <div
            className={
              styles.errorBox
            }
          >
            {error}
          </div>
        )}

        <div className={styles.stats}>
          <div
            className={
              styles.statCard
            }
          >
            <h2>
              {total}
            </h2>
            <p>Total Jobs</p>
          </div>

          <div
            className={
              styles.statCard
            }
          >
            <h2>
              {
                stats.filter(
                  (j) => j.id
                ).length
              }
            </h2>
            <p>Active Jobs</p>
          </div>
        </div>

        {stats.length === 0 && (
          <div
            className={
              styles.empty
            }
          >
            No jobs created yet 🚀
          </div>
        )}

        <div className={styles.jobs}>
          {stats.map((job) => (
            <div
              key={job.id}
              className={styles.card}
            >
              <div
                className={
                  styles.cardTop
                }
              >
                <h3>
                  {job.title.charAt(0).toUpperCase() + job.title.slice(1)}
                </h3>

                <span
                  className={
                    styles.badge
                  }
                >
                  {job.job_type}
                </span>
              </div>

              <p>
                📍{" "}
                {
                  job.location
                }
              </p>

              <p>
                💻{" "}
                {
                  job.skills
                }
              </p>

              <p>
                📅{" "}
                {new Date(
                  job.created_at
                ).toLocaleDateString()}
              </p>

              <div
                className={
                  styles.actions
                }
              >
                <Link
                  to={`/jobs/Applications/${job.id}`}
                  className={
                    styles.viewBtn
                  }
                >
                  Applications ( {applicationCounts[job.id]||0} )
                </Link>

                <button
                  className={
                    styles.deleteBtn
                  }
                  onClick={() =>
                    handleDelete(
                      job.id
                    )
                  }
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default RecruiterDashboard;