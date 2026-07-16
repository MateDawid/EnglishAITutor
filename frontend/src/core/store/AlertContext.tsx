/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState, type JSX, type ReactNode } from 'react';

/**
 * Alert type definition. It represents the structure of an alert message, including the message text and its type (success, error, info, or warning).
 */
type Alert = {
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
}

/**
 * AlertContextType defines the shape of the context value provided by AlertContext. It includes the current alert state and a function to update it.
 */
type AlertContextType = {
  alert: Alert | null;
  setAlert: (alert: Alert | null) => void;
}

/**
 * ChildrenType defines the props for the AlertProvider component, specifically the children that will be wrapped by the provider.
 */
type ChildrenType = {
  children: ReactNode;
};

const AlertContext = createContext<AlertContextType | undefined>(undefined);

/**
 * Provider component for AlertContext. It provides the alert state and setAlert function to its children.
 * 
 * @param {ChildrenType} children The child components that will have access to the alert context.
 * @returns {JSX.Element} The AlertContext.Provider component wrapping the children.
 */
export const AlertProvider = ({ children }: ChildrenType): JSX.Element => {
  const [alert, setAlert] = useState<Alert | null>(null);

  const value = { alert, setAlert };

  return (
    <AlertContext.Provider value={value}>{children}</AlertContext.Provider>
  );
};


/**
 * Hook to access the AlertContext. It throws an error if used outside of the AlertProvider.
 * 
 * @returns AlertContextType - The current alert state and the setAlert function.
 */
export const useAlertContext = (): AlertContextType => {
  const context = useContext(AlertContext);
  if (!context) throw new Error('useAlertContext must be used within AlertProvider');
  return context;
};