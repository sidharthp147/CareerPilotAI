import { useState } from "react";
import styles from "./RecruiterRegister.module.css";
import api from "./api.jsx"
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

function RecruiterRegister (){
  const navigate=useNavigate();
  const [loading,setLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmpassword: "",
    company_name: "",
    company_description: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };
  const validatepassword = (password) => {

    const regex =/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$/;

    return regex.test(password);
  };

  const handleSubmit = async (e) => {
    
    e.preventDefault();
    if(loading) return;
    setLoading(true);
    if (!validatepassword(formData.password)) {
      setError(
        "Password must contain uppercase, lowercase, number and special character."
      );
      return;
    }
    if (formData.password !== formData.confirmpassword) {
      setError("Passwords do not match");
      return;
    }

    setError("");
    try{
        await api.post("/auth/RecruiterRegister",formData);
        alert("Registration Successful");
      navigate("/login");
      }
      catch (err) {
        console.error(err)
        setLoading(false);

  setError(
    "Can't fetch data"
  );
}
  setLoading(false);
  };

 return (
  <div className={styles.container}>
    {/* Left Section */}
    <div className={styles.leftPanel}>
      <h1>
        Hire <span>Top Talent</span>
      </h1>

      <p>
        Reach qualified candidates faster with AI-powered
        candidate matching and resume analysis.
      </p>

      <div className={styles.feature}>
        🎯 AI Candidate Ranking
      </div>

      <div className={styles.feature}>
        📄 Resume Screening
      </div>

      <div className={styles.feature}>
        ⚡ Faster Hiring Process
      </div>

      <div className={styles.feature}>
        📊 Recruiter Analytics
      </div>
    </div>

    {/* Right Section */}
    <div className={styles.card}>
      <h2>Recruiter Registration</h2>

      <p className={styles.subtitle}>
        Start hiring smarter today
      </p>

      {error && (
        <div className={styles.error}>
          {error}
        </div>
      )}

      <form
        className={styles.form}
        onSubmit={handleSubmit}
      >
        <div className={styles.field}>
          <label>Email</label>

          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.field}>
          <label>Password</label>

          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.field}>
          <label>Confirm Password</label>

          <input
            type="password"
            name="confirmpassword"
            value={formData.confirmpassword}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.field}>
          <label>Company Name</label>

          <input
            type="text"
            name="company_name"
            value={formData.company_name}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.field}>
          <label>Company Description</label>

          <textarea
            name="company_description"
            value={formData.company_description}
            onChange={handleChange}
            rows="5"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className={styles.button}
        >
          {loading
            ? "Creating Account..."
            : "Create Recruiter Account"}
        </button>
      </form>

      <div className={styles.links}>
        <Link to="/Register">
          Register as Job Seeker
        </Link>

        <Link to="/login">
          Already have an account? Login
        </Link>
      </div>
    </div>
  </div>
);
};

export default RecruiterRegister;