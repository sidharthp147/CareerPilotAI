import { useEffect, useState } from "react";
import api from "./api";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from "react-router-dom";

function Notifications() {
    const [notifications, setNotifications] = useState([]);
    const [user, setUser] = useState(null);
    const [unreadCount, setUnreadCount] = useState(0);

    const navigate = useNavigate();

    const fetchNotifications = async () => {
        try {
            const token = localStorage.getItem("token");
            if (!token) return;

            const decoded = jwtDecode(token);
            setUser(decoded.sub);

            const response = await api.get("/users/notifications", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            setNotifications(response.data);
            setUnreadCount(
                response.data.filter(
                    (notification) => !notification.is_read
                ).length
            );
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchNotifications();
        // eslint-disable-next-line
    }, []);

    useEffect(() => {
        if (!user) return;

        const ws = new WebSocket(
            `${import.meta.env.VITE_API_URL_WS}/ws/usernotifications/${user}`
        );

        ws.onmessage = (event) => {
            const notification = JSON.parse(event.data);

            setNotifications((prev) => [notification, ...prev]);

            setUnreadCount((prev) => prev + 1);
        };

        ws.onerror = (error) => {
            console.error(error);
        };

        return () => ws.close();
    }, [user]);

    const handleNotificationClick = async (notification) => {
        try {
            const token = localStorage.getItem("token");

            await api.put(`/users/notifications/${notification.id}`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            setNotifications((prev) =>
                prev.map((n) =>
                    n.id === notification.id
                        ? { ...n, is_read: true }
                        : n
                )
            );

            if (!notification.is_read) {
                setUnreadCount((prev) => Math.max(prev - 1, 0));
            }

            navigate(`/jobs/${notification.job_id}`);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div
            style={{
                maxWidth: "900px",
                margin: "0 auto",
                padding: "16px",
                width: "100%",
                boxSizing: "border-box",
                minHeight: "100vh",
            }}
        >
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    flexWrap: "wrap",
                    gap: "10px",
                    marginBottom: "20px",
                }}
            >
                <h2
                    style={{
                        margin: 0,
                        fontSize: "28px",
                    }}
                >
                    Notifications
                </h2>

                <span
                    style={{
                        background: "#2563eb",
                        color: "#fff",
                        padding: "8px 16px",
                        borderRadius: "20px",
                        fontWeight: "600",
                        fontSize: "14px",
                    }}
                >
                    {unreadCount} Unread
                </span>
            </div>

            {notifications.length === 0 ? (
                <div
                    style={{
                        textAlign: "center",
                        padding: "60px 20px",
                        color: "#666",
                        border: "1px solid #ddd",
                        borderRadius: "12px",
                        background: "#fafafa",
                    }}
                >
                    <h3>No Notifications</h3>
                    <p>You don't have any notifications yet.</p>
                </div>
            ) : (
                notifications.map((notification) => (
                    <div
                        key={notification.id}
                        onClick={() =>
                            handleNotificationClick(notification)
                        }
                        style={{
                            cursor: "pointer",
                            border: "1px solid #e5e7eb",
                            padding: "18px",
                            marginBottom: "16px",
                            borderRadius: "14px",
                            backgroundColor: notification.is_read
                                ? "#ffffff"
                                : "#eef5ff",
                            boxShadow:
                                "0 2px 8px rgba(0,0,0,0.08)",
                            transition: "0.2s",
                            width: "100%",
                            boxSizing: "border-box",
                            wordBreak: "break-word",
                        }}
                    >
                        <h4
                            style={{
                                margin: "0 0 10px",
                                fontSize: "18px",
                                color: "#222",
                            }}
                        >
                            {notification.title}
                        </h4>

                        <p
                            style={{
                                margin: "0 0 12px",
                                color: "#555",
                                lineHeight: "1.6",
                                fontSize: "15px",
                            }}
                        >
                            {notification.message}
                        </p>

                        <div
                            style={{
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                flexWrap: "wrap",
                                gap: "10px",
                            }}
                        >
                            <small
                                style={{
                                    color: "#777",
                                }}
                            >
                                {new Date(
                                    notification.created_at
                                ).toLocaleString()}
                            </small>

                            {!notification.is_read && (
                                <span
                                    style={{
                                        background: "#2563eb",
                                        color: "#fff",
                                        padding: "4px 10px",
                                        borderRadius: "12px",
                                        fontSize: "12px",
                                        fontWeight: "600",
                                    }}
                                >
                                    New
                                </span>
                            )}
                        </div>
                    </div>
                ))
            )}
        </div>
    );
}

export default Notifications;