import React, { createContext, useState, useEffect } from 'react';

// Create the UserContext
export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  // On initial load, check if the user is logged in (you can check localStorage, cookies, etc.)
  useEffect(() => {
    const loggedUser = localStorage.getItem('user'); // Example: checking localStorage for logged user
    if (loggedUser) {
      setUser(JSON.parse(loggedUser)); // Set user state if available in localStorage
    }
  }, []);

  // Function to login the user (e.g., after successful login)
  const login = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData)); // Store in localStorage for persistence
  };

  // Function to logout the user
  const logout = () => {
    setUser(null);
    localStorage.removeItem('user'); // Remove from localStorage
  };

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};
