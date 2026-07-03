import axios from "axios";
const api = axios.create({
  baseURL: "https://career-pilot-ai-147.vercel.app",
  withCredentials: true
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
  });
  api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (originalRequest.url.includes("/auth/refresh")) {
      localStorage.removeItem("token");
      window.location.href = "/login";
      return Promise.reject(error);
    }
    if (originalRequest.url === "/auth/login") {
      return Promise.reject(error);
    }
    if (
      error.response?.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        
        const res = await api.post("/auth/refresh");
        const newToken = res.data.token;
        localStorage.setItem("token", newToken);
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        window.location.reload();
        return api(originalRequest);
      } catch (err) {
        localStorage.removeItem("token");
        window.location.href = "/login";
        return Promise.reject(err);
      }
    }
    else if (
      error.response?.status_code === 429) {
      alert("Too many requests. You Are Blocked For 1 Hour.");
      return Promise.reject(error);
    } 
    else if (
      error.response?.status_code === 403) {
        const remaining_minutes=error.response.data.content.remaining_seconds;
        alert(`Access Denied.You Are Temporarily Blocked for ${Math.floor(remaining_minutes/60)} minutes`);
        return Promise.reject(error);
      }
    return Promise.reject(error);
  }
  
);

export default api;