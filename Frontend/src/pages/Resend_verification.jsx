import { useState } from "react";
import api from "./api";

function ResendVerification() {
  const [email, setEmail] = useState("");

  const handleResend = async () => {
    try {
     const res=await api.post("/auth/resend-verification", { email });
      alert(res.data.message || "Verification email resent successfully");
    } catch (err) {
      alert(err.response?.data?.detail || "Error");
    }
  };

  return (
    <div>
      <h2>Resend Verification Email</h2>
      <input
        type="email"
        placeholder="Enter your email"
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={handleResend}>Resend</button>
    </div>
  );
}

export default ResendVerification;