import React, { createContext, useContext, useState } from 'react';

// Create a context
const UserContext = createContext();

// UserProvider component to wrap around the component tree
export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null); // Initially, no user is logged in

  // You can replace this with actual login logic
  const login = (userData) => setUser(userData);
  const logout = () => setUser(null);

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};

// Custom hook to access the user context
export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
};
