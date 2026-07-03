import {
  useEffect,
  useState,
  useCallback,
  useRef,
} from "react";
import {Joyride} from "react-joyride";

import { FaInfoCircle } from "react-icons/fa";
import styles from "./JobList.module.css";

import { useNavigate } from "react-router-dom";

import api from "./api.jsx";

import { FaSearch } from "react-icons/fa";

const LIMIT = 9;

const SEARCH_DEBOUNCE_MS = 3000;

function JobList() {

  const navigate = useNavigate();

  const wsRef = useRef(null);

  const [error, setError] = useState("");

  const [jobs, setJobs] = useState([]);

  const [search, setSearch] = useState("");

  const [jobType, setJobType] = useState("");

  const [location, setLocation] = useState("");
  const steps = [
 
    {
    target: "#search-bar",
    content: "Search jobs by title, skill, or keyword.and You can apply directly with search eg-apply to top 5 python developer jobs in bangalore",
  },
  {
    target: "#filters",
    content: "Use filters to narrow down results.",
  },
  {
    target: "#job-card",
    content: "Click on view details to see more job details.",
  },
  {
    target: "#apply-button",
    content: "Apply for jobs using this button.",
  },
];

  const [page, setPage] = useState(1);

  const [runTour, setRunTour] = useState(false);


  const [total, setTotal] = useState(0);
   
  const [count,setCount]=useState(0);

  const [apply, setApply] = useState(false);

  const [streaming, setStreaming] = useState(false);

  const [savedJobs, setSavedJobs] = useState(new Set());

  const [role, setRole] = useState("");

  const [hasSearched, setHasSearched] =
    useState(false);

  const [keywords, setKeywords] =
    useState([]);

  const [filtered, setFiltered] =
    useState([]);

  const [showSuggestions, setShowSuggestions] =
    useState(true);
  const [applyResults, setApplyResults] = useState([]);
  const [showModal, setShowModal] = useState(false);

  const totalPages = Math.ceil(
    total / LIMIT
  );
  const [jobsCount, setJobsCount] = useState(0);
  // =========================
  // FETCH KEYWORDS
  // =========================

  useEffect(() => {

    const fetchKeywords = async () => {

      try {

        const res = await api.get(
          "/jobs/keywords"
        );

        setKeywords(res.data);

      } catch (err) {

        console.error(err);
      }
    };

    fetchKeywords();

  }, []);
  useEffect(() => {
    const hasSeenTour = localStorage.getItem("jobTourSeen");

    if (!hasSeenTour) {
      setRunTour(true);
      localStorage.setItem("jobTourSeen", "true");
    }
  }, []);

  // =========================
  // FILTER SUGGESTIONS
  // =========================

  useEffect(() => {

    if (
      !search.trim() ||
      !showSuggestions
    ) {

      setFiltered([]);

      return;
    }
    const filteredKeywords =
      keywords.filter((keyword) =>
        keyword
          .toLowerCase()
          .includes(
            search.toLowerCase()
          )
      );

    setFiltered(
      filteredKeywords.slice(0, 5)
    );

  }, [
    search,
    keywords,
    showSuggestions,
  ]);



  // =========================
  // WEBSOCKET CONNECTION
  // =========================

  useEffect(() => {

    const token =
      localStorage.getItem(
        "token"
      );

    let manuallyClosed = false;

    wsRef.current =
      new WebSocket(`wss://careerpilotai-production-d61a.up.railway.app//ai/ai?token=${token}`);
      

    wsRef.current.onopen = () => {

    

      // INITIAL FETCH
      //eslint-disable-next-line
      fetchJobs();
    };

    wsRef.current.onmessage = (
      event
    ) => {

      const response = JSON.parse(
        event.data
      );

     

      // STREAM JOBS

      if (
        response.type === "job"
      ) {

        setJobs((prev) => [
          ...prev,
          response.job,
        ]);
      }

      // TOTAL

      if (
        response.type === "total"
      ) {

        setTotal(
          response.total
        );
      }
      if (
        response.type === "confirmation_required"
      ) { 
        setCount(response.count);
        setTotal(response.total);

        setApply(
          response.apply
        );
      }
      // DONE

      if (
        response.type === "done"
      ) {

        setStreaming(false);
      }
      if (response.type === "Application_Status")
      {
        alert(`Application Status: ${response.status}`);
      }
      if (response.type === "apply_result") {
        setApplyResults(response.result);
        setShowModal(true);
}

      // ERROR

      if (
        response.error
      ) {

        setError(
          response.error
        );

        setStreaming(false);
      }
    };

    wsRef.current.onerror = (
      err
    ) => {
      console.error(err)

     

      setStreaming(false);

      setError(
        "WebSocket connection failed"
      );
    };

    wsRef.current.onclose = (
      event
    ) => {
      console.error(event)

      

      if (
        manuallyClosed
      ) {

        return;
      }
    };

    return () => {

      manuallyClosed = true;

      if (
        wsRef.current
      ) {

        wsRef.current.close(
          1000,
          "Component unmounted"
        );
      }
    };

  }, []);
 
  useEffect(() => {
    setJobsCount(Math.min(total , count));
  }, [total, count]);
  // =========================
  // FETCH JOBS
  // =========================

  const fetchJobs =
    useCallback(() => {
      setApply(false);
      setCount(0);
      setJobsCount(0);
      setTotal(0);

      if (
        !wsRef.current
      ) {

        

        return;
      }

      if (
        wsRef.current
          .readyState !==
        WebSocket.OPEN
      ) {

       
        return;
      }

      try {

        setError("");

        setStreaming(true);

        setJobs([]);

        const offset =
          (page - 1) * LIMIT;

        wsRef.current.send(
          JSON.stringify({
            message: search,
            job_type:
              jobType,
            location:
              location,
            limit: LIMIT,
            offset:
              offset,
          })
        );

        

      } catch (err) {

        console.error(err);

        setStreaming(false);

        setError(
          "Cannot fetch jobs"
        );
      }

    }, [
      search,
      jobType,
      location,
      page,
    ]);

  // =========================
  // SEARCH DEBOUNCE
  // =========================

  useEffect(() => {
    if (search.trim() === "") {
      fetchJobs();
    }
    if(!search ) {

      
      return;

    }

    const delay =
      setTimeout(() => {
        setShowSuggestions(false);
        setFiltered([]);

        setPage(1);

        setHasSearched(
          true
        );

        fetchJobs();

      }, SEARCH_DEBOUNCE_MS);

    return () =>
      clearTimeout(delay);

  }, [
    search,
    jobType,
    location,
  ]);

  // =========================
  // PAGE CHANGE
  // =========================

  useEffect(() => {

      fetchJobs();
  
  }, [page]);
  useEffect(() => {
    const loadsavedjobs=async () => {
      try
      {
      const token=localStorage.getItem("token");
      const role=localStorage.getItem("role");
      setRole(role);
      const response=await api.get("/jobs/savedjobs",{
        headers: {
          "Authorization":`Bearer ${token}`
        }
      });
      setSavedJobs(new Set(response.data));
    
  }
    catch(err){
      console.error(err);
  }
  }
  loadsavedjobs();
  }, []);

  // =========================
  // SEARCH BUTTON
  // =========================

  const handleSearch = () => {  
    setShowSuggestions(false);
    setFiltered([]);

    setPage(1);

    setHasSearched(true);
    fetchJobs();
  };
  const handleApply = () => {
    const confirmed=window.confirm("Are you sure you want to apply for the jobs listed?");
    if (!confirmed) {
      return;
    }
    const job_ids=jobs.slice(0,count).map(job=>job.id);
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN)
    {
    wsRef.current.send(JSON.stringify({type:"apply_confirmation",job_ids:job_ids}));
    }}
  const handleSave =async (job_id) => {
    const token=localStorage.getItem("token");
    if (token != null)
    {
      if (savedJobs.has(job_id))
      {
        try
        {
        const response=await api.post("/jobs/unsave",{"job_id":job_id},{
        headers:{
          "Authorization":`Bearer ${token}`}
        });
        
        
        if (response.data.status=="success")
        {
          setSavedJobs(prev=>{
            const updated=new Set(prev);
            updated.delete(job_id);
            return updated;});
          }
          return;
        }
        catch(err)
        {
          console.error(err);
        }
      }
      try{
      const response=await api.post("/jobs/save",{"job_id":job_id},{
          headers:{
            "Authorization":`Bearer ${token}`}
        });
        if (response.data.status=="success")
        {
          setSavedJobs(prev=> new Set([...prev,job_id]));
        }
      }
      catch(err)
      {
        console.error(err);
      }
    }
  }
  

  return (

    <div
      className={
        styles.container
      }
    >

      <FaInfoCircle style={{cursor:"pointer",fontSize:"20px"}}
      title="Show Guide"
      onClick={()=>setRunTour(true)}/><span> Show Guidelines</span>
          <Joyride
        steps={steps}
        run={runTour}
        continuous
        showSkipButton
        showProgress
        disableScrolling={false}
      />
      {showModal && (
  <div className={styles.modalOverlay}>
    <div className={styles.modal}>
      <h2>Application Results</h2>

      {applyResults.map((res) => (
        <div
          key={res.job_id}
          className={styles.resultRow}
        >
          <span>Job #{res.job_id}</span>

          <span
            className={
              res.status.includes("Success")
                ? styles.success
                : styles.warning
            }
          >
            {res.status}
          </span>
        </div>
      ))}

      <button
        onClick={() =>
          setShowModal(false)
        }
      >
        Close
      </button>
    </div>
  </div>
)}
      <div
        className={
          styles.wrapper
        }
      >

        

          <h2
            className={
              styles.title
            }
          >
            Find Your <span className={styles.highlight}>Dream Job</span>
          </h2>
          <div>
          <h3 style={{textAlign:"center"}}>
              Discover opportunities that match your skills and experience.
          </h3>
          </div>
        

        {error && error=="Invalid token" &&  (

          <p
            className={
              styles.error
            }
          >
            Loading...Please wait or refresh the page if it takes too long.
          </p>
        )}
        {error && error!=="Invalid token" &&  (<p
            className={
              styles.error
            }
          >{error}
          </p>
        )}

        {/* SEARCH */}

        <div
          className={
            styles.searchWrapper
          }
        >

          <input
            id="search-bar"
            type="search"
            placeholder="Search jobs, skills..."
            value={search}
            onChange={(e) => {

              setSearch(
                e.target.value
              );

              setShowSuggestions(
                true
              );
            }}
            className={
              styles.searchInput
            }
          />

          {/* SUGGESTIONS */}

          {filtered.length >
            0 && (

            <div
              className={
                styles.suggestions
              }
            >

              {filtered.map(
                (
                  item,
                  index
                ) => (

                  <h4
                    key={
                      index
                    }
                    onClick={() => {

                      setSearch(
                        item
                      );

                      setFiltered(
                        []
                      );

                      setShowSuggestions(
                        false
                      );
                    }}
                  >

                    <FaSearch
                      style={{
                        marginRight:
                          "15px",
                      }}
                      size={
                        13
                      }
                    />

                    {item}

                  </h4>
                )
              )}

            </div>
          )}

          {/* JOB TYPE */}

          <select id="filters"
            value={jobType}
            onChange={(e) =>
              setJobType(
                e.target
                  .value
              )
            }
          >

            <option value="">
              All Types
            </option>

            <option value="Permanent">
              Permanent
            </option>

            <option value="Remote">
              Remote
            </option>

            <option value="Part Time">
              Part Time
            </option>

          </select>

          {/* LOCATION */}

          <select
            value={location}
            onChange={(e) =>
              setLocation(
                e.target
                  .value
              )
            }
          >

            <option value="">
              All Locations
            </option>

            <option value="Bangalore">
              Bangalore
            </option>

            <option value="Chennai">
              Chennai
            </option>

          </select>

          {/* SEARCH BUTTON */}

          <button
            onClick={
              handleSearch
            }
            className={
              styles.searchBtn
            }
          >
            Search
          </button>

        </div>

        {/* STREAMING */}

        {streaming && (

          <p
            className={
              styles.loading
            }
          >
            AI searching jobs...
          </p>
        )}

        {/* EMPTY */}

        {!streaming &&
          jobs.length ===
            0 &&
          hasSearched && (

            <p
              className={
                styles.empty
              }
            >
              No jobs found 🚀
            </p>
          )}

        {/* JOBS */}

        <div id="job-card"
          className={
            styles.jobs
          }
        >
        
          {jobs.map(
            (job) => (

              <div
                key={job.id}
                className={
                  styles.card
                }
              >
                <div className={styles.cardContent}>

                <div
                  className={
                    styles.cardTop
                  }
                >

                  <h3>
                    {
                      job.heading.charAt(0).toUpperCase()+job.heading.slice(1)
                    }
                  </h3>

                </div>

                <p
                  className={
                    styles.meta
                  }
                >
                  📍<b>{" "}
                  {
                    job.location
                  }
                  </b>
                </p>

                <div
                  className={
                    styles.badge
                  } style={{width:"100px",color:"black"}}
                >
                  {
                    job.job_type
                  }
                </div>
                <p
                  className={
                    styles.jobId
                  }
                >
                  Job ID:{" "}
                  {job.id}
                </p>

                <div className={styles.skillSection}>
                  <p className={styles.skillsTitle}  style={{marginBottom:"18px"}}>
                  <b>Required Skills:</b>
                  </p>
  {job.skills.split(",").slice(0, 5).map(skill => (
  <span key={skill} className={styles.skillChip1}>
    {skill.trim()}
  </span>
))}
<br></br>
{job.skills.split(",").length > 5 && (
  <span className={styles.moreSkills}>+{job.skills.split(",").length - 5} More</span>
)}
</div>

                <p className={styles.salary}><b>
                  Salary</b>:{" "}
                  {
                    job.salary_range
                  }
                  
                </p>

                {/* SEMANTIC SCORE */}

                {job.final_score && (
  <div className={styles.scoreSection}>
    <div className={styles.scoreHeader}>
      <span>Match Score</span>

      <span>
        {(job.final_score * 100).toFixed(0)}%
      </span>
    </div>

    <div className={styles.progressBar}>
      <div
        className={styles.progressFill}
        style={{
          width: `${job.final_score * 100}%`
        }}
      />
    </div>
  </div>
)}
{job.skills_score >0  && (
<div style={{marginTop:"10px"}}>
                  Skills Score :
{job.skills_score}
</div>)}
{job.title_score > 0 && (
<div style={{marginTop:"10px"}}>
                  Title Score :
{job.title_score}
</div>)}
{job.location_score > 0 && (
<div style={{marginTop:"10px"}}>
                  Location Score :
{job.location_score}
</div>)
}
                {/* MATCHED SKILLS */}

                {job.matched_skills?.length > 0 && (
  <div className={styles.skillsSection}>
    <p className={styles.skillsTitle}>
      <b>Matched Skills</b>
    </p>

    <div className={styles.skillContainer}>
      {job.matched_skills.map(
        (skill) => (
          <span
            key={skill}
            className={styles.skillChip}
          >
            ✓ {skill}
          </span>
        )
      )}
    </div>
  </div>
)}

                {/* SUGGESTIONS */}

                {job.suggestions && (

                  <p>

                    <b>Suggestions:</b>{" "}

                    {job.suggestions
                      .map(
                        (
                          skill
                        ) =>
                          skill
                            .charAt(
                              0
                            )
                            .toUpperCase() +
                          skill.slice(
                            1
                          )
                      )
                      .join(
                        ", "
                      )}

                  </p>
                )}
                </div>

                {/* VIEW DETAILS */}
                <div className={styles.btnContainer}>
                <button
                  onClick={() =>
                    navigate(`/jobs/${job.id}`)
                    
                  }
                  className={
                    styles.btn
                  }
                >
                  View More Details
                </button>
                {role==="USER" &&(
                  <button className={styles.btn} onClick={()=>handleSave(job.id)}> {savedJobs.has(job.id)? "Unsave Job":"Save Job"}</button>)
                }</div>

              </div>
            )
          )}
         

        </div>
          {count > 0 && apply && (
  <div className={styles.bulkApplyContainer}>
    <p className={styles.bulkApplyInfo}>
      {jobsCount} matching jobs found. Apply to all with one click.
    </p>

    <button id="apply-button"
      className={styles.bulkApplyBtn}
      onClick={handleApply}
    >
      🚀 Apply to {jobsCount} {jobsCount > 1 ? "Jobs" : "Job"}
    </button>
  </div>
)}
        

        {/* PAGINATION */}

        <div
          className={
            styles.pagination
          }
        >

          <button
            onClick={() =>
              setPage(
                (
                  prev
                ) =>
                  Math.max(
                    prev -
                      1,
                    1
                  )
              )
            }
            disabled={
              page === 1
            }
          >
            Previous
          </button>

          <span>
            Page {page} of{" "}
            {totalPages ||
              1}
          </span>

          <button
            onClick={() =>
              setPage(
                (
                  prev
                ) =>
                  page >=
                  totalPages
                    ? prev
                    : prev +
                        1
              )
            }
            disabled={
              page ===
                totalPages ||
              totalPages ===
                0
            }
          >
            Next
          </button>

        </div>

      </div>

    </div>
  );
}

export default JobList;