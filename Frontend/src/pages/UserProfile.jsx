import { useEffect, useState } from "react";
import api from "./api.jsx";
import styles from "./UserProfile.module.css";
import CreatableSelect from "react-select/creatable";
import { Form } from "react-router";
import { useNavigate } from "react-router-dom";

function UserProfile() {

  const [formData, setFormData] = useState({
    username: "",
    password: "",
    confirmpassword: "",
    experience: 0,
  });
  const [resumeurl,setResumeurl]=useState("");

  const [changed, setChanged] = useState(false);
  // existing skills from DB
  const [skillOptions, setSkillOptions] = useState([]);

  // selected skills
  const [selectedSkills, setSelectedSkills] = useState([]);

  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  // fetch profile + skills
  useEffect(() => {

    fetchProfile();

    fetchSkills();

  }, []);

  // fetch all skills
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

  // fetch current user profile
  const fetchProfile = async () => {

    try {

      const token = localStorage.getItem("token");

      const res = await api.get("/users/Userprofiles",{headers: {Authorization:`Bearer ${token}`,},});



      setFormData(prev=>({...prev,username: res.data.name,experience: res.data.experience}));
      setResumeurl(res.data.resume_url)

      // convert string -> react select format
      if (res.data.skills) {

        const formattedSkills =
          res.data.skills
            .split(",")
            .map((skill) => ({
              value: skill.trim(),
              label: skill.trim(),
            }));

        setSelectedSkills(formattedSkills);
      }


    } catch (err) {

      console.error(err);
    }
  };

  // input change
  const handleChange = (e) => {
    setChanged(true);

    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // file change
  const handleFileChange = (e) => {
    setChanged(true);
    const file = e.target.files[0];

    if (!file) return;

    if (file.type !== "application/pdf") {

      alert("Only PDF allowed");

      return;
    }
    setFile(file);

  };

  // update profile
  const handleSubmit = async (e) => {

    e.preventDefault();

    try {

      setLoading(true);

      const token = localStorage.getItem("token");

      const data = new FormData();
      if (formData.username)
      data.append(
        "username",
        formData.username
      );
      if (formData.password)
      data.append(
        "password",
        formData.password
      );
      if (formData.confirmpassword)
      data.append(
        "confirmpassword",
        formData.confirmpassword
      );
      if (formData.experience)
      data.append(
        "experience",
        formData.experience
      );

      // skills array -> string
      if (selectedSkills)
      data.append(
        "selectedSkills",
        JSON.stringify(
          selectedSkills.map(
            (skill) => skill.value
          )
        )
      );

      if (file) {

        data.append(
          "file",
          file
        );
        
      }
      const validatepassword = (password) => {

    const regex =/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$/;

    return regex.test(password);
  };
    if(formData.password){
      if (!validatepassword(formData.password)) {

        alert(
          "Password must contain uppercase, lowercase, number and special character."
        );

        return;
      }}
      if (formData.password !== formData.confirmpassword) {

      alert("Passwords do not match");

      return;}
    
      await api.put(
        "/users/updateprofile",
        data,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert("Profile updated successfully");
      navigate("/UserDashboard");

    } catch (err) {

      console.error(err.response?.data);

      alert("Failed to update profile");

    } finally {

      setLoading(false);

    }
  };

 return (
  <div className={styles.container}>
    <div className={styles.profileHeader}>
      <h1>My Profile</h1>
      <p>
        Manage your skills, experience, and resume
      </p>
    </div>

    <div className={styles.profileCard}>
      <form
        className={styles.form}
        onSubmit={handleSubmit}
      >
        {/* Username */}
        <div className={styles.field}>
          <label>Username</label>

          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
          />
        </div>
        <div className={styles.field}>
          <label>Password</label>

          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
        </div>
        <div className={styles.field}>
          <label>Confirm Password</label>

          <input
            type="password"
            name="confirmpassword"
            value={formData.confirmpassword}
            onChange={handleChange}
          />
        </div>

        {/* Skills */}
        <div className={styles.field}>
          <label>Skills</label>

          <CreatableSelect
            isMulti
            options={skillOptions}
            value={selectedSkills}
            onChange={(selected) =>{
              setSelectedSkills(selected)
              setChanged(true)}
            }
            isSearchable
            closeMenuOnSelect={false}
            placeholder="Select or create skills..."
            formatCreateLabel={(inputValue) =>`Add ${inputValue}`
            }
            styles={{control:(base)=>({
              ...base,
              borderColor: "#dbeafe !important",
              outline: "none !important",
              boxShadow: "none !important",
              "&:hover": {borderColor: "#dbeafe"},
            }),}}
          />
        </div>

        {/* Experience */}
        <div className={styles.field}>
          <label>Experience (Years)</label>

          <input
            type="number"
            name="experience"
            value={formData.experience}
            onChange={handleChange}
          />
        </div>

        {/* Resume */}
        {resumeurl && (
          <div className={styles.resumeBox}>
            <h4>Current Resume</h4>

            <a
              href={resumeurl}
              target="_blank"
              rel="noopener noreferrer"
            >
              View Resume
            </a>
          </div>
        )}

        <div className={styles.field}>
          <label>Upload New Resume</label>

          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
          />
        </div>
        
        <button
          type="submit"
          className={styles.button}
          disabled={!changed}
        >
          {loading
            ? "Updating..."
            : "Update Profile"}
        </button>
      </form>
    </div>
  </div>
);
}

export default UserProfile;