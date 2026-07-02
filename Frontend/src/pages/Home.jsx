import styles from "./Home.module.css";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className={styles.container}>
      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1>
            Find Your <span>Dream Job</span>
          </h1>

          <p>
            Discover opportunities powered by AI matching,
            resume analysis, and skill gap detection.
          </p>

          <div className={styles.actions}>
            <Link to="/jobs" className={styles.primaryBtn}>
              Find Jobs
            </Link>

            <Link
              to="/RecruiterDashboard"
              className={styles.secondaryBtn}
            >
              Post a Job
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className={styles.stats}>
        <div className={styles.statCard}>
          <h2>10K+</h2>
          <p>Jobs Available</p>
        </div>

        <div className={styles.statCard}>
          <h2>2K+</h2>
          <p>Companies</p>
        </div>

        <div className={styles.statCard}>
          <h2>50K+</h2>
          <p>Candidates</p>
        </div>

        <div className={styles.statCard}>
          <h2>95%</h2>
          <p>Match Accuracy</p>
        </div>
      </section>

      {/* Features */}
      <section className={styles.features}>
        <h2>Why Choose JobPortal?</h2>

        <div className={styles.featureGrid}>
          <div className={styles.featureCard}>
            <h3>🤖 AI Job Matching</h3>
            <p>
              Get personalized recommendations based on your resume.
            </p>
          </div>

          <div className={styles.featureCard}>
            <h3>📄 Resume Analysis</h3>
            <p>
              Extract skills automatically and improve your profile.
            </p>
          </div>

          <div className={styles.featureCard}>
            <h3>🎯 ATS Score</h3>
            <p>
              Check resume compatibility with job descriptions.
            </p>
          </div>

          <div className={styles.featureCard}>
            <h3>📊 Skill Gap Detection</h3>
            <p>
              Learn which skills are missing for your dream job.
            </p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className={styles.cta}>
        <h2>Ready to Start Your Career Journey?</h2>

        <Link to="/jobs" className={styles.primaryBtn}>
          Explore Jobs
        </Link>
      </section>
    </div>
  );
}

export default Home;