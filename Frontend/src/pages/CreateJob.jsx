import { useEffect, useState } from "react";
import api from "./api.jsx";
import styles from "./CreateJob.module.css";
import { useNavigate } from "react-router";
import CreatableSelect from "react-select/creatable";

function CreateJob() {

  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    title: "",
    location: "",
    description: "",
    job_type: "",
    salary_range: "",
    experience: "",
  });

  // existing skills from DB
  const [skillOptions, setSkillOptions] = useState([]);

  // selected skills
  const [selectedSkills, setSelectedSkills] = useState([]);

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

  // form input change
  const handleChange = (e) => {

    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // submit
  const handleSubmit = async (e) => {
    if (loading) return;

    e.preventDefault();

    const token = localStorage.getItem("token");
    setLoading(true);
    try {
      const payload = {
        ...formData,
        skills: selectedSkills.map((skill) => skill.value),
      };


      await api.post(
        "/jobs/CreateJob",
        payload,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );


      alert("Job created successfully!");

      navigate("/RecruiterDashboard");

    } catch (error) {

      console.error(error);

      alert("Failed to create job");
    }
  };
return (
  <div className={styles.container}>
    <div className={styles.header}>
      <h1>Create a New Job</h1>

      <p>
        Publish opportunities and attract top talent
      </p>
    </div>

    <div className={styles.card}>
      <form
        className={styles.form}
        onSubmit={handleSubmit}
      >
        {/* Title */}
        <div className={styles.field}>
          <label>Job Title</label>

          <input
            name="title"
            placeholder="Senior Full Stack Developer"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>

        {/* Location */}
        <div className={styles.field}>
          <label>Location</label>

          <input
            name="location"
            placeholder="Bangalore"
            value={formData.location}
            onChange={handleChange}
            required
          />
        </div>

        {/* Description */}
        <div className={styles.field}>
          <label>Job Description</label>

          <textarea
            name="description"
            placeholder="Describe the role, responsibilities, and requirements..."
            value={formData.description}
            onChange={handleChange}
            required
          />
        </div>

        {/* Skills */}
        <div className={styles.field}>
          <label>Required Skills</label>

          <CreatableSelect
            isMulti
            options={skillOptions}
            value={selectedSkills}
            onChange={(selected) =>
              setSelectedSkills(selected)
            }
            isSearchable
            closeMenuOnSelect={false}
            placeholder="Select or create skills..."
            formatCreateLabel={(inputValue) =>` Add ${inputValue}`
            }
            required
          />
        </div>

        {/* Job Type */}
        <div className={styles.field}>
          <label>Job Type</label>

          <div className={styles.radioGroup}>
            <label className={styles.radioCard}>
              <input
                type="radio"
                name="job_type"
                value="Permanent"
                checked={
                  formData.job_type ===
                  "Permanent"
                }
                onChange={handleChange}
                
              />

              <span>Permanent</span>
            </label>

            <label className={styles.radioCard}>
              <input
                type="radio"
                name="job_type"
                value="Remote"
                checked={
                  formData.job_type ===
                  "Remote"
                }
                onChange={handleChange}
              />

              <span>Remote</span>
            </label>

            <label className={styles.radioCard}>
              <input
                type="radio"
                name="job_type"
                value="Part Time"
                checked={
                  formData.job_type ===
                  "Part Time"
                }
                onChange={handleChange}
              />

              <span>Part Time</span>
            </label>
          </div>
        </div>

        {/* Experience */}
        <div className={styles.field}>
          <label>Experience</label>

          <input
            type="float"
            name="experience"
            placeholder="2 years"
            value={formData.experience}
            onChange={handleChange}
            min={0}
            max={30}
            required
          />
        </div>

        {/* Salary */}
        <div className={styles.field}>
          <label>Salary Range</label>

          <input
            type="number"
            name="salary_range"
            placeholder="1200000"
            value={formData.salary_range}
            onChange={handleChange}
            required
            min={1000}
            max={99999999}
          />
        </div>

        <button
          className={styles.button}
          type="submit"
          disabled={loading}
        >
          Create Job
        </button>
      </form>
    </div>
  </div>
);
}

export default CreateJob;