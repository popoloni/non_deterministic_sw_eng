// @ts-nocheck
/**
 * UserProfile - Functional Component with Hooks (After Migration)
 * 
 * 📖 Book Reference: Chapter 7, Pattern 12 - Migration as Learning
 * 
 * This is the hooks-based version of the UserProfile component.
 * Key transformations:
 * - state → useState hooks
 * - componentDidMount → useEffect with [] deps
 * - componentDidUpdate → useEffect with [userId] deps
 * - componentWillUnmount → useEffect cleanup function
 * - Methods → useCallback for callbacks passed to children
 * 
 * NOTE: This is demonstration code. Run `npm install` to enable type checking.
 */

import React, { useState, useEffect, useCallback } from 'react';

// Types (unchanged from class version)
interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
  role: string;
  createdAt: string;
}

interface Props {
  userId: string;
  showDetails?: boolean;
  onUserLoad?: (user: User) => void;
}

// Mock API (unchanged)
const api = {
  getUser: async (userId: string): Promise<User> => {
    return {
      id: userId,
      name: 'John Doe',
      email: 'john@example.com',
      avatar: 'https://example.com/avatar.jpg',
      role: 'Developer',
      createdAt: '2024-01-15',
    };
  },
};

// Components (unchanged)
const Spinner: React.FC = () => <div className="spinner">Loading...</div>;
const ErrorMessage: React.FC<{ message: string }> = ({ message }) => (
  <div className="error">{message}</div>
);

/**
 * UserProfile Functional Component
 * 
 * Migration notes:
 * - Separate useState for each state variable (loading, user, error)
 * - useEffect handles mount, update, and cleanup
 * - Cancelled flag prevents state updates after unmount
 * - useCallback for handleRefresh since it could be passed to children
 */
function UserProfile({ userId, showDetails, onUserLoad }: Props) {
  // State - separate useState for each variable
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Fetch user data - combines componentDidMount and componentDidUpdate
  useEffect(() => {
    // Cancelled flag replaces this.mounted pattern
    let cancelled = false;

    async function fetchUser() {
      setLoading(true);
      setError(null);

      try {
        const userData = await api.getUser(userId);
        
        // Only update state if not cancelled (component still mounted)
        if (!cancelled) {
          setLoading(false);
          setUser(userData);
          
          // Notify parent if callback provided
          if (onUserLoad) {
            onUserLoad(userData);
          }
        }
      } catch (err) {
        if (!cancelled) {
          setLoading(false);
          setError(err instanceof Error ? err.message : 'Failed to load user');
        }
      }
    }

    fetchUser();

    // Cleanup function - replaces componentWillUnmount
    return () => {
      cancelled = true;
    };
  }, [userId, onUserLoad]); // Dependencies: refetch when userId or callback changes

  // Event handler - useCallback since it might be passed to children
  const handleRefresh = useCallback(() => {
    // Trigger refetch by updating a dependency would be one approach,
    // but for explicit refresh we can inline the fetch logic
    // For simplicity, we re-trigger the effect by not caching fetchUser
    setLoading(true);
    setError(null);
    
    api.getUser(userId)
      .then(userData => {
        setUser(userData);
        setLoading(false);
        if (onUserLoad) {
          onUserLoad(userData);
        }
      })
      .catch(err => {
        setError(err instanceof Error ? err.message : 'Failed to load user');
        setLoading(false);
      });
  }, [userId, onUserLoad]);

  // Render helper - now a regular function (not a method)
  function renderUserDetails() {
    if (!user || !showDetails) return null;

    return (
      <div className="user-details">
        <p>Email: {user.email}</p>
        <p>Role: {user.role}</p>
        <p>Member since: {user.createdAt}</p>
      </div>
    );
  }

  // Loading state
  if (loading) {
    return <Spinner />;
  }

  // Error state
  if (error) {
    return (
      <div className="user-profile error-state">
        <ErrorMessage message={error} />
        <button onClick={handleRefresh}>Retry</button>
      </div>
    );
  }

  // No user found
  if (!user) {
    return <div className="user-profile">User not found</div>;
  }

  // Success state
  return (
    <div className="user-profile">
      <div className="user-header">
        <img src={user.avatar} alt={user.name} className="avatar" />
        <h2>{user.name}</h2>
      </div>
      
      {renderUserDetails()}
      
      <button onClick={handleRefresh}>Refresh</button>
    </div>
  );
}

export default UserProfile;
export type { User, Props };
