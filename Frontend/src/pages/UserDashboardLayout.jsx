import { Outlet } from "react-router-dom";
import UserDashboard from "./UserDashboard";
function UserDashboardLayout() {
  return (<>
  <UserDashboard/>
  <Outlet />
  </>);
}
export default UserDashboardLayout;