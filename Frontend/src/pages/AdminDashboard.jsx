import { useEffect, useState } from "react";
import api from "./api";
import styles from "./AdminDashboard.module.css";
import { useNavigate } from "react-router-dom";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get("/admin/AdminAnalytics");
        setStats(res.data);
      } catch (err) {
        setError(
          err.response?.data?.message ||
            "Failed to load analytics"
        );
      }
    };

    fetchData();
  }, []);

  if (error) {
    return (
      <div className={styles.container}>
        <p className={styles.error}>
          {error}
        </p>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className={styles.container}>
        <h2>Loading...</h2>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.wrapper}>
        <h1 className={styles.title}>
          Admin Analytics Dashboard
        </h1>
        <div className={styles.subtitle}>
          <button
            className={styles.pendingApprovalBtn}
            onClick={() => navigate("/AdminDashboard/recruiterapproval")}
          >
            Recruiter Approvals
          </button>
        </div>

        {/* KPI */}
        <div className={styles.kpiGrid}>
          <div className={styles.kpiCard}>
            <h2>
              {stats.users.total}
            </h2>
            <p>Total Users</p>
          </div>

          <div className={styles.kpiCard}>
            <h2>
              {
                stats.recruiters
                  .total
              }
            </h2>
            <p>
              Total Recruiters
            </p>
          </div>

          <div className={styles.kpiCard}>
            <h2>
              {stats.jobs.total}
            </h2>
            <p>Total Jobs</p>
          </div>

          <div className={styles.kpiCard}>
            <h2>
              {
                stats.applications
                  .total
              }
            </h2>
            <p>
              Applications
            </p>
          </div>
        </div>

        {/* PERIOD STATS */}
        <div className={styles.analyticsGrid}>
          <div
            className={
              styles.analyticsCard
            }
          >
            <h3>Users</h3>

            <p>
              Today:
              {
                stats.users.today
              }
            </p>

            <p>
              Week:
              {
                stats.users.week
              }
            </p>

            <p>
              Month:
              {
                stats.users.month
              }
            </p>

            <p>
              Year:
              {
                stats.users.year
              }
            </p>
          </div>

          <div
            className={
              styles.analyticsCard
            }
          >
            <h3>Recruiters</h3>

            <p>
              Today:
              {
                stats.recruiters
                  .today
              }
            </p>

            <p>
              Week:
              {
                stats.recruiters
                  .week
              }
            </p>

            <p>
              Month:
              {
                stats.recruiters
                  .month
              }
            </p>

            <p>
              Year:
              {
                stats.recruiters
                  .year
              }
            </p>
          </div>

          <div
            className={
              styles.analyticsCard
            }
          >
            <h3>Jobs</h3>

            <p>
              Today:
              {
                stats.jobs.today
              }
            </p>

            <p>
              Week:
              {
                stats.jobs.week
              }
            </p>

            <p>
              Month:
              {
                stats.jobs.month
              }
            </p>

            <p>
              Year:
              {
                stats.jobs.year
              }
            </p>
          </div>

          <div
            className={
              styles.analyticsCard
            }
          >
            <h3>
              Applications
            </h3>

            <p>
              Today:
              {
                stats
                  .applications
                  .today
              }
            </p>

            <p>
              Week:
              {
                stats
                  .applications
                  .week
              }
            </p>

            <p>
              Month:
              {
                stats
                  .applications
                  .month
              }
            </p>

            <p>
              Year:
              {
                stats
                  .applications
                  .year
              }
            </p>
          </div>
        </div>

        {/* CHARTS */}

        <div className={styles.chartGrid}>
          <div
            className={
              styles.chartCard
            }
          >
            <h3>User Growth</h3>

            <ResponsiveContainer
              width="100%"
              height={300}
            >
              <LineChart
                data={
                  stats.user_growth
                }
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="count"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div
            className={
              styles.chartCard
            }
          >
            <h3>
              Application Trend
            </h3>

            <ResponsiveContainer
              width="100%"
              height={300}
            >
              <AreaChart
                data={
                  stats.application_trend
                }
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />

                <Area dataKey="count" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* LISTS */}

        <div className={styles.listGrid}>
          <div
            className={
              styles.listCard
            }
          >
            <h3>
              Top Recruiters
            </h3>

            {stats.top_recruiters.map(
              (item, index) => (
                <div
                  key={index}
                  className={
                    styles.listItem
                  }
                >
                  <span>
                    {item.name}
                  </span>

                  <strong>
                    {item.jobs}
                  </strong>
                </div>
              )
            )}
          </div>

          <div
            className={
              styles.listCard
            }
          >
            <h3>
              Most Applied Jobs
            </h3>

            {stats.most_applied_jobs.map(
              (item, index) => (
                <div
                  key={index}
                  className={
                    styles.listItem
                  }
                >
                  <span>
                    {item.title}
                  </span>

                  <strong>
                    {
                      item.applications
                    }
                  </strong>
                </div>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;