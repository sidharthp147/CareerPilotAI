import { useEffect, useState } from "react";
import api from "./api.jsx"
import styles from "./RecruiterApproval.module.css";


const RecruiterApproval = () => {
  const [recruiters, setRecruiters] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRecruiters();
  }, []);

  const fetchRecruiters = async () => {
    try {
      const res = await api.get("/admin/recruiters");
      setRecruiters(res.data);
    } catch (error) {
      console.error("Error fetching recruiters", error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id) => {
    try {
      await api.post(`/admin/${id}/approve`);
      await fetchRecruiters();
      setRecruiters((prev) => prev.filter((r) => r.userid !== id));
    } catch (error) {
      console.error(error)
    }
  };

  const handleReject = async (id) => {
    try {
       await api.post(`/admin/${id}/reject`);
       await fetchRecruiters();
      setRecruiters((prev) => prev.filter((r) => r.user_id !== id));
    } catch (error) {
      console.error("Reject failed", error);
    }
  };

  if (loading) {
    return <p className={styles.loading}>Loading recruiters...</p>;
  }
return (
  <div className={styles.container}>
    <div className={styles.header}>
      <h1>Recruiter Approvals</h1>

      <p>
        Review and manage recruiter registration requests
      </p>

      <div className={styles.stats}>
        Pending Requests: {recruiters.length}
      </div>
    </div>

    {loading ? (
      <div className={styles.loading}>
        Loading recruiters...
      </div>
    ) : recruiters.length === 0 ? (
      <div className={styles.empty}>
        No pending recruiters
      </div>
    ) : (
      <div className={styles.grid}>
        {recruiters.map((rec) => (
          <div
            key={rec.id}
            className={styles.card}
          >
            <div className={styles.cardTop}>
              <h3>{rec.company_name}</h3>

              <span className={styles.badge}>
                Pending
              </span>
            </div>

            <p>
              <strong>Email:</strong>{" "}
              {rec.email}
            </p>

            <p className={styles.desc}>
              {rec.company_description}
            </p>

            <div className={styles.actions}>
              <button
                className={styles.approve}
                onClick={() =>
                  handleApprove(rec.user_id)
                }
              >
                Approve
              </button>

              <button
                className={styles.reject}
                onClick={() =>
                  handleReject(rec.user_id)
                }
              >
                Reject
              </button>
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
);
};

export default RecruiterApproval;