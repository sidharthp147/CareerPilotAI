import { Outlet } from "react-router-dom";
import ForgotPassword from "./ForgotPassword"; 
function PasswordLayout(){
  return (<>
  <ForgotPassword/>
  <Outlet />
  </>);
}
export default PasswordLayout;