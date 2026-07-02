import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "./api";
import styles from "./ForgotPassword.module.css";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [expiry, setExpiry] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [serverOtp, setServerOtp] = useState("");
  const [userOtp, setUserOtp] = useState("");
  const [onExpiry,setOnExpiry]=useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (loading) return;

    setLoading(true);
    setMessage("");

    try {
      const res = await api.post("/auth/ForgotPassword", {
        email,
      });

      setMessage(res.data.message);
      setServerOtp(String(res.data.otp));
      setExpiry(res.data.expiry);
      setOtpSent(true);

    } catch (err) {
      setMessage(
        err.response?.data?.detail ||
        "Failed to send OTP. Please try again."
      );

      setOtpSent(false);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = () => {
    if (serverOtp !== userOtp) {
      setMessage("Invalid OTP");
      return;
    }
    if (new Date() > new Date(expiry)) {
      setMessage("OTP Expired");
      setOnExpiry(true);
      return;
    }
    setMessage("OTP Verified");

    navigate("/ForgotPassword/ResetPassword", {
      state: {
        email,
      },
    });
  };

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <div className={styles.header}>
          <h1>Forgot Password?</h1>
          <p>
            Enter your email address and we'll send you an OTP to reset your
            password.
          </p>
        </div>

        <form onSubmit={handleSubmit} className={styles.form}>
          <label>Email Address</label>

          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          {!otpSent && (
            <button
              type="submit"
              className={styles.submitButton}
              disabled={loading}
            >
              {loading ? "Sending OTP..." : "Send OTP"}
            </button>
          )}
          {onExpiry && (
            <button
              type="submit"
              className={styles.submitButton}
              disabled={loading}
            >
              {loading ? "Resending OTP..." : "Resend OTP"}
            </button>
          )}

          {otpSent && (
            <>
              <input
                type="text"
                placeholder="Enter 6 Digit OTP"
                maxLength={6}
                value={userOtp}
                onChange={(e) =>
                  setUserOtp(e.target.value.replace(/\D/g, ""))
                }
                required
              />

              <button
                type="button"
                onClick={handleVerifyOtp}
                className={styles.submitButton}
                disabled={loading}
              >
                Verify OTP
              </button>
            </>
          )}
        </form>

        {message && (
          <div className={styles.message}>
            {message}
          </div>
        )}

        <Link to="/login" className={styles.backLink}>
          ← Back to Login
        </Link>
      </div>
    </div>
  );
}

export default ForgotPassword;