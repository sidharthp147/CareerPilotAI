import { useState } from "react";
import styles from "./RecruiterRegister.module.css";
import api from "./api.jsx"
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

function RecruiterRegister (){
  const navigate=useNavigate();
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

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmpassword) {
      setError("Passwords do not match");
      return;
    }

    setError("");
    console.log("Form submitted:", formData);
    try{
      console.log(formData);
        const res=await api.post("http://127.0.0.1:8000/auth/RecruiterRegister",formData);
        console.log(res)
        alert("Registration Successful");
      navigate("/login");
      }
      catch (err) {
  console.log("AXIOS ERROR 👉", err);
  console.log("RESPONSE 👉", err.response);
  console.log("DATA 👉", err.response?.data);
  console.log("STATUS 👉", err.response?.status);

  setError(
    "Can't fetch data"
  );
}
  };

  return (
    <div className={styles.reg}>
          <div className={styles.container}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <h2 className={styles.title}>Register As Recruiter</h2>

        {error && <p className={styles.error}>{error}</p>}

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
            rows="4"
          />
        </div>

        <button type="submit" className={styles.button}>
          Register
        </button>
         <div className={styles.link}>
        <Link to="/login" className={styles.loginLink}>Already have an account? Login here</Link>
      </div>
      </form>
    </div>
    </div>
  );
};

export default RecruiterRegister;