import React, { useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const Signup = () => {
  const [credentials, setCredentials] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const validateForm = () => {
    if (!credentials.username || !credentials.email || !credentials.password || !credentials.confirmPassword) {
      setError("All fields are required.");
      return false;
    }

    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailPattern.test(credentials.email)) {
      setError("Please enter a valid email address.");
      return false;
    }

    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!passwordPattern.test(credentials.password)) {
      setError("Password must be at least 8 characters long, contain one number, and one special character.");
      return false;
    }

    if (credentials.password !== credentials.confirmPassword) {
      setError("Passwords do not match.");
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setError(""); // Clear previous errors

    try {
      const response = await axios.post("http://localhost:8000/api/signup/", {
        username: credentials.username,
        email: credentials.email,
        password: credentials.password,
      });

      if (response.status === 201) {
        setSuccess("Signup successful! Redirecting to login...");
        setTimeout(() => {
          window.location.href = "/login";
        }, 2000);
      } else {
        setError("Unexpected response from server. Please try again.");
      }
    } catch (err) {
      // Handle server errors
      if (err.response && err.response.data) {
        setError(err.response.data.message || "Signup failed. Please try again.");
      } else {
        setError("Unable to connect to the server. Please check your network.");
      }
    }
  };

  return (
    <div>
      {/* Signup Form Section */}
      <div
        className="container d-flex justify-content-center align-items-center"
        style={{ height: "80vh" }}
      >
        <div
          className="card shadow-lg p-4"
          style={{ width: "400px", borderRadius: "10px" }}
        >
          <h2 className="text-center mb-4 text-primary">Sign Up</h2>
          {success && <p className="text-success">{success}</p>}
          {error && <p className="text-danger">{error}</p>}
          <form onSubmit={handleSubmit}>
            <div className="form-group mb-3">
              <label htmlFor="username" className="form-label">
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
              />
            </div>
            <div className="form-group mb-3">
              <label htmlFor="email" className="form-label">
                Email
              </label>
              <input
                type="email"
                className="form-control"
                id="email"
                name="email"
                placeholder="Enter your email"
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group mb-3">
              <label htmlFor="password" className="form-label">
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
              />
            </div>
            <div className="form-group mb-3">
              <label htmlFor="confirmPassword" className="form-label">
                Confirm Password
              </label>
              <input
                type="password"
                className="form-control"
                id="confirmPassword"
                name="confirmPassword"
                placeholder="Confirm your password"
                onChange={handleChange}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary w-100">
              Sign Up
            </button>
          </form>
          <p className="text-center mt-3">
            Already have an account?{" "}
            <a href="/login" className="text-primary">
              Login
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

export default Signup;
