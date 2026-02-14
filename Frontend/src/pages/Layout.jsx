import Navbar from "./NavBar.jsx";
import { Outlet } from "react-router-dom";

export default function Layout({ isLoggedIn,setIsLoggedIn,role,setRole}) {
  return (
    <>
      <Navbar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} role={role} setRole={setRole}/>
      <main>
        <Outlet />
      </main>
    </>
  );
}