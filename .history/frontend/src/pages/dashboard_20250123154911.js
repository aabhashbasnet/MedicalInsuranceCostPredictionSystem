import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

const Dashboard = () => {
  const navigate = useNavigate();

  // Check if the user is authenticated (e.g., token exists)
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("You are not logged in! Redirecting to login.");
      navigate("/login");
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token"); // Clear the token
    alert("You have been logged out!");
    navigate("/login"); // Redirect to login page
  };

  return (
    <div>
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container">
          <a className="navbar-brand text-primary" href="/dashboard">
            Insurance System
          </a>
          <button
            className="btn btn-outline-danger"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
      </nav>

      {/* Main Dashboard Content */}
      <div className="container mt-4">
        <h1 className="text-center text-primary mb-4">Welcome to Your Dashboard</h1>
        <p className="text-center">
          Here you can manage your account, view reports, and access various features.
        </p>

        {/* Placeholder for Dashboard Features */}
        <div className="row mt-5">
          <div className="col-md-4">
            <div className="card shadow-sm">
              <div className="card-body text-center">
                <h5 className="card-title">Profile</h5>
                <p className="card-text">View and edit your account details.</p>
                <a href="/profile" className="btn btn-primary">
                  Go to Profile
                </a>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card shadow-sm">
              <div className="card-body text-center">
                <h5 className="card-title">Reports</h5>
                <p className="card-text">Download and view your insurance reports.</p>
                <a href="/reports" className="btn btn-primary">
                  View Reports
                </a>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card shadow-sm">
              <div className="card-body text-center">
                <h5 className="card-title">Support</h5>
                <p className="card-text">Need help? Contact support or use the chatbot.</p>
                <a href="/support" className="btn btn-primary">
                  Get Support
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-light text-center py-3 mt-5">
        <p className="mb-0">
          © 2024 Medical Insurance Cost Prediction System. All rights reserved.
        </p>
      </footer>
    </div>
  );
};

export default Dashboard;
