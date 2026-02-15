import { useState } from "react";
import api from "./api.jsx"
import styles from "./CreateJob.module.css";
import { useNavigate } from "react-router";

function CreateJob() {
  const [formData, setFormData] = useState({
    heading: "",
    location: "",
    description: "",
    skills: "",
    job_type: "",
    salary_range: "",
  });
  const navigate=useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token=localStorage.getItem("token")
    console.log(token,"/n",localStorage.getItem("role"))
    try {
      const res = await api.post("https://job-portal-sfyn.onrender.com/jobs/CreateJob",formData,{headers: {Authorization:`Bearer ${token}`,},});

      console.log("Job created:", res.data);
      alert("Job created successfully!");
      navigate("/RecruiterDashboard")
      
    } catch (error) {
      console.error(error);
      alert("Failed to create job");
    }
  };

  return (
    <div className={styles.container}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <h2>Create Jobs</h2>

        <div className={styles.field}>
          <label>Job Title</label>
          <input
            name="title"
            placeholder="Job Title"
            value={formData.title}
            onChange={handleChange}
          />
        </div>

        <div className={styles.field}>
          <label>Job Location</label>
          <input
            name="location"
            placeholder="Location"
            value={formData.location}
            onChange={handleChange}
          />
        </div>

        <div className={styles.field}>
          <label>Job Description</label>
          <textarea
            name="description"
            placeholder="Job Description"
            value={formData.description}
            onChange={handleChange}
          />
        </div>

        <div className={styles.field}>
          <label>Skills Required</label>
          <textarea
            name="skills"
            placeholder="Skills Required"
            value={formData.skills}
            onChange={handleChange}
          />
        </div>

        <div className={styles.field}>
          <label>Job Type</label>
        </div>

        <div className={styles.radioGroup}>
          <label className={styles.radioItem}>
            <input
              type="radio"
              name="job_type"
              value="Permanent"
              checked={formData.job_type === "Permanent"}
              onChange={handleChange}
            />
            Permanent
          </label>

          <label className={styles.radioItem}>
            <input
              type="radio"
              name="job_type"
              value="Remote"
              checked={formData.job_type === "Remote"}
              onChange={handleChange}
            />
            Remote
          </label>

          <label className={styles.radioItem}>
            <input
              type="radio"
              name="job_type"
              value="Part Time"
              checked={formData.job_type === "Part Time"}
              onChange={handleChange}
            />
            Part Time
          </label>
        </div>

        <div className={styles.field}>
          <label>Salary</label>
          <input
            name="salary_range"
            placeholder="Salary Range"
            value={formData.salary_range}
            onChange={handleChange}
          />
        </div>

        <button type="submit">Create</button>
      </form>
    </div>
  );
}

export default CreateJob;