import { Outlet } from "react-router-dom";
import JobList from "./JobList";
function JobsLayout() {
  return (<>
  <JobList/>
  <Outlet />
  </>);
}
export default JobsLayout;
