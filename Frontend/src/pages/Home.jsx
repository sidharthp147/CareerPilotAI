import styles from "./Home.module.css";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className={styles.container}>
      <section className={styles.hero}>
        <h1>Find Your Dream Job</h1>
        <p>Connecting talent with top companies</p>
        <div className={styles.actions}>
          <Link to="/jobs" className={styles.primaryBtn}>
            Find Jobs
          </Link>
          <Link to="/RecruiterDashboard" className={styles.secondaryBtn}>
            Post a Job
          </Link>
        </div>
      </section>
    </div>
  );
}

export default Home;