import React, { useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css"; // Import Bootstrap CSS

const Login = () => {
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:8000/api/login/",
        credentials
      );
      localStorage.setItem("token", response.data.token);
      alert("Login successful!");
    } catch (err) {
      setError("Invalid username or password");
    }
  };

  return (
    <div>

      {/* Login Form Section */}
      <div
        className="container d-flex justify-content-center align-items-center"
        style={{ height: "80vh" }}
      >
        <div
          className="card shadow-lg p-4"
          style={{
            width: "400px",
            borderRadius: "10px",
            boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
          }}
        >
          <h2 className="text-center mb-4 text-primary">Login</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group mb-4">
              <label htmlFor="username" className="form-label" style={{ fontWeight: "bold", fontSize: "16px" }}>
                Username
              </label>
              <input
                type="text"
                className="form-control"
                id="username"
                name="username"
                placeholder="Enter your username"
                onChange={handleChange}
                required
                style={{ padding: "10px" }}
              />
            </div>
            <div className="form-group mb-4">
              <label htmlFor="password" className="form-label" style={{ fontWeight: "bold", fontSize: "16px" }}>
                Password
              </label>
              <input
                type="password"
                className="form-control"
                id="password"
                name="password"
                placeholder="Enter your password"
                onChange={handleChange}
                required
                style={{ padding: "10px" }}
              />
            </div>
            {error && <p className="text-danger">{error}</p>}
            <button type="submit" className="btn btn-primary w-100" style={{ padding: "10px", fontSize: "16px" }}>
              Login
            </button>
          </form>
          <p className="text-center mt-3">
            Don't have an account?{" "}
            <a href="/Signup" className="text-primary">
              Sign Up
            </a>
          </p>
        </div>
      </div>

      {/* Footer Section */}
      <footer className="bg-light text-center py-3 mt-auto">
        <p className="mb-0">
          © 2024 Medical Insurance Cost Prediction System. All rights reserved.
        </p>
      </footer>
    </div>
  );
};

export default Login;
