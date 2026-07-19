import { Outlet, useParams } from "react-router-dom";
import JobList from "./JobList";
import styles from "./JobsLayout.module.css";
function JobsLayout() {
  const {id}= useParams();
  return (<>
  <div className={styles.container}>
    <div className={id?styles.blur:""}>
  <JobList/>
  </div>
  <Outlet />
  </div>
  </>);
}
export default JobsLayout;
