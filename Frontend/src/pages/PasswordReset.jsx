import { useState } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import api from "./api";
import styles from "./PasswordReset.module.css";

function ResetPassword() {
  const navigate = useNavigate();
  const location = useLocation();

  const email = location.state?.email || "";

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleResetPassword = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }
    if (!validatepassword(password)) {
      setMessage(
        "Password must contain uppercase, lowercase, number and special character."
      );
      return;
    }

    try {
      setLoading(true);

      const res = await api.post("/auth/resetpassword", {
        email,
        new_password: password,
      });

      setMessage(res.data.message);

      setTimeout(() => {
        navigate("/");
      }, 2000);
    } catch (err) {
      setMessage(
        err.response?.data?.detail ||
          "Failed to reset password"
      );
    } finally {
      setLoading(false);
    }
  };
  const validatepassword = (password) => {

    const regex =/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$/;

    return regex.test(password);
  };

  return (
    <div className={styles.container}>
      <div className={styles.hero}>
        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <h1>Reset Password</h1>
            <p>
              Create a strong password to secure your account.
            </p>
          </div>

          <form
            onSubmit={handleResetPassword}
            className={styles.form}
          >
            <div className={styles.inputGroup}>
              <label>New Password</label>
              <input
                type="password"
                placeholder="Enter new password"
                value={password}
                onChange={(e) =>
                  setPassword(e.target.value)
                }
                required
              />
            </div>

            <div className={styles.inputGroup}>
              <label>Confirm Password</label>
              <input
                type="password"
                placeholder="Confirm new password"
                value={confirmPassword}
                onChange={(e) =>
                  setConfirmPassword(e.target.value)
                }
                required
              />
            </div>

            <button
              type="submit"
              className={styles.primaryBtn}
              disabled={loading}
            >
              {loading
                ? "Updating Password..."
                : "Reset Password"}
            </button>
          </form>

          {message && (
            <div className={styles.message}>
              {message}
            </div>
          )}

          <Link
            to="/"
            className={styles.secondaryBtn}
          >
            Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
}

export default ResetPassword;