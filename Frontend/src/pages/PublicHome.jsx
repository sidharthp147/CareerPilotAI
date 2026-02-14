import { Outlet } from "react-router-dom";
import NavBar from "./NavBar.jsx";
function PublicHome() {
    return (
        <>
            <NavBar />
            <main style={{backgroundColor:"blue", color:"green"}}>  
            <Outlet />
            </main>
        </>
    );
}
export default PublicHome;