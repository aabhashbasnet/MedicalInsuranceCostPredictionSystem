import React, { createContext, useState, useContext } from 'react';

// Create UserContext
const UserContext = createContext();

// Provide context and logic for login, logout
export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = (userData) => {
    setUser(userData);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};

// Hook to use the UserContext
export const useUser = () => {
  return useContext(UserContext);
};
