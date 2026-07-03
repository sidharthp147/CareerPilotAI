import { useEffect, useState } from "react";
import api from "./api";
import {jwtDecode} from "jwt-decode";
import {useNavigate} from "react-router-dom";
function Notifications() {
    const [notifications, setNotifications] = useState([]);
    const [user, setUser] = useState(null);
    const [unreadCount, setUnreadCount] = useState(0);
    const navigate=useNavigate();

    const fetchNotifications = async () => {
        try {
            const token = localStorage.getItem("token");
            const decoded=jwtDecode(token);
            setUser(decoded.sub);
            const response = await api.get("/users/notifications",{headers: {Authorization: `Bearer ${token}`,},});
            setNotifications(response.data);
            setUnreadCount(response.data.filter((notification) => !notification.read).length);

        } catch (error) {
            console.error(error,unreadCount);
        }
    };
    // Fetch notifications from database
    useEffect(() => {
            //eslint-disable-next-line
        fetchNotifications();
    }, []);
    // Live websocket notifications
    useEffect(() => {
        if (!user) return;

        const ws = new WebSocket(`wss://career-pilot-ai-147.vercel.app/ws/usernotifications/${user}`);

        ws.onopen = () => {
        };

        ws.onmessage = (event) => {
            const notification = JSON.parse(event.data);

            setNotifications(prev => [
                notification,
                ...prev
            ]);
            setUnreadCount(prev => prev + 1);
        };

        ws.onclose = () => {
        };

        return () => ws.close();
    }, [user]);
    const handleNotificationClick = async (notification) => {
    try {
        const token = localStorage.getItem("token");

        // Mark as read in DB
        await api.put(`/users/notifications/${notification.id}`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        // Update local state
        setNotifications(prev =>
            prev.map(n =>
                n.id === notification.id
                    ? { ...n, is_read: true }
                    : n
            )
        );
        setUnreadCount(prev => prev - 1);

        // Navigate to job page
        navigate(`/jobs/${notification.job_id}`);
    }
    catch(error){
        console.error(error);
    }
};

      return (
        <div style={{ position: "relative" }}>
            {notifications.length === 0 ? (
                <p>No notifications</p>
            ) : (
                notifications.map(notification => (
    <div
        key={notification.id}
        onClick={() => handleNotificationClick(notification)}
        style={{
            cursor: "pointer",
            border: "1px solid #ddd",
            padding: "15px",
            marginBottom: "10px",
            borderRadius: "10px",
            backgroundColor:
                notification.is_read
                    ? "#fff"
                    : "#eef5ff"
        }}
    >
                        <h4>{notification.title}</h4>

                        <p>{notification.message}</p>

                        <small>
                            {new Date(
                                notification.created_at
                            ).toLocaleString()}
                        </small>
                    </div>
                ))
            )}
        </div>
    );
}


export default Notifications;