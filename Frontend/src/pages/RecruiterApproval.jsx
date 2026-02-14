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
      const res = await api.get("http://127.0.0.1:8000/admin/recruiters");
      setRecruiters(res.data);
    } catch (error) {
      console.error("Error fetching recruiters", error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id) => {
    try {
      const res=await api.post(`http://127.0.0.1:8000/admin/${id}/approve`);
      console.log(res.data.message)
      await fetchRecruiters();
      setRecruiters((prev) => prev.filter((r) => r.userid !== id));
    } catch (error) {
      console.error("Approve failed", error);
    }
  };

  const handleReject = async (id) => {
    try {
       const res=await api.post(`http://127.0.0.1:8000/admin/${id}/reject`);
       console.log(res.data.message)
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
      <h2 className={styles.title}>Recruiter Approval</h2>

      {recruiters.length === 0 ? (
        <p className={styles.empty}>No pending recruiters</p>
      ) : (
        <div className={styles.grid}>
          {recruiters.map((rec) => (
            <div key={rec.id} className={styles.card}>
              <h3>{rec.company_name}</h3>
              <p><strong>Email:</strong> {rec.email}</p>
              <p className={styles.desc}>{rec.company_description}</p>

              <div className={styles.actions}>
                <button
                  className={styles.approve}
                  onClick={() => handleApprove(rec.user_id)}
                >
                  Approve
                </button>
                <button
                  className={styles.reject}
                  onClick={() => handleReject(rec.user_id)}
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