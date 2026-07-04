import { useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from "react-router-dom";
import api from "./api";

function NotificationBell() {
    const [unreadCount, setUnreadCount] = useState(0);
    const navigate = useNavigate();

    // Load unread count from DB when component mounts
    useEffect(() => {
        const fetchUnreadCount = async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return;

                const response = await api.get("/users/aaaaaaaaaaa",{headers: {Authorization: `Bearer ${token}`,},});
                
                setUnreadCount(response.data.count);
            } catch (error) {
                console.error(error);
            }
        };

        fetchUnreadCount();
    }, []);

    // Connect websocket for live updates
    useEffect(() => {
        const token = localStorage.getItem("token");

        if (!token) return;

        const decoded = jwtDecode(token);

        const ws = new WebSocket(`wss://careerpilotai-production-d61a.up.railway.app/ws/usernotifications/${decoded.sub}`);

        ws.onopen = () => {
        };

        ws.onmessage = (event) => {
            const data= JSON.parse(event.data);
            if (data.type=="notification_read") {
                setUnreadCount(prevCount => prevCount - 1);
                return;
            }
          }

        ws.onclose = () => {
        };

        return () => ws.close();
    }, []);

    return (
        <div
            onClick={() => navigate("/Notifications")}
            style={{
                position: "relative",
                cursor: "pointer",
                display: "inline-block"
            }}
        >
            <span style={{ fontSize: "22px" }}>
                🔔
            </span>

            {unreadCount > 0 && (
                <span
                    style={{
                        position: "absolute",
                        top: "-8px",
                        right: "-10px",
                        backgroundColor: "red",
                        color: "white",
                        borderRadius: "50%",
                        width: "18px",
                        height: "18px",
                        fontSize: "12px",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center"
                    }}
                >
                    {unreadCount}
                </span>
            )}
        </div>
    );
}

export default NotificationBell;