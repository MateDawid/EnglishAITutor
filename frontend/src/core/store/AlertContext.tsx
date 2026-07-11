import { createContext, useContext, useState, type JSX, type ReactNode } from 'react';

type Alert = {
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
}

type AlertContextType = {
  alert: Alert | null;
  setAlert: (alert: Alert | null) => void;
}

type ChildrenType = {
  children: ReactNode;
};

const AlertContext = createContext<AlertContextType | undefined>(undefined);

/**
 * Provider component for AlertContext. It provides the alert state and setAlert function to its children.
 * 
 * @param children - The child components that will have access to the alert context.
 * @returns The AlertContext.Provider component wrapping the children.
 */
export const AlertProvider = ({ children }: ChildrenType): JSX.Element => {
  const [alert, setAlert] = useState<Alert | null>(null);

  const value = {
    alert,
    setAlert,
  };

  return (
    <AlertContext.Provider value={value}>{children}</AlertContext.Provider>
  );
};


/**
 * 
 * @returns 
 */
export const useAlertContext = (): AlertContextType => {
  const context = useContext(AlertContext);
  if (!context) throw new Error('useAlert must be used within AlertProvider');
  return context;
};