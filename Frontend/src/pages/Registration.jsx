import { Link } from "react-router-dom";
import styles from "./Registration.module.css";
import api from "./api.jsx";

import { useEffect, useState } from "react";
import CreatableSelect from "react-select/creatable";

function Registration() {

  // Password Validation
  const validatepassword = (password) => {

    const regex =/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$/;

    return regex.test(password);
  };

  const [username, setUsername] = useState("");

  const [email, setEmail] = useState("");

  // Skills
  const [skills, setSkills] = useState([]);

  // Existing skills from DB
  const [skillOptions, setSkillOptions] = useState([]);

  const [experience, setExperience] = useState("");

  const [resume, setResume] = useState(null);

  const [password, setPassword] = useState("");

  const [confirmpassword, setConfirmpassword] = useState("");

  const [error, setError] = useState("");

  const [loading, setLoading] = useState(false);

  // Fetch skills from backend
  useEffect(() => {

    const fetchSkills = async () => {

      try {

        const res = await api.get("/auth/skills");


        const formattedSkills = res.data.skills.map((skill) => ({
          value: skill.skill,
          label: skill.skill,
          
        }));
        
        setSkillOptions(formattedSkills);


      } catch (err) {

        console.error(err);

      }
    };

    fetchSkills();

  }, []);

  // Resume Upload
  const handleFileChange = (e) => {

    const file = e.target.files[0];

    if (!file) return;

    if (file.type !== "application/pdf") {

      setError("Only PDF files are allowed");

      return;
    }

    const maxSize = 2 * 1024 * 1024;

    if (file.size > maxSize) {

      setError("File size exceeds 2MB");

      return;
    }

    setResume(file);

    setError("");
  };

  // Form Submit
  const handleSubmit = async (e) => {

    e.preventDefault();

    if (loading) return;

    if (!validatepassword(password)) {

      setError(
        "Password must contain uppercase, lowercase, number and special character."
      );

      return;
    }

    if (password !== confirmpassword) {

      setError("Passwords do not match");

      return;
    }

    try {

      setLoading(true);

      setError("");

      const formData = new FormData();

      formData.append("username", username);

      formData.append("email", email);

      formData.append("password", password);

      formData.append("confirmpassword", confirmpassword);

      formData.append("experience", experience);

      // Send only skill names
      formData.append(
        "skills",
        JSON.stringify(
          skills.map((skill) => skill.value)
        )
      );

      if (resume) {

        formData.append("file", resume);

      }

      

      await api.post(
        "/auth/registration",
        formData
      );


      localStorage.setItem("email", email);

      alert(
        "Registration Successful! Please verify your email."
      );

    } catch (err) {

      console.error(err.response);

      setError(
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Something went wrong"
      );

    } finally {

      setLoading(false);

    }
  };

  return (
  <div className={styles.container}>
    {/* Left Section */}
    <div className={styles.leftPanel}>
      <h1>
        Find Your <span>Dream Job</span>
      </h1>

      <p>
        Join thousands of candidates using AI-powered job matching,
        resume analysis, and skill gap detection.
      </p>

      <div className={styles.feature}>
        🤖 AI Job Recommendations
      </div>

      <div className={styles.feature}>
        📄 Resume Analysis
      </div>

      <div className={styles.feature}>
        🎯 ATS Score
      </div>

      <div className={styles.feature}>
        📊 Skill Gap Detection
      </div>
    </div>

    {/* Right Section */}
    <div className={styles.card}>
      <h2>Create Account</h2>

      <p className={styles.subtitle}>
        Start your career journey today
      </p>

      {error && (
        <div className={styles.error}>
          {error}
        </div>
      )}

      <form
        onSubmit={handleSubmit}
        className={styles.form}
      >
        {/* Username */}
        <div className={styles.formGroup}>
          <label>Username</label>

          <input
            type="text"
            value={username}
            onChange={(e) =>
              setUsername(e.target.value)
            }
            required
          />
        </div>

        {/* Email */}
        <div className={styles.formGroup}>
          <label>Email</label>

          <input
            type="email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            required
          />
        </div>

        {/* Skills */}
        <div className={styles.formGroup}>
          <label>Skills</label>

          <CreatableSelect
            isMulti
            options={skillOptions}
            value={skills}
            onChange={(selected) =>
              setSkills(selected)
            }
            isSearchable
            closeMenuOnSelect={false}
            placeholder="Select or create skills..."
            formatCreateLabel={(inputValue) =>`Add ${inputValue}`
            }
          />
        </div>

        {/* Experience */}
        <div className={styles.formGroup}>
          <label>Experience (years)</label>

          <input
            type="number"
            value={experience}
            onChange={(e) =>
              setExperience(e.target.value)
            }
            required
          />
        </div>

        {/* Resume */}
        <div className={styles.formGroup}>
          <label>Upload Resume (PDF)</label>

          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
          />
        </div>

        {/* Password */}
        <div className={styles.formGroup}>
          <label>Password</label>

          <input
            type="password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            required
          />
        </div>

        {/* Confirm Password */}
        <div className={styles.formGroup}>
          <label>Confirm Password</label>

          <input
            type="password"
            value={confirmpassword}
            onChange={(e) =>
              setConfirmpassword(
                e.target.value
              )
            }
            required
          />
        </div>

        <button
          className={styles.button}
          disabled={loading}
        >
          {loading
            ? "Creating Account..."
            : "Create Account"}
        </button>
      </form>

      <div className={styles.links}>
        <Link to="/RecruiterRegister">
          Register as Recruiter
        </Link>

        <Link to="/login">
          Already have an account? Login
        </Link>
      </div>
    </div>
  </div>
);
} 

export default Registration;