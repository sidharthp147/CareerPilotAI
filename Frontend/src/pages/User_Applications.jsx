import styles from "./User_Applications.module.css";
import { useEffect, useState } from "react";
import api from "./api.jsx";

function User_Applications() {
  const [stats, setStats] = useState([]);
  const [error, setError] = useState("");
  const [cursor,setCursor]= useState(null);
  const [total,setTotal]= useState(0);
  const [totalApplied,setTotalApplied]= useState(0);
  const [totalAccepted,setTotalAccepted]= useState(0);
  const [totalRejected,setTotalRejected]= useState(0);
  const [cursorFlag,setCursorFlag]= useState(false);

  const fetchstats =async()=>{
    try {
      const token = localStorage.getItem("token");
      const res =await  api.get(`/users/UserApplication?cursor=${cursor}`,{headers: {Authorization: `Bearer ${token}`},});
      setStats(prev=>[...prev,...res.data.applications]);
      setTotal(res.data.total);
      setTotalApplied(res.data.total_applied);
      setTotalAccepted(res.data.total_accepted);
      setTotalRejected(res.data.total_rejected);
      if (res.data.next_cursor == null){
        setCursorFlag(false);
        return}
      setCursor(res.data.next_cursor);
      setCursorFlag(true);
    } catch (err) {
      setError(
        err.response?.data?.message ||
          "Can't fetch data"
      );
    }}

  useEffect(() => {
      //eslint-disable-next-line
    fetchstats();
  }, []);

  useEffect(() => {
    const user_id =
      localStorage.getItem("user_id");

    const ws = new WebSocket(`ws://localhost:8000/ws/user/${user_id}`);
    
    ws.onopen = () => {
      
    };

    ws.onmessage = (event) => {
      JSON.parse(
        event.data
      );

    

      fetchstats();
    };

    ws.onclose = () => {
      
    };

    ws.onerror = (error) => {
      console.error(
        "WebSocket error:",
        error
      );
    };

    return () => {
      ws.close();
    };
  }, []);
  const handleLoadMore = () => {
    fetchstats();
  }
 

  return (
    <div className={styles.container}>
      <div className={styles.wrapper}>
        <h2 className={styles.title}>
          My Applications
        </h2>

        <p className={styles.subtitle}>
          Track all your job
          applications in one place
        </p>

        {error && (
          <p className={styles.error}>
            {error}
          </p>
        )}

        {/* STATS */}
        <div className={styles.statsBar}>
          <div
            className={styles.statCard}
          >
            <div
              className={
                styles.statNumber
              }
            >
              {total}
            </div>

            <div
              className={
                styles.statLabel
              }
            >
              Total Applications
            </div>
          </div>

          <div
            className={styles.statCard}
          >
            <div
              className={
                styles.statNumber
              }
            >
              {totalApplied
              }
            </div>

            <div
              className={
                styles.statLabel
              }
            >
              Pending
            </div>
          </div>

          <div
            className={styles.statCard}
          >
            <div
              className={
                styles.statNumber
              }
            >
              {
                totalAccepted
              }
            </div>

            <div
              className={
                styles.statLabel
              }
            >
              Accepted
            </div>
          </div>

          <div
            className={styles.statCard}
          >
            <div
              className={
                styles.statNumber
              }
            >
              {
                totalRejected
              }
            </div>

            <div
              className={
                styles.statLabel
              }
            >
              Rejected
            </div>
          </div>
        </div>

        {/* EMPTY STATE */}
        {stats.length === 0 &&
          !error && (
            <div
              className={
                styles.empty
              }
            >
              No applications found 🚀
            </div>
          )}

        {/* APPLICATIONS */}
        <div className={styles.jobs}>
          {stats.map((item) => (
            <div
              key={item.id}
              className={styles.card}
            >
              <h3>
                {item.heading.charAt(0).toUpperCase() + item.heading.slice(1)}
              </h3>

              <p
                className={
                  styles.meta
                }
              >
                📍 {item.location}
              </p>

              <span
                className={
                  styles.badge
                }
              >
                {item.job_type}
              </span>

              <p
                className={
                  styles.status
                }
              >
                Status:
                <strong>
                  {" "}
                  {
                    item.application_status
                  }
                </strong>
              </p>

              <p
                className={
                  styles.date
                }
              >
                Applied On:{" "}
                {new Date(
                  item.applied_at
                ).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
        {cursorFlag &&(
        <div className={styles.loadMoreContainer}>
          <button className={styles.loadMore} onClick={handleLoadMore}>Load More</button>
        </div>)}
      </div>
    </div>
  );
}

export default User_Applications;