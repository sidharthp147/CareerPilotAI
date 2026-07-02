import { useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import api from "./api";

function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get("token");

  useEffect(() => {
    const verify = async () => {
      try {
        await api.get(`/auth/verify-email?token=${token}`);
        alert("Email verified successfully ✅");
        navigate("/login");
      } catch (error) {
        alert("Verification failed ❌");
        console.error("Verification error:", error.response?.data || error.message);
      }
    };

    if (token) verify();
  }, [token]);

  return <h2>Verifying your email...</h2>;
}

export default VerifyEmail;